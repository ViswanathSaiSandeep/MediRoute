"""
Responsive Design Test Suite – 20 test cases covering viewport sizes,
mobile/tablet/desktop layouts, and breakpoint behavior.
"""
import pytest, time, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.all_pages import *
from pages.base_page import BasePage
from config.settings import BASE_URL, VIEWPORTS


class TestResponsiveDesign:
    """Responsive Design module – 20 test cases."""

    def test_resp_001_mobile_320_renders(self, driver):
        page = SplashPage(driver); page.set_viewport(320, 568); page.navigate(); time.sleep(5)
        assert page.wait_for_flutter()

    def test_resp_002_mobile_375_renders(self, driver):
        page = SplashPage(driver); page.set_viewport(375, 667); page.navigate(); time.sleep(5)
        assert page.wait_for_flutter()

    def test_resp_003_mobile_414_renders(self, driver):
        page = SplashPage(driver); page.set_viewport(414, 896); page.navigate(); time.sleep(5)
        assert page.wait_for_flutter()

    def test_resp_004_tablet_768_renders(self, driver):
        page = SplashPage(driver); page.set_viewport(768, 1024); page.navigate(); time.sleep(5)
        assert page.wait_for_flutter()

    def test_resp_005_laptop_1366_renders(self, driver):
        page = SplashPage(driver); page.set_viewport(1366, 768); page.navigate(); time.sleep(5)
        assert page.wait_for_flutter()

    def test_resp_006_desktop_1920_renders(self, driver):
        page = SplashPage(driver); page.set_viewport(1920, 1080); page.navigate(); time.sleep(5)
        assert page.wait_for_flutter()

    def test_resp_007_wide_2560_renders(self, driver):
        page = SplashPage(driver); page.set_viewport(2560, 1440); page.navigate(); time.sleep(5)
        assert page.wait_for_flutter()

    def test_resp_008_mobile_no_horizontal_scroll(self, driver):
        page = SplashPage(driver); page.set_viewport(375, 667); page.navigate(); time.sleep(5)
        overflow = page.execute_script("return document.documentElement.scrollWidth > document.documentElement.clientWidth;")
        assert not overflow

    def test_resp_009_tablet_no_horizontal_scroll(self, driver):
        page = SplashPage(driver); page.set_viewport(768, 1024); page.navigate(); time.sleep(5)
        overflow = page.execute_script("return document.documentElement.scrollWidth > document.documentElement.clientWidth;")
        assert not overflow

    def test_resp_010_desktop_no_horizontal_scroll(self, driver):
        page = SplashPage(driver); page.set_viewport(1920, 1080); page.navigate(); time.sleep(5)
        overflow = page.execute_script("return document.documentElement.scrollWidth > document.documentElement.clientWidth;")
        assert not overflow

    def test_resp_011_mobile_screenshot(self, driver):
        page = SplashPage(driver); page.set_viewport(375, 667); page.navigate(); time.sleep(5)
        p = page.take_screenshot("resp_mobile"); assert p and os.path.exists(p)

    def test_resp_012_tablet_screenshot(self, driver):
        page = SplashPage(driver); page.set_viewport(768, 1024); page.navigate(); time.sleep(5)
        p = page.take_screenshot("resp_tablet"); assert p and os.path.exists(p)

    def test_resp_013_desktop_screenshot(self, driver):
        page = SplashPage(driver); page.set_viewport(1920, 1080); page.navigate(); time.sleep(5)
        p = page.take_screenshot("resp_desktop"); assert p and os.path.exists(p)

    def test_resp_014_resize_mobile_to_desktop(self, driver):
        page = SplashPage(driver); page.set_viewport(375, 667); page.navigate(); time.sleep(3)
        page.set_viewport(1920, 1080); time.sleep(3)
        assert page.wait_for_flutter()

    def test_resp_015_resize_desktop_to_mobile(self, driver):
        page = SplashPage(driver); page.set_viewport(1920, 1080); page.navigate(); time.sleep(3)
        page.set_viewport(375, 667); time.sleep(3)
        assert page.wait_for_flutter()

    def test_resp_016_landscape_mode(self, driver):
        page = SplashPage(driver); page.set_viewport(896, 414); page.navigate(); time.sleep(5)
        assert page.wait_for_flutter()

    def test_resp_017_role_selection_mobile(self, driver):
        page = RoleSelectionPage(driver); page.set_viewport(375, 667)
        page.navigate(); time.sleep(5)
        assert page.is_loaded()

    def test_resp_018_role_selection_desktop(self, driver):
        page = RoleSelectionPage(driver); page.set_viewport(1920, 1080)
        page.navigate(); time.sleep(5)
        assert page.is_loaded()

    def test_resp_019_auth_page_mobile(self, driver):
        page = BystanderAuthPage(driver); page.set_viewport(375, 667)
        page.navigate(); time.sleep(5)
        assert page.is_loaded()

    def test_resp_020_all_viewports_cycle(self, driver):
        page = SplashPage(driver)
        for name, (w, h) in VIEWPORTS.items():
            page.set_viewport(w, h)
            page.navigate()
            time.sleep(2)
        assert page.wait_for_flutter()
