"""Regression tests for priorities, environment, and relationships results."""

from pathlib import Path
import sys
import unittest


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from environment_logic import EnvironmentAssessment
from priorities_logic import PrioritiesAssessment
from relationships_logic import RelationshipsAssessment


class PrioritiesAssessmentTests(unittest.TestCase):
    @staticmethod
    def _set_anchor_score(assessment, anchor_id, target_score):
        """Set five 1-5 responses that add up to target_score."""
        question_count = len(assessment.ANCHORS[anchor_id]["questions"])
        remaining = target_score - question_count
        for question_index in range(question_count):
            addition = min(4, remaining)
            assessment.set_response(anchor_id, question_index, 1 + addition)
            remaining -= addition
        if remaining:
            raise AssertionError("Target score is outside the valid range")

    def test_response_validation_rejects_invalid_slots_and_non_integer_ratings(self):
        assessment = PrioritiesAssessment()
        anchor_id = next(iter(assessment.ANCHORS))

        for response in [
            ("unknown", 0, 3),
            (anchor_id, -1, 3),
            (anchor_id, 5, 3),
            (anchor_id, 0, 0),
            (anchor_id, 0, 6),
            (anchor_id, 0, True),
            (anchor_id, 0, 3.0),
        ]:
            with self.subTest(response=response), self.assertRaises(ValueError):
                assessment.set_response(*response)

    def test_top_anchors_include_every_tie_at_the_cutoff(self):
        assessment = PrioritiesAssessment()
        anchor_ids = list(assessment.ANCHORS)
        target_scores = [25, 20, 20, 20, 15, 14, 13, 12]
        for anchor_id, score in zip(anchor_ids, target_scores):
            self._set_anchor_score(assessment, anchor_id, score)

        self.assertTrue(assessment.is_complete())
        self.assertEqual(
            assessment.get_top_anchors(2),
            [(anchor_ids[0], 25), *[(anchor_id, 20) for anchor_id in anchor_ids[1:4]]],
        )

    def test_equal_scores_are_all_joint_top_anchors(self):
        assessment = PrioritiesAssessment()
        for anchor_id in assessment.ANCHORS:
            self._set_anchor_score(assessment, anchor_id, 15)

        self.assertEqual(
            [anchor_id for anchor_id, _ in assessment.get_top_anchors(2)],
            list(assessment.ANCHORS),
        )


class EnvironmentAssessmentTests(unittest.TestCase):
    @staticmethod
    def _answer(assessment, options):
        for factor_index, option in zip(assessment.FACTORS, options):
            assessment.set_response(factor_index, option)

    def test_a_and_c_responses_map_to_profiles_described_by_the_options(self):
        structured = EnvironmentAssessment()
        self._answer(structured, "A" * len(structured.FACTORS))
        self.assertEqual(structured.get_dominant_pattern(), ("A", 12, "structured"))
        self.assertEqual(structured.get_interpretation()["profile_key"], "structured")
        self.assertIn("Structured", structured.get_interpretation()["title"])

        autonomous = EnvironmentAssessment()
        self._answer(autonomous, "C" * len(autonomous.FACTORS))
        self.assertEqual(autonomous.get_dominant_pattern(), ("C", 12, "autonomous"))
        self.assertEqual(autonomous.get_interpretation()["profile_key"], "autonomous")
        self.assertIn("Autonomous", autonomous.get_interpretation()["title"])

    def test_tied_patterns_produce_a_mixed_result_not_an_arbitrary_winner(self):
        assessment = EnvironmentAssessment()
        self._answer(assessment, "A" * 6 + "C" * 6)

        self.assertIsNone(assessment.get_dominant_pattern())
        self.assertEqual(
            assessment.get_dominant_patterns(),
            [("A", 6, "structured"), ("C", 6, "autonomous")],
        )
        interpretation = assessment.get_interpretation()
        self.assertEqual(interpretation["profile_key"], "mixed")
        self.assertEqual(interpretation["dominant_options"], ["A", "C"])
        self.assertIsNone(interpretation["dominant_option"])

    def test_only_valid_defined_factor_slots_count_toward_completion(self):
        assessment = EnvironmentAssessment()
        self._answer(assessment, "B" * 11)
        assessment.responses[99] = "A"

        self.assertFalse(assessment.is_complete())
        self.assertEqual(assessment.get_completion_status(), (11, 12, 11 / 12 * 100))
        self.assertEqual(assessment.get_pattern_counts(), {"A": 0, "B": 11, "C": 0})

        for response in [(False, "A"), (-1, "A"), (12, "A"), (0, "D")]:
            with self.subTest(response=response), self.assertRaises(ValueError):
                assessment.set_response(*response)


class RelationshipsAssessmentTests(unittest.TestCase):
    VALID_REFLECTION = (
        "This is a detailed account of what happened, how it affected the work, "
        "and what I learned from the experience."
    )

    def test_completion_requires_each_required_prompt_to_be_valid(self):
        assessment = RelationshipsAssessment()
        index = assessment.add_relationship("Supportive manager", "positive")

        for prompt_index in range(5):
            assessment.set_reflection(index, prompt_index, "Too short.")
        self.assertFalse(assessment.is_relationship_complete(index))
        self.assertEqual(assessment.get_relationship_progress(index), (0, 5))

        for prompt_index in range(5):
            assessment.set_reflection(index, prompt_index, self.VALID_REFLECTION)
        self.assertTrue(assessment.is_relationship_complete(index))
        self.assertEqual(assessment.get_relationship_progress(index), (5, 5))

        assessment.relationships[index]["reflections"].pop(4)
        assessment.relationships[index]["reflections"][99] = self.VALID_REFLECTION
        self.assertFalse(assessment.is_relationship_complete(index))

    def test_reflection_slots_are_range_checked(self):
        assessment = RelationshipsAssessment()
        index = assessment.add_relationship("Former colleague", "challenging")

        for response in [
            (-1, 0, self.VALID_REFLECTION),
            (index, -1, self.VALID_REFLECTION),
            (index, 5, self.VALID_REFLECTION),
            (index, True, self.VALID_REFLECTION),
            (index, 0, None),
        ]:
            with self.subTest(response=response), self.assertRaises(ValueError):
                assessment.set_reflection(*response)

    def test_zero_score_themes_are_not_reported_as_results(self):
        assessment = RelationshipsAssessment()
        result = assessment._analyze_text(
            ["The colleague prepared documents each week and attended every scheduled meeting."],
            assessment.THEMES,
        )

        self.assertEqual(result["total_matches"], 0)
        self.assertEqual(result["top_themes"], [])

    def test_duplicate_keywords_do_not_double_count_a_mention(self):
        assessment = RelationshipsAssessment()
        result = assessment._analyze_text(
            ["They were responsible."],
            assessment.THEMES,
        )

        self.assertEqual(result["theme_scores"]["accountability"], 1.0)
        self.assertEqual(
            assessment.THEMES["accountability"]["keywords"].count("responsible"),
            1,
        )

    def test_negation_handles_contractions_without_crossing_sentences(self):
        assessment = RelationshipsAssessment()

        self.assertEqual(
            assessment._count_keyword_in_text("They didn't deliver.", "deliver"),
            0,
        )
        self.assertEqual(
            assessment._count_keyword_in_text("They were not honest.", "honest"),
            0,
        )
        self.assertEqual(
            assessment._count_keyword_in_text(
                "They were not clear. Their later feedback was honest.", "honest"
            ),
            1,
        )

    def test_theme_ties_at_the_display_cutoff_are_kept(self):
        assessment = RelationshipsAssessment()
        themes = {
            theme_id: {
                "keywords": [keyword],
                "weight": 1.0,
            }
            for theme_id, keyword in zip("abcd", ("alpha", "bravo", "charlie", "delta"))
        }

        result = assessment._analyze_text(
            ["alpha bravo charlie delta"],
            themes,
        )
        self.assertEqual(result["top_themes"], ["a", "b", "c", "d"])


if __name__ == "__main__":
    unittest.main()
