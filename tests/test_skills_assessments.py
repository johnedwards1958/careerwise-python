"""Regression tests for the skills-related assessment result calculations."""

from collections import Counter
import math
from pathlib import Path
import sys
import unittest


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from skills_data import CATEGORIES, DETAILED_FEEDBACK  # noqa: E402
from skills_logic import SkillsAssessment  # noqa: E402
from teams_data import ROLE_MAPPING  # noqa: E402
from teams_logic import TeamsAssessment  # noqa: E402
from transferrable_logic import TransferrableSkillsAssessment  # noqa: E402


def ratings_with_total(count, total):
    """Return ``count`` integer ratings in 1..5 that add up to ``total``."""
    if total not in range(count, count * 5 + 1):
        raise ValueError("Requested total is outside the rating range")

    ratings = [1] * count
    remaining = total - count
    for index in range(count):
        addition = min(4, remaining)
        ratings[index] += addition
        remaining -= addition
    return ratings


def complete_skills_assessment(total):
    assessment = SkillsAssessment()
    question_keys = [
        (category_id, question_index)
        for category_id, category in assessment.CATEGORIES.items()
        for question_index in range(len(category["questions"]))
    ]
    for key, rating in zip(question_keys, ratings_with_total(len(question_keys), total)):
        assessment.set_response(*key, rating)
    return assessment


def complete_transferrable_assessment(total):
    assessment = TransferrableSkillsAssessment()
    for question_index, rating in enumerate(
        ratings_with_total(len(assessment.QUESTIONS), total)
    ):
        assessment.set_response(question_index, rating)
    return assessment


class SkillsAssessmentTests(unittest.TestCase):
    def test_feedback_covers_every_question_and_rating(self):
        self.assertEqual(set(DETAILED_FEEDBACK), set(CATEGORIES))
        for category_id, category in CATEGORIES.items():
            expected_questions = set(range(len(category["questions"])))
            self.assertEqual(set(DETAILED_FEEDBACK[category_id]), expected_questions)
            for question_index in expected_questions:
                self.assertEqual(
                    set(DETAILED_FEEDBACK[category_id][question_index]),
                    set(range(1, 6)),
                )

    def test_category_threshold_boundaries(self):
        assessment = SkillsAssessment()
        category_id = "skills_abilities"

        for total, expected_status in (
            (18, "needs_improvement"),
            (19, "acceptable"),
            (23, "acceptable"),
            (24, "good"),
        ):
            assessment.reset()
            ratings = ratings_with_total(
                len(assessment.CATEGORIES[category_id]["questions"]), total
            )
            for question_index, rating in enumerate(ratings):
                assessment.set_response(category_id, question_index, rating)
            self.assertEqual(assessment.get_category_status(category_id), expected_status)

    def test_overall_threshold_boundaries(self):
        for total, expected_status in (
            (126, "needs_improvement"),
            (127, "good"),
            (150, "good"),
            (151, "excellent"),
        ):
            assessment = complete_skills_assessment(total)
            self.assertTrue(assessment.is_complete())
            self.assertEqual(assessment.get_overall_status(), expected_status)

    def test_incomplete_and_invalid_responses_cannot_produce_results(self):
        assessment = SkillsAssessment()
        assessment.responses[("not_a_category", 0)] = 5
        self.assertFalse(assessment.is_complete())
        self.assertEqual(assessment.get_completion_percentage(), 0)

        with self.assertRaises(ValueError):
            assessment.set_response("not_a_category", 0, 5)
        with self.assertRaises(ValueError):
            assessment.set_response("skills_abilities", -1, 5)
        with self.assertRaises(ValueError):
            assessment.set_response("skills_abilities", 0, True)
        with self.assertRaises(ValueError):
            assessment.set_response("skills_abilities", 0, 3.0)


class TeamsAssessmentTests(unittest.TestCase):
    def test_mapping_assigns_each_role_once_per_section(self):
        expected_roles = Counter({role_id: 1 for role_id in TeamsAssessment.ROLES})
        for section_id, section in TeamsAssessment.SECTIONS.items():
            mapping = ROLE_MAPPING[section_id]
            self.assertEqual(
                set(mapping), set(range(1, len(section["questions"]) + 1))
            )
            self.assertEqual(Counter(mapping.values()), expected_roles)

    def test_allocations_and_role_scores_preserve_seventy_total_points(self):
        assessment = TeamsAssessment()
        for section_id, section in assessment.SECTIONS.items():
            for question_index in range(len(section["questions"])):
                assessment.set_rating(section_id, question_index, 3)
            self.assertTrue(
                math.isclose(
                    sum(assessment.convert_ratings_to_allocations(section_id)),
                    assessment.POINTS_PER_SECTION,
                    abs_tol=1e-9,
                )
            )

        scores = assessment.calculate_role_scores()
        self.assertTrue(math.isclose(sum(scores.values()), 70.0, abs_tol=1e-9))
        for score in scores.values():
            self.assertTrue(math.isclose(score, 8.75, abs_tol=1e-9))

    def test_equal_scores_are_reported_as_one_tied_rank(self):
        assessment = TeamsAssessment()
        for section_id, section in assessment.SECTIONS.items():
            for question_index in range(len(section["questions"])):
                assessment.set_rating(section_id, question_index, 1)

        groups = assessment.get_ranked_role_groups()
        self.assertEqual(len(groups), 1)
        self.assertEqual({role_id for role_id, _ in groups[0]}, set(assessment.ROLES))
        self.assertEqual(
            {role_id for role_id, _ in assessment.get_top_roles(2)},
            set(assessment.ROLES),
        )

    def test_max_attainable_role_score_on_rating_scale(self):
        assessment = TeamsAssessment()
        target_role = "SH"
        for section_id, section in assessment.SECTIONS.items():
            target_question = next(
                question_number - 1
                for question_number, role_id in ROLE_MAPPING[section_id].items()
                if role_id == target_role
            )
            for question_index in range(len(section["questions"])):
                assessment.set_rating(
                    section_id,
                    question_index,
                    5 if question_index == target_question else 1,
                )

        scores = assessment.calculate_role_scores()
        self.assertTrue(math.isclose(scores[target_role], 175 / 6, abs_tol=1e-9))
        self.assertTrue(math.isclose(sum(scores.values()), 70.0, abs_tol=1e-9))

    def test_invalid_coordinates_and_non_integer_ratings_are_rejected(self):
        assessment = TeamsAssessment()
        with self.assertRaises(ValueError):
            assessment.set_rating("Z", 0, 3)
        with self.assertRaises(ValueError):
            assessment.set_rating("A", 8, 3)
        with self.assertRaises(ValueError):
            assessment.set_rating("A", 0, True)
        with self.assertRaises(ValueError):
            assessment.set_rating("A", 0, 3.0)


class TransferrableSkillsAssessmentTests(unittest.TestCase):
    def test_domains_partition_questions_exactly_once(self):
        question_indices = [
            question_index
            for domain in TransferrableSkillsAssessment.DOMAINS.values()
            for question_index in domain["questions"]
        ]
        self.assertEqual(
            sorted(question_indices),
            list(range(len(TransferrableSkillsAssessment.QUESTIONS))),
        )

    def test_overall_threshold_boundaries(self):
        for total, expected_status in (
            (39, "narrowly_specialised"),
            (40, "developing"),
            (59, "developing"),
            (60, "moderately_transferable"),
            (79, "moderately_transferable"),
            (80, "highly_transferable"),
        ):
            assessment = complete_transferrable_assessment(total)
            self.assertTrue(assessment.is_complete())
            self.assertEqual(assessment.get_overall_status(), expected_status)

    def test_incomplete_and_invalid_responses_cannot_produce_results(self):
        assessment = TransferrableSkillsAssessment()
        assessment.responses[len(assessment.QUESTIONS)] = 5
        self.assertFalse(assessment.is_complete())
        self.assertEqual(assessment.calculate_overall_score(), (0, 100, 0))
        self.assertEqual(assessment.get_completion_percentage(), 0)
        self.assertEqual(assessment.get_overall_status(), "incomplete")

        with self.assertRaises(ValueError):
            assessment.set_response(-1, 5)
        with self.assertRaises(ValueError):
            assessment.set_response(len(assessment.QUESTIONS), 5)
        with self.assertRaises(ValueError):
            assessment.set_response(0, True)
        with self.assertRaises(ValueError):
            assessment.set_response(0, 3.0)


if __name__ == "__main__":
    unittest.main()
