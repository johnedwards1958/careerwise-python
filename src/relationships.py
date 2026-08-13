"""
Compatibility module for Relationships assessment.

Public interface is now split across:
- relationships_data.py
- relationships_logic.py
- relationships_ui.py
"""

import flet as ft

from relationships_data import THEMES, FRUSTRATION_THEMES, POSITIVE_PROMPTS, CHALLENGING_PROMPTS, NEGATION_WORDS
from relationships_logic import RelationshipsAssessment
from relationships_ui import create_relationships_assessment_ui, create_relationships_page, _run_standalone

__all__ = [
    "THEMES",
    "FRUSTRATION_THEMES",
    "POSITIVE_PROMPTS",
    "CHALLENGING_PROMPTS",
    "NEGATION_WORDS",
    "RelationshipsAssessment",
    "create_relationships_assessment_ui",
    "create_relationships_page",
    "_run_standalone",
]


if __name__ == "__main__":
    ft.app(target=_run_standalone)
