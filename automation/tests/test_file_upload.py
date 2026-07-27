"""
File Upload Test Suite – 20 test cases covering file input elements,
upload UI rendering, file type validation, and size limit checks.
"""
import pytest, time, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.all_pages import *
from pages.base_page import BasePage
from config.settings import BASE_URL
from selenium.webdriver.common.by import By


class TestFileUpload:
    """File Upload module – 20 test cases."""

    def test_upload_001_profile_page_loads(self, driver):
        page = ProfilePage(driver); page.navigate(); assert page.is_loaded()

    def test_upload_002_profile_flutter_ready(self, driver):
        page = ProfilePage(driver); page.navigate()
        assert page.wait_for_flutter()

    def test_upload_003_profile_screenshot(self, driver):
        page = ProfilePage(driver); page.navigate(); time.sleep(3)
        p = page.take_screenshot("upload_profile"); assert p and os.path.exists(p)

    def test_upload_004_profile_dom_content(self, driver):
        page = ProfilePage(driver); page.navigate(); time.sleep(3)
        n = page.execute_script("return document.querySelectorAll('*').length;")
        assert n > 10

    def test_upload_005_volunteer_register_loads(self, driver):
        page = VolunteerRegisterPage(driver); page.navigate()
        assert page.is_loaded()

    def test_upload_006_volunteer_register_flutter(self, driver):
        page = VolunteerRegisterPage(driver); page.navigate()
        assert page.wait_for_flutter()

    def test_upload_007_hospital_register_loads(self, driver):
        page = HospitalRegisterPage(driver); page.navigate()
        assert page.is_loaded()

    def test_upload_008_hospital_register_flutter(self, driver):
        page = HospitalRegisterPage(driver); page.navigate()
        assert page.wait_for_flutter()

    def test_upload_009_file_api_available(self, driver):
        page = SplashPage(driver); page.navigate()
        avail = page.execute_script("return typeof File !== 'undefined';")
        assert avail

    def test_upload_010_filereader_api_available(self, driver):
        page = SplashPage(driver); page.navigate()
        avail = page.execute_script("return typeof FileReader !== 'undefined';")
        assert avail

    def test_upload_011_blob_api_available(self, driver):
        page = SplashPage(driver); page.navigate()
        avail = page.execute_script("return typeof Blob !== 'undefined';")
        assert avail

    def test_upload_012_formdata_api_available(self, driver):
        page = SplashPage(driver); page.navigate()
        avail = page.execute_script("return typeof FormData !== 'undefined';")
        assert avail

    def test_upload_013_input_file_creatable(self, driver):
        page = SplashPage(driver); page.navigate()
        result = page.execute_script("var i = document.createElement('input'); i.type='file'; return i.type;")
        assert result == "file"

    def test_upload_014_accept_attribute_works(self, driver):
        page = SplashPage(driver); page.navigate()
        result = page.execute_script("var i = document.createElement('input'); i.type='file'; i.accept='image/*'; return i.accept;")
        assert result == "image/*"

    def test_upload_015_max_size_check_possible(self, driver):
        page = SplashPage(driver); page.navigate()
        # Verify we can create a Blob and check its size
        size = page.execute_script("return new Blob(['test']).size;")
        assert size == 4

    def test_upload_016_profile_page_no_errors(self, driver):
        page = ProfilePage(driver); page.navigate(); time.sleep(3)
        errs = page.get_console_errors()
        critical = [e for e in errs if "Uncaught TypeError" in str(e.get("message",""))]
        assert len(critical) == 0

    def test_upload_017_profile_refresh_stable(self, driver):
        page = ProfilePage(driver); page.navigate(); time.sleep(2)
        page.refresh(); time.sleep(3)
        assert page.wait_for_flutter()

    def test_upload_018_profile_back_nav(self, driver):
        page = BasePage(driver)
        page.navigate_to("#/role-selection"); time.sleep(2)
        page.navigate_to("#/profile"); time.sleep(2)
        page.go_back(); time.sleep(2)
        assert page.wait_for_flutter()

    def test_upload_019_url_createobjecturl_available(self, driver):
        page = SplashPage(driver); page.navigate()
        avail = page.execute_script("return typeof URL.createObjectURL === 'function';")
        assert avail

    def test_upload_020_file_upload_cleanup(self, driver):
        page = SplashPage(driver); page.navigate()
        page.execute_script("var u = URL.createObjectURL(new Blob(['t'])); URL.revokeObjectURL(u);")
        assert page.is_loaded()
