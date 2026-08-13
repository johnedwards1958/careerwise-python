"""Regression tests for the responsive application shell."""

import sys
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from ui import (  # noqa: E402
    SMALL_SCREEN_BREAKPOINT,
    set_assessments_sidebar_visibility,
    should_hide_assessments_sidebar,
)


class VisibilityControl:
    def __init__(self):
        self.visible = True


class ResponsiveSidebarTests(unittest.TestCase):
    def test_sidebar_stays_visible_when_setting_is_disabled(self):
        self.assertFalse(should_hide_assessments_sidebar(False, 500))

    def test_sidebar_hides_below_breakpoint_when_setting_is_enabled(self):
        self.assertTrue(
            should_hide_assessments_sidebar(True, SMALL_SCREEN_BREAKPOINT - 1)
        )

    def test_sidebar_stays_visible_at_and_above_breakpoint(self):
        self.assertFalse(
            should_hide_assessments_sidebar(True, SMALL_SCREEN_BREAKPOINT)
        )
        self.assertFalse(
            should_hide_assessments_sidebar(True, SMALL_SCREEN_BREAKPOINT + 1)
        )

    def test_unknown_width_does_not_hide_sidebar(self):
        self.assertFalse(should_hide_assessments_sidebar(True, None))

    def test_sidebar_and_divider_visibility_change_together(self):
        sidebar = VisibilityControl()
        divider = VisibilityControl()
        temporary_show_button = VisibilityControl()
        temporary_show_button.visible = False

        changed = set_assessments_sidebar_visibility(
            sidebar,
            divider,
            True,
            SMALL_SCREEN_BREAKPOINT - 1,
            temporary_show_button,
        )
        self.assertTrue(changed)
        self.assertFalse(sidebar.visible)
        self.assertFalse(divider.visible)
        self.assertTrue(temporary_show_button.visible)

        changed = set_assessments_sidebar_visibility(
            sidebar,
            divider,
            False,
            SMALL_SCREEN_BREAKPOINT - 1,
            temporary_show_button,
        )
        self.assertTrue(changed)
        self.assertTrue(sidebar.visible)
        self.assertTrue(divider.visible)
        self.assertFalse(temporary_show_button.visible)

    def test_unchanged_responsive_controls_do_not_request_an_update(self):
        sidebar = VisibilityControl()
        divider = VisibilityControl()
        temporary_show_button = VisibilityControl()
        temporary_show_button.visible = False

        changed = set_assessments_sidebar_visibility(
            sidebar,
            divider,
            False,
            SMALL_SCREEN_BREAKPOINT - 1,
            temporary_show_button,
        )

        self.assertFalse(changed)


if __name__ == "__main__":
    unittest.main()
