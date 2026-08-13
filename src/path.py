"""
Compatibility module for Path assessment.

Public interface is now split across:
- path_data.py
- path_logic.py
- path_ui.py
"""

import flet as ft

from path_data import CATEGORIES, STATEMENTS, REVERSE_ITEMS
from path_logic import CareerPathAssessment, generate_career_narrative
from path_ui import create_career_path_assessment_ui, _run_standalone

__all__ = [
    "CATEGORIES",
    "STATEMENTS",
    "REVERSE_ITEMS",
    "CareerPathAssessment",
    "generate_career_narrative",
    "create_career_path_assessment_ui",
    "_run_standalone",
]


if __name__ == "__main__":
    ft.app(target=_run_standalone)
