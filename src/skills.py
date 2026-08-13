"""
Compatibility module for Job Search Skills assessment.

Public interface is now split across:
- skills_data.py
- skills_logic.py
- skills_ui.py
"""

import flet as ft

from skills_data import CATEGORIES, CATEGORY_FEEDBACK, DETAILED_FEEDBACK
from skills_logic import SkillsAssessment, get_category_feedback, get_detailed_feedback
from skills_ui import create_skills_assessment_ui, create_skills_page, _run_standalone

__all__ = [
    "CATEGORIES",
    "DETAILED_FEEDBACK",
    "CATEGORY_FEEDBACK",
    "SkillsAssessment",
    "get_detailed_feedback",
    "get_category_feedback",
    "create_skills_assessment_ui",
    "create_skills_page",
    "_run_standalone",
]


if __name__ == "__main__":
    ft.app(target=_run_standalone)

