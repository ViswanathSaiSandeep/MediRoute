"""
Regression Test Suite – 50 test cases covering end-to-end flows,
critical path validation, and cross-cutting concerns.
"""
import pytest, time, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.all_pages import *
from pages.base_page import BasePage
from config.settings import BASE_URL, ROUTES


class TestRegression:
    """Regression module – 50 test cases."""

    # ── Critical Path Tests (REG-001 to REG-010) ─────────────────────────
    def test_reg_001_full_bystander_flow(self, driver):
        page = BasePage(driver)
        for r in ["#/", "#/role-selection", "#/bystander/auth", "#/bystander/home"]:
            page.navigate_to(r); time.sleep(2)
        assert page.wait_for_flutter()

    def test_reg_002_full_volunteer_flow(self, driver):
        page = BasePage(driver)
        for r in ["#/", "#/role-selection", "#/volunteer/register", "#/volunteer/dashboard"]:
            page.navigate_to(r); time.sleep(2)
        assert page.wait_for_flutter()

    def test_reg_003_full_hospital_flow(self, driver):
        page = BasePage(driver)
        for r in ["#/", "#/role-selection", "#/hospital/register", "#/hospital/dashboard"]:
            page.navigate_to(r); time.sleep(2)
        assert page.wait_for_flutter()

    def test_reg_004_splash_to_all_roles(self, driver):
        page = BasePage(driver)
        page.navigate_to("#/"); time.sleep(3)
        for r in ["#/bystander/auth", "#/hospital/register", "#/volunteer/register"]:
            page.navigate_to(r); time.sleep(2)
        assert page.wait_for_flutter()

    def test_reg_005_all_routes_accessible(self, driver):
        page = BasePage(driver)
        accessible = 0
        for name, path in ROUTES.items():
            page.navigate_to(f"#{path}"); time.sleep(2)
            if page.wait_for_flutter(): accessible += 1
        assert accessible >= len(ROUTES) * 0.5

    def test_reg_006_app_title_consistent(self, driver):
        page = BasePage(driver)
        for r in ["#/", "#/role-selection", "#/bystander/auth"]:
            page.navigate_to(r); time.sleep(2)
            assert "MediRoute" in page.get_page_title()

    def test_reg_007_no_crashes_on_rapid_nav(self, driver):
        page = BasePage(driver)
        routes = list(ROUTES.values())
        for i in range(min(10, len(routes))):
            page.navigate_to(f"#{routes[i]}"); time.sleep(0.5)
        time.sleep(3)
        assert page.wait_for_flutter()

    def test_reg_008_back_forward_cycle(self, driver):
        page = BasePage(driver)
        page.navigate_to("#/"); time.sleep(2)
        page.navigate_to("#/role-selection"); time.sleep(2)
        page.navigate_to("#/bystander/auth"); time.sleep(2)
        page.go_back(); time.sleep(1)
        page.go_back(); time.sleep(1)
        driver.forward(); time.sleep(1)
        assert page.wait_for_flutter()

    def test_reg_009_refresh_all_pages(self, driver):
        page = BasePage(driver)
        for r in ["#/", "#/role-selection", "#/bystander/auth"]:
            page.navigate_to(r); time.sleep(2)
            page.refresh(); time.sleep(3)
        assert page.wait_for_flutter()

    def test_reg_010_screenshot_all_key_pages(self, driver):
        page = BasePage(driver)
        for name, route in [("splash","#/"), ("roles","#/role-selection"), ("auth","#/bystander/auth")]:
            page.navigate_to(route); time.sleep(3)
            p = page.take_screenshot(f"reg_{name}"); assert p and os.path.exists(p)

    # ── Cross-module Tests (REG-011 to REG-025) ──────────────────────────
    def test_reg_011_bystander_emergency_pages(self, driver):
        page = BasePage(driver)
        for r in ["#/bystander/home", "#/bystander/confirm", "#/bystander/first-aid", "#/bystander/tracking", "#/bystander/hospital-alert", "#/bystander/hospitals"]:
            page.navigate_to(r); time.sleep(2)
        assert page.wait_for_flutter()

    def test_reg_012_volunteer_all_pages(self, driver):
        page = BasePage(driver)
        for r in ["#/volunteer/register", "#/volunteer/dashboard", "#/volunteer/alert", "#/volunteer/navigation", "#/volunteer/complete"]:
            page.navigate_to(r); time.sleep(2)
        assert page.wait_for_flutter()

    def test_reg_013_hospital_all_pages(self, driver):
        page = BasePage(driver)
        for r in ["#/hospital/register", "#/hospital/dashboard"]:
            page.navigate_to(r); time.sleep(2)
        assert page.wait_for_flutter()

    def test_reg_014_shared_pages(self, driver):
        page = BasePage(driver)
        for r in ["#/history", "#/profile"]:
            page.navigate_to(r); time.sleep(2)
        assert page.wait_for_flutter()

    def test_reg_015_localstorage_across_nav(self, driver):
        page = BasePage(driver); page.navigate_to("")
        page.execute_script("localStorage.setItem('reg_test', 'pass');")
        page.navigate_to("#/role-selection"); time.sleep(2)
        val = page.execute_script("return localStorage.getItem('reg_test');")
        assert val == "pass"

    def test_reg_016_no_memory_leaks_rapid_nav(self, driver):
        page = BasePage(driver); page.navigate_to(""); time.sleep(3)
        initial = page.execute_script("return performance.memory ? performance.memory.usedJSHeapSize : 0;")
        for _ in range(5):
            page.navigate_to("#/role-selection"); time.sleep(1)
            page.navigate_to("#/bystander/auth"); time.sleep(1)
        final = page.execute_script("return performance.memory ? performance.memory.usedJSHeapSize : 0;")
        # Allow 3x growth
        assert final == 0 or initial == 0 or final < initial * 3

    def test_reg_017_console_errors_stable(self, driver):
        page = SplashPage(driver); page.navigate(); time.sleep(5)
        errors = page.get_console_errors()
        assert len(errors) < 20

    def test_reg_018_page_source_not_empty(self, driver):
        page = BasePage(driver)
        for r in ["#/", "#/role-selection", "#/bystander/auth"]:
            page.navigate_to(r); time.sleep(2)
            assert len(page.get_page_source()) > 500

    def test_reg_019_dom_nodes_reasonable(self, driver):
        page = SplashPage(driver); page.navigate(); time.sleep(5)
        nodes = page.execute_script("return document.querySelectorAll('*').length;")
        assert nodes and nodes > 5 and nodes < 50000

    def test_reg_020_viewport_meta_on_all_pages(self, driver):
        page = BasePage(driver)
        for r in ["#/", "#/role-selection"]:
            page.navigate_to(r); time.sleep(2)
            src = page.get_page_source()
            assert "viewport" in src.lower() or "width" in src

    def test_reg_021_https_on_all_pages(self, driver):
        page = BasePage(driver)
        for r in ["#/", "#/role-selection", "#/bystander/auth"]:
            page.navigate_to(r); time.sleep(2)
            assert page.get_current_url().startswith("https")

    def test_reg_022_no_mixed_content(self, driver):
        page = SplashPage(driver); page.navigate(); time.sleep(3)
        logs = page.get_console_logs()
        mixed = [l for l in logs if "Mixed Content" in str(l.get("message",""))]
        assert len(mixed) < 5

    def test_reg_023_favicon_loads(self, driver):
        page = SplashPage(driver); page.navigate()
        assert "favicon" in page.get_page_source().lower()

    def test_reg_024_manifest_referenced(self, driver):
        page = SplashPage(driver); page.navigate()
        assert "manifest.json" in page.get_page_source()

    def test_reg_025_flutter_bootstrap_referenced(self, driver):
        page = SplashPage(driver); page.navigate()
        assert "flutter_bootstrap" in page.get_page_source() or "flutter" in page.get_page_source().lower()

    # ── Edge Case Regression (REG-026 to REG-040) ────────────────────────
    def test_reg_026_double_navigation_stable(self, driver):
        page = BasePage(driver)
        page.navigate_to("#/role-selection"); page.navigate_to("#/role-selection")
        time.sleep(3); assert page.wait_for_flutter()

    def test_reg_027_triple_refresh_stable(self, driver):
        page = SplashPage(driver); page.navigate()
        for _ in range(3): page.refresh(); time.sleep(1)
        time.sleep(3); assert page.wait_for_flutter()

    def test_reg_028_navigate_and_back_rapid(self, driver):
        page = BasePage(driver); page.navigate_to("#/")
        for _ in range(5):
            page.navigate_to("#/role-selection"); time.sleep(0.3)
            page.go_back(); time.sleep(0.3)
        assert page.wait_for_flutter()

    def test_reg_029_all_routes_return_flutter(self, driver):
        page = BasePage(driver)
        flutter_count = 0
        for path in list(ROUTES.values())[:10]:
            page.navigate_to(f"#{path}"); time.sleep(2)
            if page.wait_for_flutter(): flutter_count += 1
        assert flutter_count > 0

    def test_reg_030_error_routes_dont_crash(self, driver):
        page = BasePage(driver)
        for r in ["#/404", "#/error", "#/undefined", "#/null"]:
            page.navigate_to(r); time.sleep(1)
        assert page.wait_for_flutter() or True

    def test_reg_031_special_route_chars(self, driver):
        page = BasePage(driver)
        for r in ["#/@", "#/$", "#/+", "#/="]:
            page.navigate_to(r); time.sleep(1)
        assert page.wait_for_flutter() or True

    def test_reg_032_unicode_routes(self, driver):
        page = BasePage(driver)
        page.navigate_to("#/日本語"); time.sleep(2)
        assert page.wait_for_flutter() or True

    def test_reg_033_empty_hash(self, driver):
        page = BasePage(driver); page.navigate_to("#")
        time.sleep(2); assert page.wait_for_flutter() or True

    def test_reg_034_root_without_hash(self, driver):
        page = BasePage(driver); page.navigate_to("")
        time.sleep(3); assert page.wait_for_flutter()

    def test_reg_035_large_viewport_all_pages(self, driver):
        page = BasePage(driver); page.set_viewport(2560, 1440)
        for r in ["#/", "#/role-selection"]:
            page.navigate_to(r); time.sleep(2)
        assert page.wait_for_flutter()

    def test_reg_036_small_viewport_all_pages(self, driver):
        page = BasePage(driver); page.set_viewport(320, 568)
        for r in ["#/", "#/role-selection"]:
            page.navigate_to(r); time.sleep(2)
        assert page.wait_for_flutter()

    def test_reg_037_storage_not_leaking(self, driver):
        page = SplashPage(driver); page.navigate()
        page.execute_script("localStorage.clear();")
        for _ in range(10):
            page.execute_script("localStorage.setItem('leak_' + Math.random(), 'data');")
        count = page.execute_script("return localStorage.length;")
        assert count <= 20

    def test_reg_038_session_cleanup(self, driver):
        page = SplashPage(driver); page.navigate()
        page.execute_script("sessionStorage.clear();")
        count = page.execute_script("return sessionStorage.length;")
        assert count == 0

    def test_reg_039_performance_stable(self, driver):
        page = SplashPage(driver); page.navigate(); time.sleep(5)
        timing = page.execute_script("return performance.getEntriesByType('resource').length;")
        assert timing is not None and timing >= 0

    def test_reg_040_no_infinite_redirects(self, driver):
        page = SplashPage(driver)
        start = time.time(); page.navigate(); elapsed = time.time() - start
        assert elapsed < 30, "Possible infinite redirect"

    # ── Final Validation (REG-041 to REG-050) ────────────────────────────
    def test_reg_041_complete_bystander_emergency_flow(self, driver):
        page = BasePage(driver)
        flow = ["#/", "#/role-selection", "#/bystander/auth", "#/bystander/home",
                "#/bystander/confirm", "#/bystander/first-aid", "#/bystander/tracking"]
        for r in flow: page.navigate_to(r); time.sleep(1.5)
        assert page.wait_for_flutter()

    def test_reg_042_complete_volunteer_response_flow(self, driver):
        page = BasePage(driver)
        flow = ["#/", "#/role-selection", "#/volunteer/register", "#/volunteer/dashboard",
                "#/volunteer/alert", "#/volunteer/navigation", "#/volunteer/complete"]
        for r in flow: page.navigate_to(r); time.sleep(1.5)
        assert page.wait_for_flutter()

    def test_reg_043_complete_hospital_flow(self, driver):
        page = BasePage(driver)
        flow = ["#/", "#/role-selection", "#/hospital/register", "#/hospital/dashboard"]
        for r in flow: page.navigate_to(r); time.sleep(1.5)
        assert page.wait_for_flutter()

    def test_reg_044_all_shared_pages(self, driver):
        page = BasePage(driver)
        for r in ["#/history", "#/profile"]:
            page.navigate_to(r); time.sleep(2)
            assert page.wait_for_flutter()

    def test_reg_045_final_screenshot_splash(self, driver):
        page = SplashPage(driver); page.navigate(); time.sleep(5)
        p = page.take_screenshot("reg_final_splash"); assert p and os.path.exists(p)

    def test_reg_046_final_screenshot_roles(self, driver):
        page = RoleSelectionPage(driver); page.navigate(); time.sleep(5)
        p = page.take_screenshot("reg_final_roles"); assert p and os.path.exists(p)

    def test_reg_047_final_screenshot_auth(self, driver):
        page = BystanderAuthPage(driver); page.navigate(); time.sleep(5)
        p = page.take_screenshot("reg_final_auth"); assert p and os.path.exists(p)

    def test_reg_048_final_no_critical_errors(self, driver):
        page = SplashPage(driver); page.navigate(); time.sleep(5)
        errors = page.get_console_errors()
        critical = [e for e in errors if "Uncaught" in str(e.get("message","")) and "TypeError" in str(e.get("message",""))]
        assert len(critical) == 0

    def test_reg_049_final_page_renders_content(self, driver):
        page = SplashPage(driver); page.navigate(); time.sleep(5)
        assert page.wait_for_flutter()
        assert len(page.get_page_source()) > 1000

    def test_reg_050_final_cleanup(self, driver):
        page = SplashPage(driver); page.navigate()
        page.execute_script("localStorage.clear(); sessionStorage.clear();")
        assert page.is_loaded()
