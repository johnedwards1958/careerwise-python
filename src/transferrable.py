"""
Compatibility module for Transferrable assessment.

Public interface is now split across:
- transferrable_data.py
- transferrable_logic.py
- transferrable_ui.py
"""

import flet as ft

from transferrable_data import QUESTIONS, DOMAINS, HIGHLY_TRANSFERABLE, MODERATELY_TRANSFERABLE, DEVELOPING
from transferrable_logic import TransferrableSkillsAssessment
from transferrable_ui import create_transferrable_assessment_ui, create_transferrable_page, _run_standalone

__all__ = [
    "QUESTIONS",
    "DOMAINS",
    "HIGHLY_TRANSFERABLE",
    "MODERATELY_TRANSFERABLE",
    "DEVELOPING",
    "TransferrableSkillsAssessment",
    "create_transferrable_assessment_ui",
    "create_transferrable_page",
    "_run_standalone",
]


if __name__ == "__main__":
    ft.app(target=_run_standalone)
