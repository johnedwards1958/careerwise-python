"""
Compatibility module for Learning Preferences assessment.

Public interface is now split across:
- learning_data.py
- learning_logic.py
- learning_ui.py
"""

import flet as ft

from learning_data import QUESTIONS, STYLES
from learning_logic import LearningPreferenceAssessment
from learning_ui import LearningPreferenceUI, create_learning_preference_assessment_ui, _run_standalone

__all__ = [
    "STYLES",
    "QUESTIONS",
    "LearningPreferenceAssessment",
    "LearningPreferenceUI",
    "create_learning_preference_assessment_ui",
    "_run_standalone",
]


if __name__ == "__main__":
    ft.app(target=_run_standalone)
