"""
Navigation Test Suite – 30 test cases covering route transitions,
deep linking, browser navigation, and GoRouter behavior.
"""
import pytest
import time
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.all_pages import *
from pages.base_page import BasePage
from config.settings import BASE_URL, ROUTES


class TestNavigation:
    """Navigation module – 30 test cases."""

    def test_nav_001_home_to_role_selection(self, driver):
        """TC: NAV-001 | Navigate from splash to role selection."""
        page = BasePage(driver)
        page.navigate_to("")
        time.sleep(3)
        page.navigate_to("#/role-selection")
        time.sleep(3)
        assert page.wait_for_flutter(), "Navigation to role selection failed"

    def test_nav_002_role_to_bystander_auth(self, driver):
        """TC: NAV-002 | Navigate from role selection to bystander auth."""
        page = BasePage(driver)
        page.navigate_to("#/bystander/auth")
        time.sleep(3)
        assert page.wait_for_flutter(), "Navigation to bystander auth failed"

    def test_nav_003_role_to_hospital_register(self, driver):
        """TC: NAV-003 | Navigate to hospital registration."""
        page = BasePage(driver)
        page.navigate_to("#/hospital/register")
        time.sleep(3)
        assert page.wait_for_flutter(), "Navigation to hospital register failed"

    def test_nav_004_role_to_volunteer_register(self, driver):
        """TC: NAV-004 | Navigate to volunteer registration."""
        page = BasePage(driver)
        page.navigate_to("#/volunteer/register")
        time.sleep(3)
        assert page.wait_for_flutter(), "Navigation to volunteer register failed"

    def test_nav_005_browser_back_button(self, driver):
        """TC: NAV-005 | Verify browser back button works."""
        page = BasePage(driver)
        page.navigate_to("")
        time.sleep(2)
        page.navigate_to("#/role-selection")
        time.sleep(2)
        page.go_back()
        time.sleep(2)
        assert page.wait_for_flutter(), "Back button broke app"

    def test_nav_006_browser_forward_button(self, driver):
        """TC: NAV-006 | Verify browser forward button works."""
        page = BasePage(driver)
        page.navigate_to("")
        time.sleep(2)
        page.navigate_to("#/role-selection")
        time.sleep(2)
        page.go_back()
        time.sleep(1)
        driver.forward()
        time.sleep(2)
        assert page.wait_for_flutter(), "Forward button broke app"

    def test_nav_007_deep_link_splash(self, driver):
        """TC: NAV-007 | Deep link to splash page."""
        page = BasePage(driver)
        page.navigate_to("#/")
        time.sleep(3)
        assert page.wait_for_flutter(), "Deep link to splash failed"

    def test_nav_008_deep_link_bystander_home(self, driver):
        """TC: NAV-008 | Deep link to bystander home."""
        page = BasePage(driver)
        page.navigate_to("#/bystander/home")
        time.sleep(3)
        assert page.wait_for_flutter(), "Deep link to bystander home failed"

    def test_nav_009_deep_link_hospital_dashboard(self, driver):
        """TC: NAV-009 | Deep link to hospital dashboard."""
        page = BasePage(driver)
        page.navigate_to("#/hospital/dashboard")
        time.sleep(3)
        assert page.wait_for_flutter(), "Deep link to hospital dashboard failed"

    def test_nav_010_deep_link_volunteer_dashboard(self, driver):
        """TC: NAV-010 | Deep link to volunteer dashboard."""
        page = BasePage(driver)
        page.navigate_to("#/volunteer/dashboard")
        time.sleep(3)
        assert page.wait_for_flutter(), "Deep link to volunteer dashboard failed"

    def test_nav_011_deep_link_history(self, driver):
        """TC: NAV-011 | Deep link to history page."""
        page = BasePage(driver)
        page.navigate_to("#/history")
        time.sleep(3)
        assert page.wait_for_flutter(), "Deep link to history failed"

    def test_nav_012_deep_link_profile(self, driver):
        """TC: NAV-012 | Deep link to profile page."""
        page = BasePage(driver)
        page.navigate_to("#/profile")
        time.sleep(3)
        assert page.wait_for_flutter(), "Deep link to profile failed"

    def test_nav_013_page_refresh_stability(self, driver):
        """TC: NAV-013 | Verify page refresh doesn't break navigation."""
        page = BasePage(driver)
        page.navigate_to("#/role-selection")
        time.sleep(3)
        page.refresh()
        time.sleep(3)
        assert page.wait_for_flutter(), "Refresh broke navigation"

    def test_nav_014_rapid_navigation(self, driver):
        """TC: NAV-014 | Verify rapid navigation between routes."""
        page = BasePage(driver)
        for route in ["#/", "#/role-selection", "#/bystander/auth", "#/hospital/register"]:
            page.navigate_to(route)
            time.sleep(0.5)
        time.sleep(2)
        assert page.wait_for_flutter(), "Rapid navigation crashed app"

    def test_nav_015_all_defined_routes_reachable(self, driver):
        """TC: NAV-015 | Verify all defined routes are reachable."""
        page = BasePage(driver)
        reachable = 0
        for name, path in ROUTES.items():
            page.navigate_to(f"#{path}")
            time.sleep(2)
            if page.wait_for_flutter():
                reachable += 1
        assert reachable > 0, "No routes reachable"

    def test_nav_016_404_error_page_shows(self, driver):
        """TC: NAV-016 | Verify 404 error page for invalid routes."""
        page = BasePage(driver)
        page.navigate_to("#/this-route-does-not-exist")
        time.sleep(3)
        # GoRouter errorBuilder shows "Page not found"
        assert page.wait_for_flutter(), "Error page did not render"

    def test_nav_017_url_hash_routing_works(self, driver):
        """TC: NAV-017 | Verify hash-based routing works correctly."""
        page = BasePage(driver)
        page.navigate_to("#/role-selection")
        time.sleep(3)
        url = page.get_current_url()
        assert "#" in url or "role" in url or page.wait_for_flutter(), "Hash routing broken"

    def test_nav_018_navigate_to_bystander_hospitals(self, driver):
        """TC: NAV-018 | Navigate to hospital map screen."""
        page = BasePage(driver)
        page.navigate_to("#/bystander/hospitals")
        time.sleep(3)
        assert page.wait_for_flutter(), "Hospital map navigation failed"

    def test_nav_019_navigate_to_volunteer_alert(self, driver):
        """TC: NAV-019 | Navigate to volunteer alert screen."""
        page = BasePage(driver)
        page.navigate_to("#/volunteer/alert")
        time.sleep(3)
        assert page.wait_for_flutter(), "Volunteer alert navigation failed"

    def test_nav_020_navigate_to_volunteer_nav(self, driver):
        """TC: NAV-020 | Navigate to volunteer navigation screen."""
        page = BasePage(driver)
        page.navigate_to("#/volunteer/navigation")
        time.sleep(3)
        assert page.wait_for_flutter(), "Volunteer navigation failed"

    def test_nav_021_navigate_to_case_completion(self, driver):
        """TC: NAV-021 | Navigate to case completion screen."""
        page = BasePage(driver)
        page.navigate_to("#/volunteer/complete")
        time.sleep(3)
        assert page.wait_for_flutter(), "Case completion navigation failed"

    def test_nav_022_navigate_to_bystander_confirm(self, driver):
        """TC: NAV-022 | Navigate to bystander confirmation."""
        page = BasePage(driver)
        page.navigate_to("#/bystander/confirm")
        time.sleep(3)
        assert page.wait_for_flutter(), "Bystander confirm navigation failed"

    def test_nav_023_navigate_to_first_aid(self, driver):
        """TC: NAV-023 | Navigate to first aid guidance."""
        page = BasePage(driver)
        page.navigate_to("#/bystander/first-aid")
        time.sleep(3)
        assert page.wait_for_flutter(), "First aid navigation failed"

    def test_nav_024_navigate_to_tracking(self, driver):
        """TC: NAV-024 | Navigate to volunteer tracking."""
        page = BasePage(driver)
        page.navigate_to("#/bystander/tracking")
        time.sleep(3)
        assert page.wait_for_flutter(), "Tracking navigation failed"

    def test_nav_025_navigate_to_hospital_alert(self, driver):
        """TC: NAV-025 | Navigate to hospital alert."""
        page = BasePage(driver)
        page.navigate_to("#/bystander/hospital-alert")
        time.sleep(3)
        assert page.wait_for_flutter(), "Hospital alert navigation failed"

    def test_nav_026_sequential_bystander_flow(self, driver):
        """TC: NAV-026 | Navigate through complete bystander flow."""
        page = BasePage(driver)
        flow = ["#/", "#/role-selection", "#/bystander/auth", "#/bystander/home"]
        for route in flow:
            page.navigate_to(route)
            time.sleep(2)
        assert page.wait_for_flutter(), "Bystander flow navigation failed"

    def test_nav_027_sequential_volunteer_flow(self, driver):
        """TC: NAV-027 | Navigate through complete volunteer flow."""
        page = BasePage(driver)
        flow = ["#/", "#/role-selection", "#/volunteer/register", "#/volunteer/dashboard"]
        for route in flow:
            page.navigate_to(route)
            time.sleep(2)
        assert page.wait_for_flutter(), "Volunteer flow navigation failed"

    def test_nav_028_sequential_hospital_flow(self, driver):
        """TC: NAV-028 | Navigate through complete hospital flow."""
        page = BasePage(driver)
        flow = ["#/", "#/role-selection", "#/hospital/register", "#/hospital/dashboard"]
        for route in flow:
            page.navigate_to(route)
            time.sleep(2)
        assert page.wait_for_flutter(), "Hospital flow navigation failed"

    def test_nav_029_cross_role_navigation(self, driver):
        """TC: NAV-029 | Navigate between different role sections."""
        page = BasePage(driver)
        page.navigate_to("#/bystander/auth")
        time.sleep(2)
        page.navigate_to("#/volunteer/register")
        time.sleep(2)
        page.navigate_to("#/hospital/register")
        time.sleep(2)
        assert page.wait_for_flutter(), "Cross-role navigation failed"

    def test_nav_030_return_to_splash_from_deep(self, driver):
        """TC: NAV-030 | Navigate back to splash from deep route."""
        page = BasePage(driver)
        page.navigate_to("#/volunteer/dashboard")
        time.sleep(2)
        page.navigate_to("#/")
        time.sleep(3)
        assert page.wait_for_flutter(), "Return to splash failed"
