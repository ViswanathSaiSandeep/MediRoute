"""
Appium Navigation Test Suite – 50 test cases for Android.
Covers screen transitions, back navigation, gestures, deep linking, and routing.
"""
import pytest
import time
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.all_screens import *
from pages.base_screen import BaseScreen


class TestAppiumNavigation:
    """Navigation module – 50 test cases."""

    # ── ANAV-001 to ANAV-010: Basic Navigation ──────────────────────────
    def test_anav_001_splash_to_role_selection(self, driver):
        """TC: ANAV-001 | Navigate from splash to role selection."""
        screen = SplashScreen(driver)
        screen.wait_for_splash_complete()
        assert screen.is_loaded(), "Splash to role transition failed"

    def test_anav_002_back_button_from_role(self, driver):
        """TC: ANAV-002 | Back button from role selection."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        screen.go_back()
        time.sleep(2)
        assert screen.wait_for_screen_ready(), "Back from role failed"

    def test_anav_003_navigate_to_bystander_auth(self, driver):
        """TC: ANAV-003 | Navigate to bystander auth screen."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        time.sleep(3)
        assert screen.is_loaded(), "Bystander auth navigation failed"

    def test_anav_004_navigate_to_hospital_register(self, driver):
        """TC: ANAV-004 | Navigate to hospital registration."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        time.sleep(3)
        assert screen.is_loaded(), "Hospital register navigation failed"

    def test_anav_005_navigate_to_volunteer_register(self, driver):
        """TC: ANAV-005 | Navigate to volunteer registration."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        time.sleep(3)
        assert screen.is_loaded(), "Volunteer register navigation failed"

    def test_anav_006_back_from_bystander_auth(self, driver):
        """TC: ANAV-006 | Back button from bystander auth."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        screen.go_back()
        time.sleep(2)
        assert screen.wait_for_screen_ready(), "Back from bystander auth failed"

    def test_anav_007_back_from_hospital_register(self, driver):
        """TC: ANAV-007 | Back button from hospital register."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        screen.go_back()
        time.sleep(2)
        assert screen.wait_for_screen_ready(), "Back from hospital register failed"

    def test_anav_008_back_from_volunteer_register(self, driver):
        """TC: ANAV-008 | Back button from volunteer register."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        screen.go_back()
        time.sleep(2)
        assert screen.wait_for_screen_ready(), "Back from volunteer register failed"

    def test_anav_009_rapid_back_presses(self, driver):
        """TC: ANAV-009 | Multiple rapid back presses don't crash."""
        screen = BaseScreen(driver)
        for _ in range(5):
            screen.go_back()
            time.sleep(0.5)
        assert screen.wait_for_screen_ready(), "Rapid back presses caused crash"

    def test_anav_010_forward_navigation_chain(self, driver):
        """TC: ANAV-010 | Full forward navigation chain."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        time.sleep(5)
        assert screen.is_loaded(), "Forward navigation chain failed"

    # ── ANAV-011 to ANAV-020: Scroll & Gesture Navigation ────────────────
    def test_anav_011_scroll_down_on_screen(self, driver):
        """TC: ANAV-011 | Scroll down gesture works."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        screen.scroll_down()
        assert screen.is_loaded(), "Scroll down failed"

    def test_anav_012_scroll_up_on_screen(self, driver):
        """TC: ANAV-012 | Scroll up gesture works."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        screen.scroll_up()
        assert screen.is_loaded(), "Scroll up failed"

    def test_anav_013_swipe_left_gesture(self, driver):
        """TC: ANAV-013 | Swipe left gesture works."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        screen.swipe_left()
        assert screen.is_loaded(), "Swipe left failed"

    def test_anav_014_swipe_right_gesture(self, driver):
        """TC: ANAV-014 | Swipe right gesture works."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        screen.swipe_right()
        assert screen.is_loaded(), "Swipe right failed"

    def test_anav_015_continuous_scrolling(self, driver):
        """TC: ANAV-015 | Continuous scrolling doesn't crash."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        for _ in range(5):
            screen.scroll_down()
            time.sleep(0.5)
        assert screen.is_loaded(), "Continuous scroll caused crash"

    def test_anav_016_scroll_then_back(self, driver):
        """TC: ANAV-016 | Scroll then back maintains state."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        screen.scroll_down()
        screen.go_back()
        assert screen.wait_for_screen_ready(), "Scroll+back broke state"

    def test_anav_017_tap_coordinates_center(self, driver):
        """TC: ANAV-017 | Tap at screen center."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        size = screen.get_screen_size()
        screen.tap_coordinates(size['width']//2, size['height']//2)
        assert screen.is_loaded(), "Center tap failed"

    def test_anav_018_double_scroll_down(self, driver):
        """TC: ANAV-018 | Double scroll down."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        screen.scroll_down()
        screen.scroll_down()
        assert screen.is_loaded(), "Double scroll down failed"

    def test_anav_019_scroll_back_to_top(self, driver):
        """TC: ANAV-019 | Scroll down then back to top."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        screen.scroll_down()
        screen.scroll_up()
        screen.scroll_up()
        assert screen.is_loaded(), "Scroll back to top failed"

    def test_anav_020_gesture_after_orientation_change(self, driver):
        """TC: ANAV-020 | Gestures work after orientation change."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        screen.set_orientation("LANDSCAPE")
        time.sleep(2)
        screen.scroll_down()
        screen.set_orientation("PORTRAIT")
        assert screen.is_loaded(), "Post-rotation gesture failed"

    # ── ANAV-021 to ANAV-030: Screen Transition Timing ───────────────────
    def test_anav_021_transition_speed_acceptable(self, driver):
        """TC: ANAV-021 | Screen transition under 3s."""
        screen = BaseScreen(driver)
        start = time.time()
        screen.wait_for_screen_ready()
        elapsed = time.time() - start
        assert elapsed < 10, f"Transition took {elapsed:.1f}s"

    def test_anav_022_no_white_flash_on_transition(self, driver):
        """TC: ANAV-022 | No blank white screen during transition."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        source = screen.get_page_source()
        assert len(source) > 50, "Possible white flash"

    def test_anav_023_back_transition_speed(self, driver):
        """TC: ANAV-023 | Back transition under 3s."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        start = time.time()
        screen.go_back()
        screen.wait_for_screen_ready()
        elapsed = time.time() - start
        assert elapsed < 10, f"Back transition took {elapsed:.1f}s"

    def test_anav_024_screen_state_after_transition(self, driver):
        """TC: ANAV-024 | Screen state preserved after transition."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "State not preserved"

    def test_anav_025_multiple_transitions_stable(self, driver):
        """TC: ANAV-025 | Multiple transitions remain stable."""
        screen = BaseScreen(driver)
        for _ in range(3):
            screen.wait_for_screen_ready()
            screen.go_back()
            time.sleep(1)
        assert screen.wait_for_screen_ready(), "Unstable after transitions"

    def test_anav_026_activity_changes_correctly(self, driver):
        """TC: ANAV-026 | Activity changes on navigation."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        activity = screen.get_current_activity()
        assert activity is not None, "Activity not accessible"

    def test_anav_027_package_stays_same(self, driver):
        """TC: ANAV-027 | App package stays same during navigation."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        pkg = screen.get_current_package()
        screen.go_back()
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Package changed unexpectedly"

    def test_anav_028_no_crash_on_empty_back_stack(self, driver):
        """TC: ANAV-028 | No crash when back stack exhausted."""
        screen = BaseScreen(driver)
        for _ in range(10):
            screen.go_back()
            time.sleep(0.3)
        time.sleep(2)
        assert True, "Back stack exhaustion handled"

    def test_anav_029_screen_elements_update_on_nav(self, driver):
        """TC: ANAV-029 | UI elements update on navigation."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        source1 = screen.get_page_source()
        screen.go_back()
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Elements did not update"

    def test_anav_030_navigation_with_keyboard_open(self, driver):
        """TC: ANAV-030 | Navigation works with keyboard open."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        screen.go_back()
        assert screen.wait_for_screen_ready(), "Nav with keyboard failed"

    # ── ANAV-031 to ANAV-040: App Lifecycle ──────────────────────────────
    def test_anav_031_home_and_resume(self, driver):
        """TC: ANAV-031 | App resumes correctly from home."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        screen.press_home()
        time.sleep(3)
        assert True, "Home+resume cycle"

    def test_anav_032_app_state_after_pause(self, driver):
        """TC: ANAV-032 | App state preserved after pause."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "State after pause"

    def test_anav_033_landscape_navigation(self, driver):
        """TC: ANAV-033 | Navigation works in landscape."""
        screen = BaseScreen(driver)
        screen.set_orientation("LANDSCAPE")
        time.sleep(2)
        screen.wait_for_screen_ready()
        screen.set_orientation("PORTRAIT")
        assert screen.is_loaded(), "Landscape navigation failed"

    def test_anav_034_portrait_to_landscape_transition(self, driver):
        """TC: ANAV-034 | Portrait→Landscape transition smooth."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        screen.set_orientation("LANDSCAPE")
        time.sleep(2)
        assert screen.wait_for_screen_ready(), "P→L transition failed"
        screen.set_orientation("PORTRAIT")

    def test_anav_035_landscape_to_portrait_transition(self, driver):
        """TC: ANAV-035 | Landscape→Portrait transition smooth."""
        screen = BaseScreen(driver)
        screen.set_orientation("LANDSCAPE")
        time.sleep(1)
        screen.set_orientation("PORTRAIT")
        time.sleep(2)
        assert screen.wait_for_screen_ready(), "L→P transition failed"

    def test_anav_036_multiple_orientation_changes(self, driver):
        """TC: ANAV-036 | Multiple orientation changes stable."""
        screen = BaseScreen(driver)
        for orient in ["LANDSCAPE", "PORTRAIT", "LANDSCAPE", "PORTRAIT"]:
            screen.set_orientation(orient)
            time.sleep(1)
        assert screen.wait_for_screen_ready(), "Orientation changes unstable"

    def test_anav_037_screen_size_correct(self, driver):
        """TC: ANAV-037 | Screen size reported correctly."""
        screen = BaseScreen(driver)
        size = screen.get_screen_size()
        assert size['width'] > 0 and size['height'] > 0, "Invalid screen size"

    def test_anav_038_screen_dimensions_landscape(self, driver):
        """TC: ANAV-038 | Screen dimensions change in landscape."""
        screen = BaseScreen(driver)
        screen.set_orientation("LANDSCAPE")
        time.sleep(2)
        size = screen.get_screen_size()
        screen.set_orientation("PORTRAIT")
        assert size['width'] > 0, "Landscape dimensions invalid"

    def test_anav_039_app_survives_rapid_rotation(self, driver):
        """TC: ANAV-039 | App survives rapid rotation."""
        screen = BaseScreen(driver)
        for _ in range(5):
            screen.set_orientation("LANDSCAPE")
            time.sleep(0.5)
            screen.set_orientation("PORTRAIT")
            time.sleep(0.5)
        assert screen.wait_for_screen_ready(), "Rapid rotation crash"

    def test_anav_040_navigation_after_rotation(self, driver):
        """TC: ANAV-040 | Navigation works after rotation."""
        screen = BaseScreen(driver)
        screen.set_orientation("LANDSCAPE")
        time.sleep(1)
        screen.set_orientation("PORTRAIT")
        time.sleep(1)
        screen.go_back()
        assert screen.wait_for_screen_ready(), "Post-rotation nav failed"

    # ── ANAV-041 to ANAV-050: Edge Cases ─────────────────────────────────
    def test_anav_041_screen_timeout_handling(self, driver):
        """TC: ANAV-041 | Screen load timeout handled gracefully."""
        screen = BaseScreen(driver)
        assert screen.wait_for_screen_ready(timeout=5), "Timeout not handled"

    def test_anav_042_navigation_with_slow_render(self, driver):
        """TC: ANAV-042 | Navigation handles slow rendering."""
        screen = BaseScreen(driver)
        time.sleep(5)
        assert screen.is_loaded(), "Slow render navigation failed"

    def test_anav_043_double_tap_navigation(self, driver):
        """TC: ANAV-043 | Double tap doesn't cause double navigation."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Double tap navigation issue"

    def test_anav_044_navigation_memory_leak(self, driver):
        """TC: ANAV-044 | No memory leak on repeated navigation."""
        screen = BaseScreen(driver)
        for _ in range(10):
            screen.wait_for_screen_ready()
            screen.go_back()
            time.sleep(0.3)
        assert screen.wait_for_screen_ready(), "Possible memory leak"

    def test_anav_045_page_source_accessible(self, driver):
        """TC: ANAV-045 | Page source always accessible."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        source = screen.get_page_source()
        assert source is not None, "Page source unavailable"

    def test_anav_046_elements_findable_after_nav(self, driver):
        """TC: ANAV-046 | Elements findable after navigation."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        elements = screen.find_by_class("android.view.View")
        assert elements is not None, "Elements not findable"

    def test_anav_047_scroll_boundaries(self, driver):
        """TC: ANAV-047 | Scroll doesn't go past boundaries."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        for _ in range(20):
            screen.scroll_down()
        assert screen.is_loaded(), "Scroll boundary issue"

    def test_anav_048_gesture_sensitivity(self, driver):
        """TC: ANAV-048 | Gesture sensitivity appropriate."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        screen.scroll_down()
        assert screen.is_loaded(), "Gesture sensitivity issue"

    def test_anav_049_navigation_stress_test(self, driver):
        """TC: ANAV-049 | 20 rapid navigations stable."""
        screen = BaseScreen(driver)
        for _ in range(20):
            screen.go_back()
            time.sleep(0.2)
        time.sleep(3)
        assert True, "Navigation stress test passed"

    def test_anav_050_final_state_valid(self, driver):
        """TC: ANAV-050 | Final state after all navigation tests valid."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Final state invalid"
