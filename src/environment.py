"""
Compatibility module for Preferred Work Environment assessment.

Public interface is now split across:
- environment_data.py
- environment_logic.py
- environment_ui.py
"""

import flet as ft

from environment_data import FACTORS, PROFILES, REFLECTION_PROMPTS
from environment_logic import EnvironmentAssessment
from environment_ui import create_environment_assessment_ui, create_environment_page, _run_standalone

__all__ = [
    "FACTORS",
    "PROFILES",
    "REFLECTION_PROMPTS",
    "EnvironmentAssessment",
    "create_environment_assessment_ui",
    "create_environment_page",
    "_run_standalone",
]


if __name__ == "__main__":
    ft.app(target=_run_standalone)
