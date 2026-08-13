"""
Compatibility module for Teams assessment.

Public interface is now split across:
- teams_data.py
- teams_logic.py
- teams_ui.py
"""

import flet as ft

from teams_data import ROLES, SECTIONS, ROLE_MAPPING, POINTS_PER_SECTION
from teams_logic import TeamsAssessment
from teams_ui import create_teams_assessment_ui, _run_standalone

__all__ = [
    "ROLES",
    "SECTIONS",
    "ROLE_MAPPING",
    "POINTS_PER_SECTION",
    "TeamsAssessment",
    "create_teams_assessment_ui",
    "_run_standalone",
]


if __name__ == "__main__":
    ft.app(target=_run_standalone)
