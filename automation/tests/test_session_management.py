"""
Session Management Test Suite – 20 test cases covering localStorage,
sessionStorage, cookies, tab behavior, and state persistence.
"""
import pytest, time, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.all_pages import *
from pages.base_page import BasePage
from config.settings import BASE_URL


class TestSessionManagement:
    """Session Management module – 20 test cases."""

    def test_session_001_localstorage_works(self, driver):
        page = SplashPage(driver); page.navigate()
        page.execute_script("localStorage.setItem('test_key', 'test_value');")
        val = page.execute_script("return localStorage.getItem('test_key');")
        assert val == "test_value"

    def test_session_002_sessionstorage_works(self, driver):
        page = SplashPage(driver); page.navigate()
        page.execute_script("sessionStorage.setItem('test_key', 'test_value');")
        val = page.execute_script("return sessionStorage.getItem('test_key');")
        assert val == "test_value"

    def test_session_003_cookies_enabled(self, driver):
        page = SplashPage(driver); page.navigate()
        assert page.execute_script("return navigator.cookieEnabled;")

    def test_session_004_localstorage_persists_across_nav(self, driver):
        page = BasePage(driver); page.navigate_to("")
        page.execute_script("localStorage.setItem('persist_test', 'hello');")
        page.navigate_to("#/role-selection"); time.sleep(2)
        val = page.execute_script("return localStorage.getItem('persist_test');")
        assert val == "hello"

    def test_session_005_sessionstorage_persists_in_tab(self, driver):
        page = BasePage(driver); page.navigate_to("")
        page.execute_script("sessionStorage.setItem('tab_test', 'value');")
        page.navigate_to("#/role-selection"); time.sleep(2)
        val = page.execute_script("return sessionStorage.getItem('tab_test');")
        assert val == "value"

    def test_session_006_localstorage_survives_refresh(self, driver):
        page = SplashPage(driver); page.navigate()
        page.execute_script("localStorage.setItem('refresh_test', 'data');")
        page.refresh(); time.sleep(3)
        val = page.execute_script("return localStorage.getItem('refresh_test');")
        assert val == "data"

    def test_session_007_localstorage_clearable(self, driver):
        page = SplashPage(driver); page.navigate()
        page.execute_script("localStorage.setItem('clear_test', 'val');")
        page.execute_script("localStorage.removeItem('clear_test');")
        val = page.execute_script("return localStorage.getItem('clear_test');")
        assert val is None

    def test_session_008_sessionstorage_clearable(self, driver):
        page = SplashPage(driver); page.navigate()
        page.execute_script("sessionStorage.setItem('clear_test', 'val');")
        page.execute_script("sessionStorage.clear();")
        val = page.execute_script("return sessionStorage.getItem('clear_test');")
        assert val is None

    def test_session_009_localstorage_quota(self, driver):
        page = SplashPage(driver); page.navigate()
        # Verify we can store at least 1KB
        data = "x" * 1024
        page.execute_script(f"localStorage.setItem('quota_test', '{data}');")
        val = page.execute_script("return localStorage.getItem('quota_test');")
        assert val and len(val) >= 1024

    def test_session_010_history_length_tracks(self, driver):
        page = BasePage(driver); page.navigate_to("")
        initial = page.execute_script("return window.history.length;")
        page.navigate_to("#/role-selection"); time.sleep(2)
        after = page.execute_script("return window.history.length;")
        assert after >= initial

    def test_session_011_back_forward_cache(self, driver):
        page = BasePage(driver)
        page.navigate_to("#/"); time.sleep(2)
        page.navigate_to("#/role-selection"); time.sleep(2)
        page.go_back(); time.sleep(2)
        assert page.wait_for_flutter()

    def test_session_012_window_name_accessible(self, driver):
        page = SplashPage(driver); page.navigate()
        name = page.execute_script("return typeof window.name;")
        assert name == "string"

    def test_session_013_page_visibility_api(self, driver):
        page = SplashPage(driver); page.navigate()
        state = page.execute_script("return document.visibilityState;")
        assert state in ["visible", "hidden", "prerender"]

    def test_session_014_performance_api_available(self, driver):
        page = SplashPage(driver); page.navigate()
        avail = page.execute_script("return typeof window.performance !== 'undefined';")
        assert avail

    def test_session_015_indexeddb_available(self, driver):
        page = SplashPage(driver); page.navigate()
        avail = page.execute_script("return typeof window.indexedDB !== 'undefined';")
        assert avail

    def test_session_016_service_worker_api(self, driver):
        page = SplashPage(driver); page.navigate()
        avail = page.execute_script("return 'serviceWorker' in navigator;")
        assert avail

    def test_session_017_multiple_localstorage_keys(self, driver):
        page = SplashPage(driver); page.navigate()
        for i in range(10):
            page.execute_script(f"localStorage.setItem('multi_{i}', 'val_{i}');")
        for i in range(10):
            val = page.execute_script(f"return localStorage.getItem('multi_{i}');")
            assert val == f"val_{i}"

    def test_session_018_json_in_localstorage(self, driver):
        page = SplashPage(driver); page.navigate()
        page.execute_script('localStorage.setItem("json_test", JSON.stringify({a:1,b:2}));')
        val = page.execute_script('return JSON.parse(localStorage.getItem("json_test"));')
        assert val and val.get("a") == 1

    def test_session_019_localstorage_unicode(self, driver):
        page = SplashPage(driver); page.navigate()
        page.execute_script("localStorage.setItem('unicode', '测试');")
        val = page.execute_script("return localStorage.getItem('unicode');")
        assert val == "测试"

    def test_session_020_cleanup_test_data(self, driver):
        page = SplashPage(driver); page.navigate()
        page.execute_script("localStorage.clear(); sessionStorage.clear();")
        count = page.execute_script("return localStorage.length;")
        assert count == 0
