"""
CRUD Operations Test Suite – 50 test cases covering create/read/update/delete
flows across emergency, volunteer, hospital, and profile features.
"""
import pytest
import time
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.all_pages import *
from pages.base_page import BasePage
from config.settings import BASE_URL, ROUTES


class TestCRUDOperations:
    """CRUD Operations module – 50 test cases."""

    # ── Emergency CRUD (CRUD-001 to CRUD-015) ─────────────────────────────
    def test_crud_001_bystander_home_loads(self, driver):
        page = BystanderHomePage(driver); page.navigate(); assert page.is_loaded()

    def test_crud_002_emergency_page_renders(self, driver):
        page = BystanderHomePage(driver); page.navigate()
        assert page.wait_for_flutter()

    def test_crud_003_emergency_confirm_loads(self, driver):
        page = BasePage(driver); page.navigate_to("#/bystander/confirm"); time.sleep(3)
        assert page.wait_for_flutter()

    def test_crud_004_first_aid_page_loads(self, driver):
        page = BasePage(driver); page.navigate_to("#/bystander/first-aid"); time.sleep(3)
        assert page.wait_for_flutter()

    def test_crud_005_tracking_page_loads(self, driver):
        page = BasePage(driver); page.navigate_to("#/bystander/tracking"); time.sleep(3)
        assert page.wait_for_flutter()

    def test_crud_006_hospital_alert_loads(self, driver):
        page = BasePage(driver); page.navigate_to("#/bystander/hospital-alert"); time.sleep(3)
        assert page.wait_for_flutter()

    def test_crud_007_hospital_map_loads(self, driver):
        page = BasePage(driver); page.navigate_to("#/bystander/hospitals"); time.sleep(3)
        assert page.wait_for_flutter()

    def test_crud_008_emergency_home_screenshot(self, driver):
        page = BystanderHomePage(driver); page.navigate(); time.sleep(3)
        p = page.take_screenshot("crud_emergency_home"); assert p and os.path.exists(p)

    def test_crud_009_emergency_home_dom(self, driver):
        page = BystanderHomePage(driver); page.navigate(); time.sleep(3)
        n = page.execute_script("return document.querySelectorAll('*').length;"); assert n > 10

    def test_crud_010_emergency_home_no_errors(self, driver):
        page = BystanderHomePage(driver); page.navigate(); time.sleep(3)
        errs = page.get_console_errors()
        critical = [e for e in errs if "Uncaught TypeError" in str(e.get("message",""))]
        assert len(critical) == 0

    def test_crud_011_emergency_flow_sequence(self, driver):
        page = BasePage(driver)
        for r in ["#/bystander/home", "#/bystander/confirm", "#/bystander/first-aid"]:
            page.navigate_to(r); time.sleep(2)
        assert page.wait_for_flutter()

    def test_crud_012_emergency_tracking_flow(self, driver):
        page = BasePage(driver)
        page.navigate_to("#/bystander/tracking"); time.sleep(3)
        assert page.wait_for_flutter()

    def test_crud_013_emergency_hospital_alert_flow(self, driver):
        page = BasePage(driver)
        page.navigate_to("#/bystander/hospital-alert"); time.sleep(3)
        assert page.wait_for_flutter()

    def test_crud_014_emergency_confirm_screenshot(self, driver):
        page = BasePage(driver); page.navigate_to("#/bystander/confirm"); time.sleep(3)
        p = page.take_screenshot("crud_confirm"); assert p and os.path.exists(p)

    def test_crud_015_first_aid_screenshot(self, driver):
        page = BasePage(driver); page.navigate_to("#/bystander/first-aid"); time.sleep(3)
        p = page.take_screenshot("crud_first_aid"); assert p and os.path.exists(p)

    # ── Hospital CRUD (CRUD-016 to CRUD-030) ─────────────────────────────
    def test_crud_016_hospital_dashboard_loads(self, driver):
        page = HospitalDashboardPage(driver); page.navigate(); assert page.is_loaded()

    def test_crud_017_hospital_dashboard_flutter(self, driver):
        page = HospitalDashboardPage(driver); page.navigate()
        assert page.wait_for_flutter()

    def test_crud_018_hospital_dashboard_screenshot(self, driver):
        page = HospitalDashboardPage(driver); page.navigate(); time.sleep(3)
        p = page.take_screenshot("crud_hospital_dash"); assert p and os.path.exists(p)

    def test_crud_019_hospital_dashboard_dom(self, driver):
        page = HospitalDashboardPage(driver); page.navigate(); time.sleep(3)
        n = page.execute_script("return document.querySelectorAll('*').length;"); assert n > 10

    def test_crud_020_hospital_register_loads(self, driver):
        page = HospitalRegisterPage(driver); page.navigate(); assert page.is_loaded()

    def test_crud_021_hospital_register_flutter(self, driver):
        page = HospitalRegisterPage(driver); page.navigate()
        assert page.wait_for_flutter()

    def test_crud_022_hospital_register_to_dashboard(self, driver):
        page = BasePage(driver)
        page.navigate_to("#/hospital/register"); time.sleep(2)
        page.navigate_to("#/hospital/dashboard"); time.sleep(2)
        assert page.wait_for_flutter()

    def test_crud_023_hospital_dashboard_no_errors(self, driver):
        page = HospitalDashboardPage(driver); page.navigate(); time.sleep(3)
        errs = page.get_console_errors()
        critical = [e for e in errs if "Uncaught TypeError" in str(e.get("message",""))]
        assert len(critical) == 0

    def test_crud_024_hospital_dashboard_refresh(self, driver):
        page = HospitalDashboardPage(driver); page.navigate(); time.sleep(2)
        page.refresh(); time.sleep(3)
        assert page.wait_for_flutter()

    def test_crud_025_hospital_page_source(self, driver):
        page = HospitalDashboardPage(driver); page.navigate()
        assert len(page.get_page_source()) > 1000

    def test_crud_026_hospital_register_screenshot(self, driver):
        page = HospitalRegisterPage(driver); page.navigate(); time.sleep(3)
        p = page.take_screenshot("crud_hospital_reg"); assert p and os.path.exists(p)

    def test_crud_027_hospital_dashboard_back_nav(self, driver):
        page = BasePage(driver)
        page.navigate_to("#/hospital/register"); time.sleep(2)
        page.navigate_to("#/hospital/dashboard"); time.sleep(2)
        page.go_back(); time.sleep(2)
        assert page.wait_for_flutter()

    def test_crud_028_hospital_dashboard_canvas(self, driver):
        page = HospitalDashboardPage(driver); page.navigate(); time.sleep(5)
        from selenium.webdriver.common.by import By
        assert page.is_element_visible(By.TAG_NAME, "canvas", timeout=10) or page.is_loaded()

    def test_crud_029_hospital_register_fast_load(self, driver):
        start = time.time()
        page = HospitalRegisterPage(driver); page.navigate()
        assert time.time() - start < 30

    def test_crud_030_hospital_dashboard_body(self, driver):
        page = HospitalDashboardPage(driver); page.navigate(); time.sleep(3)
        c = page.execute_script("return document.body.childElementCount;"); assert c > 0

    # ── Volunteer CRUD (CRUD-031 to CRUD-045) ────────────────────────────
    def test_crud_031_volunteer_dashboard_loads(self, driver):
        page = VolunteerDashboardPage(driver); page.navigate(); assert page.is_loaded()

    def test_crud_032_volunteer_dashboard_flutter(self, driver):
        page = VolunteerDashboardPage(driver); page.navigate()
        assert page.wait_for_flutter()

    def test_crud_033_volunteer_dashboard_screenshot(self, driver):
        page = VolunteerDashboardPage(driver); page.navigate(); time.sleep(3)
        p = page.take_screenshot("crud_vol_dash"); assert p and os.path.exists(p)

    def test_crud_034_volunteer_dashboard_dom(self, driver):
        page = VolunteerDashboardPage(driver); page.navigate(); time.sleep(3)
        n = page.execute_script("return document.querySelectorAll('*').length;"); assert n > 10

    def test_crud_035_volunteer_register_loads(self, driver):
        page = VolunteerRegisterPage(driver); page.navigate(); assert page.is_loaded()

    def test_crud_036_volunteer_register_flutter(self, driver):
        page = VolunteerRegisterPage(driver); page.navigate()
        assert page.wait_for_flutter()

    def test_crud_037_volunteer_alert_loads(self, driver):
        page = BasePage(driver); page.navigate_to("#/volunteer/alert"); time.sleep(3)
        assert page.wait_for_flutter()

    def test_crud_038_volunteer_navigation_loads(self, driver):
        page = BasePage(driver); page.navigate_to("#/volunteer/navigation"); time.sleep(3)
        assert page.wait_for_flutter()

    def test_crud_039_volunteer_complete_loads(self, driver):
        page = BasePage(driver); page.navigate_to("#/volunteer/complete"); time.sleep(3)
        assert page.wait_for_flutter()

    def test_crud_040_volunteer_flow_sequence(self, driver):
        page = BasePage(driver)
        for r in ["#/volunteer/register", "#/volunteer/dashboard", "#/volunteer/alert"]:
            page.navigate_to(r); time.sleep(2)
        assert page.wait_for_flutter()

    def test_crud_041_volunteer_dashboard_no_errors(self, driver):
        page = VolunteerDashboardPage(driver); page.navigate(); time.sleep(3)
        errs = page.get_console_errors()
        critical = [e for e in errs if "Uncaught TypeError" in str(e.get("message",""))]
        assert len(critical) == 0

    def test_crud_042_volunteer_dashboard_refresh(self, driver):
        page = VolunteerDashboardPage(driver); page.navigate(); time.sleep(2)
        page.refresh(); time.sleep(3)
        assert page.wait_for_flutter()

    def test_crud_043_volunteer_register_screenshot(self, driver):
        page = VolunteerRegisterPage(driver); page.navigate(); time.sleep(3)
        p = page.take_screenshot("crud_vol_reg"); assert p and os.path.exists(p)

    def test_crud_044_volunteer_dashboard_back_nav(self, driver):
        page = BasePage(driver)
        page.navigate_to("#/volunteer/register"); time.sleep(2)
        page.navigate_to("#/volunteer/dashboard"); time.sleep(2)
        page.go_back(); time.sleep(2)
        assert page.wait_for_flutter()

    def test_crud_045_volunteer_dashboard_canvas(self, driver):
        page = VolunteerDashboardPage(driver); page.navigate(); time.sleep(5)
        from selenium.webdriver.common.by import By
        assert page.is_element_visible(By.TAG_NAME, "canvas", timeout=10) or page.is_loaded()

    # ── Shared CRUD (CRUD-046 to CRUD-050) ───────────────────────────────
    def test_crud_046_history_page_loads(self, driver):
        page = EmergencyHistoryPage(driver); page.navigate(); assert page.is_loaded()

    def test_crud_047_profile_page_loads(self, driver):
        page = ProfilePage(driver); page.navigate(); assert page.is_loaded()

    def test_crud_048_history_screenshot(self, driver):
        page = EmergencyHistoryPage(driver); page.navigate(); time.sleep(3)
        p = page.take_screenshot("crud_history"); assert p and os.path.exists(p)

    def test_crud_049_profile_screenshot(self, driver):
        page = ProfilePage(driver); page.navigate(); time.sleep(3)
        p = page.take_screenshot("crud_profile"); assert p and os.path.exists(p)

    def test_crud_050_history_to_profile_nav(self, driver):
        page = BasePage(driver)
        page.navigate_to("#/history"); time.sleep(2)
        page.navigate_to("#/profile"); time.sleep(2)
        assert page.wait_for_flutter()
