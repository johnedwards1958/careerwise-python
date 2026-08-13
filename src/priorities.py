"""
Compatibility module for Priorities assessment.

Public interface is now split across:
- priorities_data.py
- priorities_logic.py
- priorities_ui.py
"""

import flet as ft

from priorities_data import ANCHORS
from priorities_logic import PrioritiesAssessment
from priorities_ui import create_priorities_assessment_ui, create_priorities_page, _run_standalone

__all__ = [
    "ANCHORS",
    "PrioritiesAssessment",
    "create_priorities_assessment_ui",
    "create_priorities_page",
    "_run_standalone",
]


if __name__ == "__main__":
    ft.app(target=_run_standalone)
