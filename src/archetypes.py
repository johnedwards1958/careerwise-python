"""
Compatibility module for Influence Archetypes assessment.

Public interface is now split across:
- archetypes_data.py
- archetypes_logic.py
- archetypes_ui.py
"""

import flet as ft

from archetypes_data import ARCHETYPE_INFO, CLUSTERS, STATEMENTS
from archetypes_logic import InfluenceArchetypesAssessment
from archetypes_ui import create_influence_archetypes_assessment_ui, _run_standalone

__all__ = [
    "STATEMENTS",
    "CLUSTERS",
    "ARCHETYPE_INFO",
    "InfluenceArchetypesAssessment",
    "create_influence_archetypes_assessment_ui",
    "_run_standalone",
]


if __name__ == "__main__":
    ft.app(target=_run_standalone)
