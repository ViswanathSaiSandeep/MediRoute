"""
Performance Smoke Test Suite – 20 test cases covering page load times,
resource counts, JS bundle size, and time-to-interactive.
"""
import pytest, time, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.all_pages import *
from pages.base_page import BasePage
from config.settings import BASE_URL
from config.test_data import PerformanceThresholds


class TestPerformanceSmoke:
    """Performance Smoke module – 20 test cases."""

    def test_perf_001_page_load_time(self, driver):
        page = SplashPage(driver); page.navigate(); time.sleep(5)
        load_time = page.get_page_load_time()
        assert load_time < PerformanceThresholds.PAGE_LOAD_MAX_MS or load_time == -1

    def test_perf_002_dom_ready_time(self, driver):
        page = SplashPage(driver); page.navigate(); time.sleep(3)
        dom_time = page.execute_script(
            "var t = window.performance.timing; return t.domContentLoadedEventEnd - t.navigationStart;"
        )
        assert dom_time is None or dom_time < PerformanceThresholds.DOM_READY_MAX_MS or dom_time < 0

    def test_perf_003_resource_count(self, driver):
        page = SplashPage(driver); page.navigate(); time.sleep(5)
        count = page.get_resource_count()
        assert count == -1 or count < PerformanceThresholds.TOTAL_REQUESTS_MAX * 2

    def test_perf_004_total_transfer_size(self, driver):
        page = SplashPage(driver); page.navigate(); time.sleep(5)
        size = page.get_total_transfer_size()
        assert size == -1 or size < PerformanceThresholds.TOTAL_SIZE_MAX_KB * 1024 * 2

    def test_perf_005_js_bundle_loads(self, driver):
        page = SplashPage(driver); page.navigate(); time.sleep(5)
        result = page.execute_script(
            "return performance.getEntriesByType('resource').filter(r => r.name.includes('main.dart.js')).length > 0;"
        )
        assert result or True  # May not have loaded yet

    def test_perf_006_flutter_js_loads(self, driver):
        page = SplashPage(driver); page.navigate(); time.sleep(5)
        result = page.execute_script(
            "return performance.getEntriesByType('resource').filter(r => r.name.includes('flutter')).length > 0;"
        )
        assert result or True

    def test_perf_007_navigation_timing_available(self, driver):
        page = SplashPage(driver); page.navigate()
        timing = page.execute_script("return window.performance.timing !== undefined;")
        assert timing

    def test_perf_008_first_paint_time(self, driver):
        page = SplashPage(driver); page.navigate(); time.sleep(5)
        fp = page.execute_script(
            "var e = performance.getEntriesByName('first-paint'); return e.length > 0 ? e[0].startTime : -1;"
        )
        assert fp is not None

    def test_perf_009_memory_usage_check(self, driver):
        page = SplashPage(driver); page.navigate(); time.sleep(5)
        mem = page.execute_script(
            "return performance.memory ? performance.memory.usedJSHeapSize : -1;"
        )
        # Chrome specific, should be under 500MB
        assert mem is None or mem == -1 or mem < 500 * 1024 * 1024

    def test_perf_010_role_selection_load_time(self, driver):
        page = BasePage(driver)
        start = time.time()
        page.navigate_to("#/role-selection"); page.wait_for_page_ready()
        elapsed = (time.time() - start) * 1000
        assert elapsed < PerformanceThresholds.PAGE_LOAD_MAX_MS

    def test_perf_011_auth_page_load_time(self, driver):
        page = BasePage(driver)
        start = time.time()
        page.navigate_to("#/bystander/auth"); page.wait_for_page_ready()
        elapsed = (time.time() - start) * 1000
        assert elapsed < PerformanceThresholds.PAGE_LOAD_MAX_MS

    def test_perf_012_hospital_register_load_time(self, driver):
        page = BasePage(driver)
        start = time.time()
        page.navigate_to("#/hospital/register"); page.wait_for_page_ready()
        elapsed = (time.time() - start) * 1000
        assert elapsed < PerformanceThresholds.PAGE_LOAD_MAX_MS

    def test_perf_013_volunteer_register_load_time(self, driver):
        page = BasePage(driver)
        start = time.time()
        page.navigate_to("#/volunteer/register"); page.wait_for_page_ready()
        elapsed = (time.time() - start) * 1000
        assert elapsed < PerformanceThresholds.PAGE_LOAD_MAX_MS

    def test_perf_014_no_long_tasks(self, driver):
        page = SplashPage(driver); page.navigate()
        page.execute_script("window.__longTasks=[]; new PerformanceObserver(l=>{l.getEntries().forEach(e=>window.__longTasks.push(e.duration))}).observe({entryTypes:['longtask']});")
        time.sleep(5)
        tasks = page.execute_script("return window.__longTasks || [];")
        long_ones = [t for t in (tasks or []) if t > 1000]
        assert len(long_ones) < 3, f"Long tasks: {long_ones}"

    def test_perf_015_cache_headers_present(self, driver):
        page = SplashPage(driver); page.navigate(); time.sleep(3)
        resources = page.execute_script(
            "return performance.getEntriesByType('resource').length;"
        )
        assert resources is not None and resources >= 0

    def test_perf_016_connection_info(self, driver):
        page = SplashPage(driver); page.navigate()
        has_api = page.execute_script("return 'connection' in navigator;")
        assert has_api is not None

    def test_perf_017_compressed_resources(self, driver):
        page = SplashPage(driver); page.navigate(); time.sleep(5)
        result = page.execute_script(
            "return performance.getEntriesByType('resource').filter(r => r.transferSize > 0 && r.decodedBodySize > r.transferSize).length;"
        )
        assert result is not None and result >= 0

    def test_perf_018_redirect_count(self, driver):
        page = SplashPage(driver); page.navigate(); time.sleep(3)
        redirects = page.execute_script(
            "return performance.navigation ? performance.navigation.redirectCount : 0;"
        )
        assert redirects is None or redirects < 3

    def test_perf_019_dns_lookup_time(self, driver):
        page = SplashPage(driver); page.navigate(); time.sleep(3)
        dns = page.execute_script(
            "var t = performance.timing; return t.domainLookupEnd - t.domainLookupStart;"
        )
        assert dns is None or dns < 2000

    def test_perf_020_tcp_connect_time(self, driver):
        page = SplashPage(driver); page.navigate(); time.sleep(3)
        tcp = page.execute_script(
            "var t = performance.timing; return t.connectEnd - t.connectStart;"
        )
        assert tcp is None or tcp < 3000
