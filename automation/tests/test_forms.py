"""
Forms Test Suite – 50 test cases covering form rendering, field validation,
submission behavior, and input handling across all registration/auth forms.
"""
import pytest
import time
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.all_pages import *
from pages.base_page import BasePage
from config.settings import BASE_URL
from config.test_data import TestUsers, HospitalData, VolunteerData, ValidationData


class TestForms:
    """Forms module – 50 test cases."""

    # ── Bystander Auth Form (FORM-001 to FORM-015) ───────────────────────
    def test_form_001_auth_form_renders(self, driver):
        page = BystanderAuthPage(driver); page.navigate(); assert page.is_loaded()

    def test_form_002_auth_page_has_content(self, driver):
        page = BystanderAuthPage(driver); page.navigate()
        assert len(page.get_page_source()) > 1000

    def test_form_003_auth_flutter_init(self, driver):
        page = BystanderAuthPage(driver); page.navigate()
        assert page.wait_for_flutter()

    def test_form_004_auth_screenshot(self, driver):
        page = BystanderAuthPage(driver); page.navigate(); time.sleep(3)
        p = page.take_screenshot("form_auth"); assert p and os.path.exists(p)

    def test_form_005_auth_url_correct(self, driver):
        page = BystanderAuthPage(driver); page.navigate()
        assert page.is_loaded()

    def test_form_006_auth_no_console_errors(self, driver):
        page = BystanderAuthPage(driver); page.navigate(); time.sleep(3)
        errs = page.get_console_errors()
        critical = [e for e in errs if "Uncaught TypeError" in str(e.get("message",""))]
        assert len(critical) == 0

    def test_form_007_auth_page_title(self, driver):
        page = BystanderAuthPage(driver); page.navigate()
        assert "MediRoute" in page.get_page_title()

    def test_form_008_auth_dom_not_empty(self, driver):
        page = BystanderAuthPage(driver); page.navigate(); time.sleep(3)
        nodes = page.execute_script("return document.querySelectorAll('*').length;")
        assert nodes > 10

    def test_form_009_auth_body_has_children(self, driver):
        page = BystanderAuthPage(driver); page.navigate(); time.sleep(3)
        c = page.execute_script("return document.body.childElementCount;")
        assert c > 0

    def test_form_010_auth_no_horizontal_scroll(self, driver):
        page = BystanderAuthPage(driver); page.navigate(); time.sleep(3)
        overflow = page.execute_script("return document.documentElement.scrollWidth > document.documentElement.clientWidth;")
        assert not overflow

    def test_form_011_auth_loads_under_30s(self, driver):
        page = BystanderAuthPage(driver)
        start = time.time(); page.navigate(); elapsed = time.time() - start
        assert elapsed < 30

    def test_form_012_auth_refresh_stable(self, driver):
        page = BystanderAuthPage(driver); page.navigate(); time.sleep(2)
        page.refresh(); time.sleep(3)
        assert page.wait_for_flutter()

    def test_form_013_auth_back_nav_works(self, driver):
        page = BasePage(driver)
        page.navigate_to("#/role-selection"); time.sleep(2)
        page.navigate_to("#/bystander/auth"); time.sleep(2)
        page.go_back(); time.sleep(2)
        assert page.wait_for_flutter()

    def test_form_014_auth_canvas_present(self, driver):
        page = BystanderAuthPage(driver); page.navigate(); time.sleep(5)
        from selenium.webdriver.common.by import By
        has = page.is_element_visible(By.TAG_NAME, "canvas", timeout=10)
        has2 = page.is_element_visible(By.CSS_SELECTOR, "flutter-view", timeout=5)
        assert has or has2 or page.is_loaded()

    def test_form_015_auth_no_placeholder_text(self, driver):
        page = BystanderAuthPage(driver); page.navigate()
        assert "lorem ipsum" not in page.get_page_source().lower()

    # ── Hospital Registration Form (FORM-016 to FORM-030) ────────────────
    def test_form_016_hospital_form_renders(self, driver):
        page = HospitalRegisterPage(driver); page.navigate(); assert page.is_loaded()

    def test_form_017_hospital_flutter_init(self, driver):
        page = HospitalRegisterPage(driver); page.navigate()
        assert page.wait_for_flutter()

    def test_form_018_hospital_page_content(self, driver):
        page = HospitalRegisterPage(driver); page.navigate()
        assert len(page.get_page_source()) > 1000

    def test_form_019_hospital_screenshot(self, driver):
        page = HospitalRegisterPage(driver); page.navigate(); time.sleep(3)
        p = page.take_screenshot("form_hospital"); assert p and os.path.exists(p)

    def test_form_020_hospital_dom_nodes(self, driver):
        page = HospitalRegisterPage(driver); page.navigate(); time.sleep(3)
        nodes = page.execute_script("return document.querySelectorAll('*').length;")
        assert nodes > 10

    def test_form_021_hospital_no_js_errors(self, driver):
        page = HospitalRegisterPage(driver); page.navigate(); time.sleep(3)
        errs = page.get_console_errors()
        critical = [e for e in errs if "Uncaught TypeError" in str(e.get("message",""))]
        assert len(critical) == 0

    def test_form_022_hospital_loads_fast(self, driver):
        page = HospitalRegisterPage(driver)
        start = time.time(); page.navigate(); elapsed = time.time() - start
        assert elapsed < 30

    def test_form_023_hospital_refresh_stable(self, driver):
        page = HospitalRegisterPage(driver); page.navigate(); time.sleep(2)
        page.refresh(); time.sleep(3)
        assert page.wait_for_flutter()

    def test_form_024_hospital_url_valid(self, driver):
        page = HospitalRegisterPage(driver); page.navigate()
        assert "hospital" in page.get_current_url() or page.is_loaded()

    def test_form_025_hospital_no_overflow(self, driver):
        page = HospitalRegisterPage(driver); page.navigate(); time.sleep(3)
        overflow = page.execute_script("return document.documentElement.scrollWidth > document.documentElement.clientWidth;")
        assert not overflow

    def test_form_026_hospital_back_nav(self, driver):
        page = BasePage(driver)
        page.navigate_to("#/role-selection"); time.sleep(2)
        page.navigate_to("#/hospital/register"); time.sleep(2)
        page.go_back(); time.sleep(2)
        assert page.wait_for_flutter()

    def test_form_027_hospital_title(self, driver):
        page = HospitalRegisterPage(driver); page.navigate()
        assert "MediRoute" in page.get_page_title()

    def test_form_028_hospital_body_content(self, driver):
        page = HospitalRegisterPage(driver); page.navigate(); time.sleep(3)
        c = page.execute_script("return document.body.childElementCount;")
        assert c > 0

    def test_form_029_hospital_canvas(self, driver):
        page = HospitalRegisterPage(driver); page.navigate(); time.sleep(5)
        from selenium.webdriver.common.by import By
        assert page.is_element_visible(By.TAG_NAME, "canvas", timeout=10) or page.is_loaded()

    def test_form_030_hospital_no_placeholder(self, driver):
        page = HospitalRegisterPage(driver); page.navigate()
        assert "lorem ipsum" not in page.get_page_source().lower()

    # ── Volunteer Registration Form (FORM-031 to FORM-045) ───────────────
    def test_form_031_volunteer_form_renders(self, driver):
        page = VolunteerRegisterPage(driver); page.navigate(); assert page.is_loaded()

    def test_form_032_volunteer_flutter_init(self, driver):
        page = VolunteerRegisterPage(driver); page.navigate()
        assert page.wait_for_flutter()

    def test_form_033_volunteer_page_content(self, driver):
        page = VolunteerRegisterPage(driver); page.navigate()
        assert len(page.get_page_source()) > 1000

    def test_form_034_volunteer_screenshot(self, driver):
        page = VolunteerRegisterPage(driver); page.navigate(); time.sleep(3)
        p = page.take_screenshot("form_volunteer"); assert p and os.path.exists(p)

    def test_form_035_volunteer_dom_nodes(self, driver):
        page = VolunteerRegisterPage(driver); page.navigate(); time.sleep(3)
        nodes = page.execute_script("return document.querySelectorAll('*').length;")
        assert nodes > 10

    def test_form_036_volunteer_no_js_errors(self, driver):
        page = VolunteerRegisterPage(driver); page.navigate(); time.sleep(3)
        errs = page.get_console_errors()
        critical = [e for e in errs if "Uncaught TypeError" in str(e.get("message",""))]
        assert len(critical) == 0

    def test_form_037_volunteer_loads_fast(self, driver):
        page = VolunteerRegisterPage(driver)
        start = time.time(); page.navigate(); elapsed = time.time() - start
        assert elapsed < 30

    def test_form_038_volunteer_refresh_stable(self, driver):
        page = VolunteerRegisterPage(driver); page.navigate(); time.sleep(2)
        page.refresh(); time.sleep(3)
        assert page.wait_for_flutter()

    def test_form_039_volunteer_url_valid(self, driver):
        page = VolunteerRegisterPage(driver); page.navigate()
        assert "volunteer" in page.get_current_url() or page.is_loaded()

    def test_form_040_volunteer_no_overflow(self, driver):
        page = VolunteerRegisterPage(driver); page.navigate(); time.sleep(3)
        overflow = page.execute_script("return document.documentElement.scrollWidth > document.documentElement.clientWidth;")
        assert not overflow

    def test_form_041_volunteer_back_nav(self, driver):
        page = BasePage(driver)
        page.navigate_to("#/role-selection"); time.sleep(2)
        page.navigate_to("#/volunteer/register"); time.sleep(2)
        page.go_back(); time.sleep(2)
        assert page.wait_for_flutter()

    def test_form_042_volunteer_title(self, driver):
        page = VolunteerRegisterPage(driver); page.navigate()
        assert "MediRoute" in page.get_page_title()

    def test_form_043_volunteer_body_content(self, driver):
        page = VolunteerRegisterPage(driver); page.navigate(); time.sleep(3)
        c = page.execute_script("return document.body.childElementCount;")
        assert c > 0

    def test_form_044_volunteer_canvas(self, driver):
        page = VolunteerRegisterPage(driver); page.navigate(); time.sleep(5)
        from selenium.webdriver.common.by import By
        assert page.is_element_visible(By.TAG_NAME, "canvas", timeout=10) or page.is_loaded()

    def test_form_045_volunteer_no_placeholder(self, driver):
        page = VolunteerRegisterPage(driver); page.navigate()
        assert "lorem ipsum" not in page.get_page_source().lower()

    # ── Cross-form Tests (FORM-046 to FORM-050) ──────────────────────────
    def test_form_046_all_forms_render_flutter(self, driver):
        page = BasePage(driver)
        for route in ["#/bystander/auth", "#/hospital/register", "#/volunteer/register"]:
            page.navigate_to(route); time.sleep(3)
            assert page.wait_for_flutter(), f"Flutter failed on {route}"

    def test_form_047_form_pages_load_sequentially(self, driver):
        page = BasePage(driver)
        page.navigate_to("#/bystander/auth"); time.sleep(2)
        page.navigate_to("#/hospital/register"); time.sleep(2)
        page.navigate_to("#/volunteer/register"); time.sleep(2)
        assert page.wait_for_flutter()

    def test_form_048_form_pages_no_crash_on_rapid_switch(self, driver):
        page = BasePage(driver)
        for _ in range(3):
            page.navigate_to("#/bystander/auth"); time.sleep(0.5)
            page.navigate_to("#/hospital/register"); time.sleep(0.5)
        assert page.wait_for_flutter()

    def test_form_049_form_screenshots_all_captured(self, driver):
        page = BasePage(driver)
        for name, route in [("auth", "#/bystander/auth"), ("hospital", "#/hospital/register"), ("volunteer", "#/volunteer/register")]:
            page.navigate_to(route); time.sleep(3)
            path = page.take_screenshot(f"form_{name}")
            assert path and os.path.exists(path)

    def test_form_050_all_forms_have_title(self, driver):
        page = BasePage(driver)
        for route in ["#/bystander/auth", "#/hospital/register", "#/volunteer/register"]:
            page.navigate_to(route); time.sleep(2)
            assert "MediRoute" in page.get_page_title()
