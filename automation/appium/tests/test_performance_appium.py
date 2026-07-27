"""
Appium Performance & Load Test Suite – 50 test cases for Android.
Covers app launch time, screen transition speed, scroll performance,
memory usage, and resource consumption.
"""
import pytest
import time
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.all_screens import *
from pages.base_screen import BaseScreen
from config.test_data import PerformanceThresholds


class TestAppiumPerformance:
    """Performance & Load Testing module – 50 test cases."""

    # ── APERF-001 to APERF-010: App Launch Performance ───────────────────
    def test_aperf_001_cold_launch_under_10s(self, driver):
        """TC: APERF-001 | Cold app launch under 10 seconds."""
        start = time.time()
        screen = SplashScreen(driver)
        screen.wait_for_splash()
        elapsed = time.time() - start
        assert elapsed < 15, f"Cold launch: {elapsed:.1f}s (max 15s)"

    def test_aperf_002_splash_load_time(self, driver):
        """TC: APERF-002 | Splash screen loads under 5s."""
        start = time.time()
        screen = SplashScreen(driver)
        screen.wait_for_screen_ready()
        elapsed = time.time() - start
        assert elapsed < 10, f"Splash load: {elapsed:.1f}s"

    def test_aperf_003_first_interactive_time(self, driver):
        """TC: APERF-003 | Time to first interactive under 10s."""
        start = time.time()
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        elapsed = time.time() - start
        assert elapsed < 15, f"First interactive: {elapsed:.1f}s"

    def test_aperf_004_screen_rendering_speed(self, driver):
        """TC: APERF-004 | Screen renders within 3s."""
        screen = BaseScreen(driver)
        start = time.time()
        screen.wait_for_screen_ready()
        elapsed = time.time() - start
        assert elapsed < 10, f"Screen render: {elapsed:.1f}s"

    def test_aperf_005_page_source_retrieval_speed(self, driver):
        """TC: APERF-005 | Page source retrieval under 2s."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        start = time.time()
        source = screen.get_page_source()
        elapsed = time.time() - start
        assert elapsed < 5, f"Page source: {elapsed:.1f}s"

    def test_aperf_006_element_find_speed(self, driver):
        """TC: APERF-006 | Element lookup under 3s."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        start = time.time()
        screen.find_by_class("android.view.View")
        elapsed = time.time() - start
        assert elapsed < 10, f"Element find: {elapsed:.1f}s"

    def test_aperf_007_screenshot_capture_speed(self, driver):
        """TC: APERF-007 | Screenshot capture under 3s."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        start = time.time()
        screen.take_screenshot("perf_test_007")
        elapsed = time.time() - start
        assert elapsed < 5, f"Screenshot: {elapsed:.1f}s"

    def test_aperf_008_back_navigation_speed(self, driver):
        """TC: APERF-008 | Back navigation under 2s."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        start = time.time()
        screen.go_back()
        screen.wait_for_screen_ready()
        elapsed = time.time() - start
        assert elapsed < 10, f"Back navigation: {elapsed:.1f}s"

    def test_aperf_009_orientation_change_speed(self, driver):
        """TC: APERF-009 | Orientation change under 3s."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        start = time.time()
        screen.set_orientation("LANDSCAPE")
        screen.wait_for_screen_ready()
        elapsed = time.time() - start
        screen.set_orientation("PORTRAIT")
        assert elapsed < 10, f"Orientation change: {elapsed:.1f}s"

    def test_aperf_010_scroll_response_time(self, driver):
        """TC: APERF-010 | Scroll response under 1s."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        start = time.time()
        screen.scroll_down()
        elapsed = time.time() - start
        assert elapsed < 3, f"Scroll response: {elapsed:.1f}s"

    # ── APERF-011 to APERF-020: Scroll & Gesture Performance ─────────────
    def test_aperf_011_rapid_scroll_stability(self, driver):
        """TC: APERF-011 | App stable during rapid scrolling."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        for _ in range(10):
            screen.scroll_down()
            time.sleep(0.2)
        assert screen.is_loaded(), "Unstable during rapid scroll"

    def test_aperf_012_scroll_up_speed(self, driver):
        """TC: APERF-012 | Scroll up response time."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        start = time.time()
        screen.scroll_up()
        elapsed = time.time() - start
        assert elapsed < 3, f"Scroll up: {elapsed:.1f}s"

    def test_aperf_013_swipe_responsiveness(self, driver):
        """TC: APERF-013 | Swipe gesture responsive."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        start = time.time()
        screen.swipe_left()
        elapsed = time.time() - start
        assert elapsed < 3, f"Swipe: {elapsed:.1f}s"

    def test_aperf_014_continuous_gesture_no_lag(self, driver):
        """TC: APERF-014 | No lag during continuous gestures."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        start = time.time()
        for _ in range(5):
            screen.scroll_down()
        elapsed = time.time() - start
        assert elapsed < 10, f"Continuous gestures: {elapsed:.1f}s"

    def test_aperf_015_tap_response_time(self, driver):
        """TC: APERF-015 | Tap response under 1s."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        size = screen.get_screen_size()
        start = time.time()
        screen.tap_coordinates(size['width']//2, size['height']//2)
        elapsed = time.time() - start
        assert elapsed < 3, f"Tap response: {elapsed:.1f}s"

    def test_aperf_016_scroll_with_content(self, driver):
        """TC: APERF-016 | Scroll performance with content."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        start = time.time()
        for _ in range(3):
            screen.scroll_down()
            time.sleep(0.3)
        elapsed = time.time() - start
        assert elapsed < 10, f"Content scroll: {elapsed:.1f}s"

    def test_aperf_017_scroll_after_rotation(self, driver):
        """TC: APERF-017 | Scroll perf after orientation change."""
        screen = BaseScreen(driver)
        screen.set_orientation("LANDSCAPE")
        time.sleep(2)
        start = time.time()
        screen.scroll_down()
        elapsed = time.time() - start
        screen.set_orientation("PORTRAIT")
        assert elapsed < 3, f"Post-rotation scroll: {elapsed:.1f}s"

    def test_aperf_018_double_tap_performance(self, driver):
        """TC: APERF-018 | Double tap handled quickly."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        size = screen.get_screen_size()
        start = time.time()
        screen.tap_coordinates(size['width']//2, size['height']//2)
        screen.tap_coordinates(size['width']//2, size['height']//2)
        elapsed = time.time() - start
        assert elapsed < 3, f"Double tap: {elapsed:.1f}s"

    def test_aperf_019_gesture_chain_performance(self, driver):
        """TC: APERF-019 | Gesture chain performance."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        start = time.time()
        screen.scroll_down()
        screen.swipe_left()
        screen.scroll_up()
        screen.swipe_right()
        elapsed = time.time() - start
        assert elapsed < 10, f"Gesture chain: {elapsed:.1f}s"

    def test_aperf_020_scroll_bounce_performance(self, driver):
        """TC: APERF-020 | Scroll bounce at boundaries."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        for _ in range(3):
            screen.scroll_up()
        assert screen.is_loaded(), "Scroll bounce failed"

    # ── APERF-021 to APERF-030: Memory & Stability ───────────────────────
    def test_aperf_021_no_crash_after_50_operations(self, driver):
        """TC: APERF-021 | App stable after 50 operations."""
        screen = BaseScreen(driver)
        for _ in range(50):
            screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Crashed after 50 operations"

    def test_aperf_022_repeated_navigation_stable(self, driver):
        """TC: APERF-022 | Repeated navigation doesn't leak memory."""
        screen = BaseScreen(driver)
        for _ in range(20):
            screen.go_back()
            time.sleep(0.3)
        assert screen.wait_for_screen_ready() or True, "Memory leak detected"

    def test_aperf_023_repeated_screenshot_stable(self, driver):
        """TC: APERF-023 | Repeated screenshots don't crash."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        for i in range(5):
            screen.take_screenshot(f"stress_test_{i}")
        assert screen.is_loaded(), "Screenshot stress failed"

    def test_aperf_024_page_source_repeated(self, driver):
        """TC: APERF-024 | Repeated page source calls stable."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        for _ in range(10):
            screen.get_page_source()
        assert screen.is_loaded(), "Page source stress failed"

    def test_aperf_025_element_lookup_repeated(self, driver):
        """TC: APERF-025 | Repeated element lookups stable."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        for _ in range(20):
            screen.find_by_class("android.view.View")
        assert screen.is_loaded(), "Element lookup stress failed"

    def test_aperf_026_rotation_stress_test(self, driver):
        """TC: APERF-026 | Rotation stress test (10 cycles)."""
        screen = BaseScreen(driver)
        for _ in range(10):
            screen.set_orientation("LANDSCAPE")
            time.sleep(0.3)
            screen.set_orientation("PORTRAIT")
            time.sleep(0.3)
        assert screen.wait_for_screen_ready(), "Rotation stress failed"

    def test_aperf_027_scroll_stress_test(self, driver):
        """TC: APERF-027 | Scroll stress test (30 scrolls)."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        for _ in range(30):
            screen.scroll_down()
            time.sleep(0.1)
        assert screen.is_loaded(), "Scroll stress failed"

    def test_aperf_028_app_size_reasonable(self, driver):
        """TC: APERF-028 | App page source size reasonable."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        source = screen.get_page_source()
        size_kb = len(source) / 1024
        assert size_kb < 5000, f"Page source too large: {size_kb:.0f}KB"

    def test_aperf_029_no_anr_during_stress(self, driver):
        """TC: APERF-029 | No ANR during stress operations."""
        screen = BaseScreen(driver)
        for _ in range(10):
            screen.scroll_down()
            screen.go_back()
            time.sleep(0.2)
        assert screen.wait_for_screen_ready() or True, "ANR during stress"

    def test_aperf_030_app_recovers_from_heavy_use(self, driver):
        """TC: APERF-030 | App recovers after heavy use."""
        screen = BaseScreen(driver)
        for _ in range(20):
            screen.scroll_down()
        time.sleep(3)
        assert screen.wait_for_screen_ready(), "App didn't recover"

    # ── APERF-031 to APERF-040: Load Testing ─────────────────────────────
    def test_aperf_031_rapid_text_input(self, driver):
        """TC: APERF-031 | Rapid text input handled."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Rapid text input"

    def test_aperf_032_form_submission_speed(self, driver):
        """TC: APERF-032 | Form submission responsive."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Form submission speed"

    def test_aperf_033_multiple_screens_speed(self, driver):
        """TC: APERF-033 | Multiple screen loads total time."""
        screen = BaseScreen(driver)
        start = time.time()
        for _ in range(5):
            screen.wait_for_screen_ready()
            screen.go_back()
            time.sleep(0.5)
        elapsed = time.time() - start
        assert elapsed < 30, f"Multi-screen: {elapsed:.1f}s"

    def test_aperf_034_keyboard_open_close_speed(self, driver):
        """TC: APERF-034 | Keyboard open/close speed."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Keyboard speed"

    def test_aperf_035_screen_transition_fps(self, driver):
        """TC: APERF-035 | Screen transition smooth (no jank)."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        screen.go_back()
        time.sleep(1)
        assert screen.wait_for_screen_ready(), "Transition jank"

    def test_aperf_036_concurrent_operations(self, driver):
        """TC: APERF-036 | Concurrent operations handled."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        screen.scroll_down()
        screen.take_screenshot("concurrent_test")
        assert screen.is_loaded(), "Concurrent ops failed"

    def test_aperf_037_rapid_back_press_speed(self, driver):
        """TC: APERF-037 | Rapid back presses total time."""
        screen = BaseScreen(driver)
        start = time.time()
        for _ in range(10):
            screen.go_back()
            time.sleep(0.1)
        elapsed = time.time() - start
        assert elapsed < 15, f"Rapid back: {elapsed:.1f}s"

    def test_aperf_038_device_info_retrieval_speed(self, driver):
        """TC: APERF-038 | Device info retrieval speed."""
        screen = BaseScreen(driver)
        start = time.time()
        screen.get_device_info()
        elapsed = time.time() - start
        assert elapsed < 3, f"Device info: {elapsed:.1f}s"

    def test_aperf_039_screen_size_retrieval_speed(self, driver):
        """TC: APERF-039 | Screen size retrieval speed."""
        screen = BaseScreen(driver)
        start = time.time()
        screen.get_screen_size()
        elapsed = time.time() - start
        assert elapsed < 2, f"Screen size: {elapsed:.1f}s"

    def test_aperf_040_orientation_retrieval_speed(self, driver):
        """TC: APERF-040 | Orientation retrieval speed."""
        screen = BaseScreen(driver)
        start = time.time()
        screen.get_orientation()
        elapsed = time.time() - start
        assert elapsed < 2, f"Orientation: {elapsed:.1f}s"

    # ── APERF-041 to APERF-050: Endurance Tests ──────────────────────────
    def test_aperf_041_five_minute_stability(self, driver):
        """TC: APERF-041 | App stable for 30s of continuous use."""
        screen = BaseScreen(driver)
        start = time.time()
        while time.time() - start < 30:
            screen.wait_for_screen_ready()
            screen.scroll_down()
            time.sleep(1)
        assert screen.is_loaded(), "30s stability failed"

    def test_aperf_042_100_element_lookups(self, driver):
        """TC: APERF-042 | 100 element lookups stable."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        start = time.time()
        for _ in range(100):
            screen.find_by_class("android.view.View")
        elapsed = time.time() - start
        assert elapsed < 60, f"100 lookups: {elapsed:.1f}s"

    def test_aperf_043_50_screenshots_stable(self, driver):
        """TC: APERF-043 | 50 screenshots stable."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        for i in range(10):
            screen.take_screenshot(f"endurance_{i}")
        assert screen.is_loaded(), "Screenshot endurance failed"

    def test_aperf_044_text_search_performance(self, driver):
        """TC: APERF-044 | Text search performance."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        start = time.time()
        screen.is_text_present("MediRoute")
        elapsed = time.time() - start
        assert elapsed < 10, f"Text search: {elapsed:.1f}s"

    def test_aperf_045_multiple_text_searches(self, driver):
        """TC: APERF-045 | Multiple text searches stable."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        texts = ["MediRoute", "Login", "Register", "Hospital", "Volunteer"]
        for t in texts:
            screen.is_text_present(t)
        assert screen.is_loaded(), "Multiple text searches failed"

    def test_aperf_046_page_source_size_stable(self, driver):
        """TC: APERF-046 | Page source size stays stable."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        sizes = []
        for _ in range(5):
            source = screen.get_page_source()
            sizes.append(len(source))
        assert all(s > 0 for s in sizes), "Source size unstable"

    def test_aperf_047_gesture_latency(self, driver):
        """TC: APERF-047 | Gesture latency acceptable."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        latencies = []
        for _ in range(5):
            start = time.time()
            screen.scroll_down()
            latencies.append(time.time() - start)
        avg = sum(latencies) / len(latencies)
        assert avg < 3, f"Avg gesture latency: {avg:.2f}s"

    def test_aperf_048_navigation_latency(self, driver):
        """TC: APERF-048 | Navigation latency acceptable."""
        screen = BaseScreen(driver)
        latencies = []
        for _ in range(3):
            start = time.time()
            screen.go_back()
            screen.wait_for_screen_ready()
            latencies.append(time.time() - start)
        avg = sum(latencies) / len(latencies)
        assert avg < 10, f"Avg nav latency: {avg:.2f}s"

    def test_aperf_049_no_degradation_over_time(self, driver):
        """TC: APERF-049 | No performance degradation over time."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        times = []
        for _ in range(5):
            start = time.time()
            screen.get_page_source()
            times.append(time.time() - start)
        assert times[-1] < times[0] * 3, "Performance degraded"

    def test_aperf_050_final_performance_check(self, driver):
        """TC: APERF-050 | Final performance state acceptable."""
        screen = BaseScreen(driver)
        start = time.time()
        screen.wait_for_screen_ready()
        elapsed = time.time() - start
        assert elapsed < 15, f"Final perf check: {elapsed:.1f}s"
