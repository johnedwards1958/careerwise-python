"""Regression tests for the archetype, learning, and career-path assessments."""

from pathlib import Path
import sys
import unittest


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from archetypes_logic import InfluenceArchetypesAssessment
from learning_logic import LearningPreferenceAssessment
from path_logic import CareerPathAssessment, generate_career_narrative


class InfluenceArchetypesAssessmentTests(unittest.TestCase):
    def test_scores_use_only_the_three_defined_statement_slots(self):
        assessment = InfluenceArchetypesAssessment()
        assessment.set_response("Analyst", 0, 1)
        assessment.set_response("Analyst", 1, 3)
        assessment.set_response("Analyst", 2, 5)

        self.assertEqual(assessment.calculate_archetype_score("Analyst"), (3.0, 3))

        # Even if external code mutates the public response mapping, an invalid
        # slot must not change a result or completion status.
        assessment.responses["Analyst"][-1] = 5
        self.assertEqual(assessment.calculate_archetype_score("Analyst"), (3.0, 3))
        self.assertAlmostEqual(assessment.get_completion_percentage(), 3 / 27 * 100)

        assessment.responses["Analyst"][0] = 99
        self.assertEqual(assessment.calculate_archetype_score("Analyst"), (4.0, 2))
        self.assertAlmostEqual(assessment.get_completion_percentage(), 2 / 27 * 100)

    def test_set_response_rejects_invalid_archetypes_indices_and_ratings(self):
        assessment = InfluenceArchetypesAssessment()

        invalid_responses = [
            ("Unknown", 0, 3),
            ("Analyst", -1, 3),
            ("Analyst", 3, 3),
            ("Analyst", 0, 0),
            ("Analyst", 0, 6),
            ("Analyst", 0, True),
        ]
        for response in invalid_responses:
            with self.subTest(response=response), self.assertRaises(ValueError):
                assessment.set_response(*response)

        self.assertEqual(assessment.get_completion_percentage(), 0)

    def test_cluster_definitions_cover_each_archetype_once(self):
        assessment = InfluenceArchetypesAssessment()
        clustered = [
            archetype
            for archetypes in assessment.CLUSTERS.values()
            for archetype in archetypes
        ]

        self.assertCountEqual(clustered, assessment.STATEMENTS)
        self.assertEqual(len(clustered), len(set(clustered)))

    def test_top_archetypes_can_include_a_tie_at_the_cutoff(self):
        assessment = InfluenceArchetypesAssessment()
        ratings = {"Analyst": 5, "Enforcer": 4, "Negotiator": 4}
        for archetype, rating in ratings.items():
            for statement_index in range(len(assessment.STATEMENTS[archetype])):
                assessment.set_response(archetype, statement_index, rating)

        self.assertEqual(
            assessment.get_top_archetypes(count=2),
            [("Analyst", 5.0), ("Enforcer", 4.0), ("Negotiator", 4.0)],
        )


class LearningPreferenceAssessmentTests(unittest.TestCase):
    @staticmethod
    def _option_for_style(question, style):
        return next(
            index
            for index, option in enumerate(question["options"])
            if option["style"] == style
        )

    def test_each_question_maps_one_option_to_each_style(self):
        assessment = LearningPreferenceAssessment()

        for question in assessment.QUESTIONS:
            self.assertCountEqual(
                [option["style"] for option in question["options"]],
                assessment.STYLES,
            )

    def test_selected_options_map_to_style_totals(self):
        assessment = LearningPreferenceAssessment()
        expected_styles = ["V"] * 6 + ["A"] * 4 + ["R"] * 3 + ["K"] * 3

        for question_index, style in enumerate(expected_styles):
            question = assessment.QUESTIONS[question_index]
            assessment.set_response(
                question_index,
                self._option_for_style(question, style),
            )

        self.assertEqual(
            assessment.calculate_style_scores(),
            {"V": 6, "A": 4, "R": 3, "K": 3},
        )
        self.assertEqual(assessment.get_dominant_style(), ("Bimodal", ["V", "A"]))
        self.assertTrue(assessment.is_complete())

    def test_negative_and_out_of_range_indices_cannot_score_or_complete(self):
        assessment = LearningPreferenceAssessment()

        for response in [(-1, 0), (16, 0), (0, -1), (0, 4), (0, True)]:
            with self.subTest(response=response), self.assertRaises(ValueError):
                assessment.set_response(*response)

        assessment.responses[-1] = -1
        assessment.responses[0] = 99
        self.assertEqual(
            assessment.calculate_style_scores(),
            {"V": 0, "A": 0, "R": 0, "K": 0},
        )
        self.assertEqual(assessment.get_completion_status(), (0, 16))
        self.assertFalse(assessment.is_complete())

    def test_equal_style_scores_are_reported_as_multimodal(self):
        assessment = LearningPreferenceAssessment()
        selected_styles = ["V", "A", "R", "K"] * 4
        for question_index, style in enumerate(selected_styles):
            assessment.set_response(
                question_index,
                self._option_for_style(assessment.QUESTIONS[question_index], style),
            )

        self.assertEqual(
            assessment.get_dominant_style(),
            ("Multimodal", ["V", "A", "R", "K"]),
        )


class CareerPathAssessmentTests(unittest.TestCase):
    def test_reverse_keyed_response_is_scored_once_and_preserved_for_display(self):
        assessment = CareerPathAssessment()

        assessment.set_response("R", 8, 1)
        self.assertEqual(assessment.get_response("R", 8), 5)
        self.assertEqual(assessment.get_raw_response("R", 8), 1)

        assessment.set_response("R", 8, 5)
        self.assertEqual(assessment.get_response("R", 8), 1)
        self.assertEqual(assessment.get_raw_response("R", 8), 5)

    def test_set_response_rejects_negative_indices_and_non_integer_scores(self):
        assessment = CareerPathAssessment()

        for response in [("R", -1, 3), ("R", 9, 3), ("R", 0, 0), ("R", 0, 6), ("R", 0, True)]:
            with self.subTest(response=response), self.assertRaises(ValueError):
                assessment.set_response(*response)

        assessment.responses[("R", -1)] = 5
        assessment.responses[("R", 0)] = 99
        self.assertEqual(assessment.get_completion_counts(), (0, 54))
        self.assertEqual(assessment.calculate_category_score("R")[0], 0)
        self.assertFalse(assessment.is_complete())

    def test_page_layout_contains_every_statement_exactly_once(self):
        assessment = CareerPathAssessment()
        paged_items = [
            (category, statement_index)
            for page in assessment.get_statements_by_page()
            for category, statement_index, _ in page
        ]
        expected_items = [
            (category, statement_index)
            for category, statements in assessment.STATEMENTS.items()
            for statement_index in range(len(statements))
        ]

        self.assertCountEqual(paged_items, expected_items)
        self.assertEqual(len(paged_items), len(set(paged_items)))

    def test_equal_scores_are_reported_as_a_tie_not_an_arbitrary_code(self):
        assessment = CareerPathAssessment()
        for category, statements in assessment.STATEMENTS.items():
            for statement_index in range(len(statements)):
                assessment.set_response(category, statement_index, 3)

        code, top_three, is_complete = assessment.get_interest_code()

        self.assertTrue(is_complete)
        self.assertEqual(code, "(R/I/A/S/E/C)")
        self.assertEqual(
            [category for category, _, _ in top_three],
            ["R", "I", "A", "S", "E", "C"],
        )
        self.assertIn("does not assign an arbitrary order", assessment.get_career_narrative())

    def test_third_place_tie_includes_every_category_at_the_cutoff(self):
        assessment = CareerPathAssessment()
        scored_rating = {"R": 5, "I": 4, "A": 3, "S": 3, "E": 2, "C": 1}
        for category, statements in assessment.STATEMENTS.items():
            for statement_index in range(len(statements)):
                raw_rating = scored_rating[category]
                if statement_index in assessment.REVERSE_ITEMS[category]:
                    raw_rating = 6 - raw_rating
                assessment.set_response(category, statement_index, raw_rating)

        code, top_ranked, is_complete = assessment.get_interest_code()

        self.assertTrue(is_complete)
        self.assertEqual(code, "RI(A/S)")
        self.assertEqual(
            [category for category, _, _ in top_ranked],
            ["R", "I", "A", "S"],
        )

    def test_cronbach_alpha_reverse_scores_items_and_uses_complete_rows(self):
        assessment = CareerPathAssessment()
        raw_responses = [
            [1] * 8 + [5],
            [5] * 8 + [1],
            [None] + [3] * 8,
        ]

        alpha, item_count, respondent_count = assessment.calculate_cronbach_alpha(
            "R", raw_responses
        )

        self.assertAlmostEqual(alpha, 1.0)
        self.assertEqual(item_count, 9)
        self.assertEqual(respondent_count, 2)

    def test_narrative_does_not_substitute_an_unrelated_interest_pair(self):
        narrative = generate_career_narrative(
            "ARC",
            [("A", 40, 88.9), ("R", 35, 77.8), ("C", 30, 66.7)],
        )

        self.assertNotIn("Artistic-Social", narrative)
        self.assertIn("artistic and realistic elements", narrative)


if __name__ == "__main__":
    unittest.main()
