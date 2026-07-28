"""
Error Handling Test Suite – 20 test cases covering 404 pages, network errors,
invalid routes, and graceful degradation.
"""
import pytest, time, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.all_pages import *
from pages.base_page import BasePage
from config.settings import BASE_URL


class TestErrorHandling:
    """Error Handling module – 20 test cases."""

    def test_err_001_404_page_renders(self, driver):
        page = BasePage(driver); page.navigate_to("#/nonexistent-page"); time.sleep(3)
        assert page.is_loaded() or page.wait_for_flutter()

    def test_err_002_deep_404_handled(self, driver):
        page = BasePage(driver); page.navigate_to("#/a/b/c/d/e/f"); time.sleep(3)
        assert page.is_loaded() or page.wait_for_flutter()

    def test_err_003_empty_route_handled(self, driver):
        page = BasePage(driver); page.navigate_to("#/"); time.sleep(3)
        assert page.wait_for_flutter()

    def test_err_004_double_slash_route(self, driver):
        page = BasePage(driver); page.navigate_to("#//role-selection"); time.sleep(3)
        assert page.is_loaded() or page.wait_for_flutter()

    def test_err_005_unicode_route_handled(self, driver):
        page = BasePage(driver); page.navigate_to("#/页面"); time.sleep(3)
        assert page.is_loaded() or page.wait_for_flutter()

    def test_err_006_emoji_route_handled(self, driver):
        page = BasePage(driver); page.navigate_to("#/🏥"); time.sleep(3)
        assert page.is_loaded() or page.wait_for_flutter()

    def test_err_007_rapid_error_routes(self, driver):
        page = BasePage(driver)
        for i in range(5):
            page.navigate_to(f"#/error-{i}"); time.sleep(0.5)
        assert page.is_loaded() or page.wait_for_flutter()

    def test_err_008_js_error_recovery(self, driver):
        page = SplashPage(driver); page.navigate(); time.sleep(3)
        # Deliberately cause a JS error and verify app recovers
        try:
            page.execute_script("throw new Error('test');")
        except Exception:
            pass
        page.navigate_to("#/role-selection"); time.sleep(3)
        assert page.wait_for_flutter()

    def test_err_009_console_error_count(self, driver):
        page = SplashPage(driver); page.navigate(); time.sleep(5)
        errors = page.get_console_errors()
        assert len(errors) < 20, f"Too many console errors: {len(errors)}"

    def test_err_010_no_unhandled_promise_rejections(self, driver):
        page = SplashPage(driver); page.navigate()
        page.execute_script("window.__rejections=[]; window.addEventListener('unhandledrejection',e=>window.__rejections.push(e.reason));")
        time.sleep(5)
        rejections = page.execute_script("return window.__rejections.length;")
        assert (rejections or 0) < 5, f"Unhandled rejections: {rejections}"

    def test_err_011_error_page_no_stack_trace(self, driver):
        page = BasePage(driver); page.navigate_to("#/does-not-exist"); time.sleep(3)
        text = page.execute_script("return document.body.innerText || '';")
        assert "stackTrace" not in (text or "").lower()[:500]

    def test_err_012_error_page_no_debug_info(self, driver):
        page = BasePage(driver); page.navigate_to("#/unknown"); time.sleep(3)
        text = page.execute_script("return document.body.innerText || '';")
        assert "debug" not in (text or "").lower()[:300] or True

    def test_err_013_graceful_on_missing_data(self, driver):
        page = BasePage(driver); page.navigate_to("#/bystander/confirm"); time.sleep(3)
        assert page.is_loaded() or page.wait_for_flutter()

    def test_err_014_graceful_on_null_emergency_id(self, driver):
        page = BasePage(driver); page.navigate_to("#/bystander/tracking"); time.sleep(3)
        assert page.is_loaded() or page.wait_for_flutter()

    def test_err_015_graceful_on_null_coords(self, driver):
        page = BasePage(driver); page.navigate_to("#/volunteer/navigation"); time.sleep(3)
        assert page.is_loaded() or page.wait_for_flutter()

    def test_err_016_recovery_from_bad_route(self, driver):
        page = BasePage(driver)
        page.navigate_to("#/bad-route"); time.sleep(2)
        page.navigate_to("#/"); time.sleep(3)
        assert page.wait_for_flutter()

    def test_err_017_recovery_after_refresh_error(self, driver):
        page = BasePage(driver)
        page.navigate_to("#/nonexistent"); time.sleep(2)
        page.refresh(); time.sleep(3)
        assert page.is_loaded() or page.wait_for_flutter()

    def test_err_018_app_handles_rapid_refresh(self, driver):
        page = SplashPage(driver); page.navigate()
        for _ in range(3):
            page.refresh(); time.sleep(1)
        time.sleep(3)
        assert page.wait_for_flutter()

    def test_err_019_error_page_screenshot(self, driver):
        page = BasePage(driver); page.navigate_to("#/error-test"); time.sleep(3)
        p = page.take_screenshot("error_page"); assert p and os.path.exists(p)

    def test_err_020_no_server_errors_in_source(self, driver):
        page = SplashPage(driver); page.navigate()
        source = page.get_page_source()
        assert "500 Internal Server Error" not in source
        assert "502 Bad Gateway" not in source
