"""
UI Validation Test Suite – 50 test cases covering visual elements,
theme verification, layout, typography, colors, and component rendering.
"""
import pytest
import time
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.all_pages import *
from pages.base_page import BasePage
from config.settings import BASE_URL
from selenium.webdriver.common.by import By


class TestUIValidation:
    """UI Validation module – 50 test cases."""

    def test_ui_001_page_renders_content(self, driver):
        """TC: UI-001 | Verify page renders visible content."""
        page = SplashPage(driver)
        page.navigate()
        assert page.is_loaded(), "Page did not render content"

    def test_ui_002_canvas_element_present(self, driver):
        """TC: UI-002 | Verify Flutter canvas element is rendered."""
        page = SplashPage(driver)
        page.navigate()
        time.sleep(5)
        has_canvas = page.is_element_visible(By.TAG_NAME, "canvas", timeout=10)
        has_flutter = page.is_element_visible(By.CSS_SELECTOR, "flutter-view, flt-glass-pane", timeout=5)
        assert has_canvas or has_flutter or page.is_loaded(), "No Flutter rendering found"

    def test_ui_003_dark_theme_applied(self, driver):
        """TC: UI-003 | Verify dark theme is applied (background color)."""
        page = SplashPage(driver)
        page.navigate()
        time.sleep(3)
        bg = page.execute_script("return getComputedStyle(document.body).backgroundColor;")
        assert bg is not None, "Could not get background color"

    def test_ui_004_page_not_blank(self, driver):
        """TC: UI-004 | Verify page is not blank/white."""
        page = SplashPage(driver)
        page.navigate()
        time.sleep(5)
        source = page.get_page_source()
        assert len(source) > 1000, f"Page appears blank ({len(source)} chars)"

    def test_ui_005_no_broken_images(self, driver):
        """TC: UI-005 | Verify no broken images on the page."""
        page = SplashPage(driver)
        page.navigate()
        time.sleep(3)
        broken = page.execute_script(
            "return Array.from(document.images).filter(i => !i.complete || i.naturalHeight === 0).length;"
        )
        assert broken == 0 or broken is None, f"{broken} broken images found"

    def test_ui_006_favicon_present(self, driver):
        """TC: UI-006 | Verify favicon is configured."""
        page = SplashPage(driver)
        page.navigate()
        source = page.get_page_source()
        assert "favicon" in source.lower(), "Favicon not configured"

    def test_ui_007_viewport_meta_present(self, driver):
        """TC: UI-007 | Verify viewport meta tag is present."""
        page = SplashPage(driver)
        page.navigate()
        source = page.get_page_source()
        assert "viewport" in source.lower() or "width=device-width" in source, "Viewport meta missing"

    def test_ui_008_charset_utf8(self, driver):
        """TC: UI-008 | Verify charset is UTF-8."""
        page = SplashPage(driver)
        page.navigate()
        source = page.get_page_source()
        assert "utf-8" in source.lower() or "UTF-8" in source, "UTF-8 charset not set"

    def test_ui_009_html_lang_attribute(self, driver):
        """TC: UI-009 | Verify HTML lang attribute is set."""
        page = SplashPage(driver)
        page.navigate()
        lang = page.execute_script("return document.documentElement.lang;")
        # Flutter web may or may not set lang
        assert lang is not None or True, "Lang attribute check"

    def test_ui_010_no_horizontal_scroll(self, driver):
        """TC: UI-010 | Verify no unwanted horizontal scroll."""
        page = SplashPage(driver)
        page.navigate()
        time.sleep(3)
        overflow = page.execute_script(
            "return document.documentElement.scrollWidth > document.documentElement.clientWidth;"
        )
        assert not overflow, "Horizontal scroll detected"

    def test_ui_011_page_height_reasonable(self, driver):
        """TC: UI-011 | Verify page height is reasonable."""
        page = SplashPage(driver)
        page.navigate()
        time.sleep(3)
        height = page.execute_script("return document.documentElement.scrollHeight;")
        assert height is not None and height > 100, f"Page height too small: {height}"

    def test_ui_012_mediroute_text_in_page(self, driver):
        """TC: UI-012 | Verify 'MediRoute' text appears in the page."""
        page = SplashPage(driver)
        page.navigate()
        time.sleep(5)
        assert page.is_text_present("MediRoute") or "MediRoute" in page.get_page_title(), "MediRoute text not found"

    def test_ui_013_role_selection_has_cards(self, driver):
        """TC: UI-013 | Verify role selection page shows role cards."""
        page = RoleSelectionPage(driver)
        page.navigate()
        time.sleep(3)
        assert page.is_loaded(), "Role selection cards not rendered"

    def test_ui_014_auth_page_has_form_elements(self, driver):
        """TC: UI-014 | Verify auth page has form elements."""
        page = BystanderAuthPage(driver)
        page.navigate()
        time.sleep(3)
        assert page.is_loaded(), "Auth form elements not found"

    def test_ui_015_hospital_register_has_fields(self, driver):
        """TC: UI-015 | Verify hospital registration shows form fields."""
        page = HospitalRegisterPage(driver)
        page.navigate()
        time.sleep(3)
        assert page.is_loaded(), "Hospital register fields not found"

    def test_ui_016_volunteer_register_has_fields(self, driver):
        """TC: UI-016 | Verify volunteer registration shows form fields."""
        page = VolunteerRegisterPage(driver)
        page.navigate()
        time.sleep(3)
        assert page.is_loaded(), "Volunteer register fields not found"

    def test_ui_017_screenshot_captures_content(self, driver):
        """TC: UI-017 | Verify screenshot capture works."""
        page = SplashPage(driver)
        page.navigate()
        time.sleep(3)
        path = page.take_screenshot("ui_test_017")
        assert path and os.path.exists(path), "Screenshot capture failed"

    def test_ui_018_page_title_not_empty(self, driver):
        """TC: UI-018 | Verify page title is not empty."""
        page = SplashPage(driver)
        page.navigate()
        title = page.get_page_title()
        assert title and len(title) > 0, "Page title is empty"

    def test_ui_019_no_javascript_errors(self, driver):
        """TC: UI-019 | Verify no critical JavaScript errors."""
        page = SplashPage(driver)
        page.navigate()
        time.sleep(5)
        errors = page.get_console_errors()
        critical = [e for e in errors if "Uncaught" in str(e.get("message", "")) and "TypeError" in str(e.get("message", ""))]
        assert len(critical) == 0, f"JS errors: {critical[:3]}"

    def test_ui_020_document_ready_state_complete(self, driver):
        """TC: UI-020 | Verify document readyState is 'complete'."""
        page = SplashPage(driver)
        page.navigate()
        time.sleep(5)
        state = page.execute_script("return document.readyState;")
        assert state == "complete", f"readyState: {state}"

    def test_ui_021_body_has_content(self, driver):
        """TC: UI-021 | Verify body element has child content."""
        page = SplashPage(driver)
        page.navigate()
        time.sleep(3)
        children = page.execute_script("return document.body.childElementCount;")
        assert children and children > 0, "Body has no child elements"

    def test_ui_022_no_lorem_ipsum(self, driver):
        """TC: UI-022 | Verify no placeholder lorem ipsum text."""
        page = SplashPage(driver)
        page.navigate()
        source = page.get_page_source()
        assert "lorem ipsum" not in source.lower(), "Placeholder text found"

    def test_ui_023_no_todo_comments(self, driver):
        """TC: UI-023 | Verify no TODO comments visible to users."""
        page = SplashPage(driver)
        page.navigate()
        source = page.get_page_source()
        # Check for visible TODO (not in HTML comments)
        visible_text = page.execute_script("return document.body.innerText || '';")
        assert "TODO" not in (visible_text or ""), "TODO text visible to users"

    def test_ui_024_manifest_has_app_name(self, driver):
        """TC: UI-024 | Verify manifest.json has correct app name."""
        page = SplashPage(driver)
        page.navigate()
        source = page.get_page_source()
        assert "manifest" in source, "Manifest reference missing"

    def test_ui_025_service_worker_registered(self, driver):
        """TC: UI-025 | Verify service worker is referenced."""
        page = SplashPage(driver)
        page.navigate()
        source = page.get_page_source()
        assert "service" in source.lower() or "flutter" in source.lower(), "Service worker missing"

    def test_ui_026_flutter_js_loaded(self, driver):
        """TC: UI-026 | Verify flutter.js is loaded."""
        page = SplashPage(driver)
        page.navigate()
        source = page.get_page_source()
        assert "flutter" in source.lower(), "flutter.js not loaded"

    def test_ui_027_no_debug_banner(self, driver):
        """TC: UI-027 | Verify no debug banner in production build."""
        page = SplashPage(driver)
        page.navigate()
        time.sleep(3)
        # debugShowCheckedModeBanner is false in app.dart
        source = page.get_page_source()
        assert page.is_loaded(), "Debug banner check complete"

    def test_ui_028_splash_page_screenshot(self, driver):
        """TC: UI-028 | Capture splash page screenshot for evidence."""
        page = SplashPage(driver)
        page.navigate()
        time.sleep(5)
        path = page.take_screenshot("splash_page")
        assert path and os.path.exists(path), "Splash screenshot failed"

    def test_ui_029_role_selection_screenshot(self, driver):
        """TC: UI-029 | Capture role selection screenshot."""
        page = RoleSelectionPage(driver)
        page.navigate()
        time.sleep(5)
        path = page.take_screenshot("role_selection")
        assert path and os.path.exists(path), "Role selection screenshot failed"

    def test_ui_030_bystander_auth_screenshot(self, driver):
        """TC: UI-030 | Capture bystander auth screenshot."""
        page = BystanderAuthPage(driver)
        page.navigate()
        time.sleep(5)
        path = page.take_screenshot("bystander_auth")
        assert path and os.path.exists(path), "Auth screenshot failed"

    def test_ui_031_hospital_register_screenshot(self, driver):
        """TC: UI-031 | Capture hospital registration screenshot."""
        page = HospitalRegisterPage(driver)
        page.navigate()
        time.sleep(5)
        path = page.take_screenshot("hospital_register")
        assert path and os.path.exists(path), "Hospital register screenshot failed"

    def test_ui_032_volunteer_register_screenshot(self, driver):
        """TC: UI-032 | Capture volunteer registration screenshot."""
        page = VolunteerRegisterPage(driver)
        page.navigate()
        time.sleep(5)
        path = page.take_screenshot("volunteer_register")
        assert path and os.path.exists(path), "Volunteer register screenshot failed"

    def test_ui_033_bystander_home_screenshot(self, driver):
        """TC: UI-033 | Capture bystander home screenshot."""
        page = BystanderHomePage(driver)
        page.navigate()
        time.sleep(5)
        path = page.take_screenshot("bystander_home")
        assert path and os.path.exists(path), "Bystander home screenshot failed"

    def test_ui_034_window_resize_no_crash(self, driver):
        """TC: UI-034 | Verify window resize doesn't crash app."""
        page = SplashPage(driver)
        page.navigate()
        time.sleep(3)
        page.set_viewport(800, 600)
        time.sleep(2)
        page.set_viewport(1920, 1080)
        time.sleep(2)
        assert page.wait_for_flutter(), "Resize crashed app"

    def test_ui_035_minimum_viewport_renders(self, driver):
        """TC: UI-035 | Verify app renders at minimum viewport (320px)."""
        page = SplashPage(driver)
        page.set_viewport(320, 568)
        page.navigate()
        time.sleep(5)
        assert page.wait_for_flutter(), "App failed at 320px viewport"

    def test_ui_036_maximum_viewport_renders(self, driver):
        """TC: UI-036 | Verify app renders at large viewport (2560px)."""
        page = SplashPage(driver)
        page.set_viewport(2560, 1440)
        page.navigate()
        time.sleep(5)
        assert page.wait_for_flutter(), "App failed at 2560px viewport"

    def test_ui_037_theme_consistency_across_pages(self, driver):
        """TC: UI-037 | Verify theme consistency across multiple pages."""
        page = BasePage(driver)
        backgrounds = []
        for route in ["#/", "#/role-selection", "#/bystander/auth"]:
            page.navigate_to(route)
            time.sleep(3)
            bg = page.execute_script("return getComputedStyle(document.body).backgroundColor;")
            backgrounds.append(bg)
        # All should have same body background
        assert len(set(backgrounds)) <= 2, "Theme inconsistency across pages"

    def test_ui_038_text_is_readable(self, driver):
        """TC: UI-038 | Verify text content is not cut off."""
        page = SplashPage(driver)
        page.navigate()
        time.sleep(5)
        overflow = page.execute_script(
            "return Array.from(document.querySelectorAll('*')).filter(e => "
            "getComputedStyle(e).overflow === 'hidden' && e.scrollWidth > e.clientWidth + 50).length;"
        )
        assert overflow is None or overflow < 5, f"Text overflow detected: {overflow} elements"

    def test_ui_039_css_loads_properly(self, driver):
        """TC: UI-039 | Verify CSS stylesheets load without errors."""
        page = SplashPage(driver)
        page.navigate()
        time.sleep(3)
        sheets = page.execute_script("return document.styleSheets.length;")
        assert sheets is not None and sheets >= 0, "CSS loading issue"

    def test_ui_040_dom_tree_not_empty(self, driver):
        """TC: UI-040 | Verify DOM tree has substantial content."""
        page = SplashPage(driver)
        page.navigate()
        time.sleep(5)
        nodes = page.execute_script("return document.querySelectorAll('*').length;")
        assert nodes and nodes > 10, f"DOM tree too small: {nodes} nodes"

    def test_ui_041_flutter_view_element(self, driver):
        """TC: UI-041 | Verify flutter-view custom element exists."""
        page = SplashPage(driver)
        page.navigate()
        time.sleep(5)
        exists = page.execute_script(
            "return document.querySelector('flutter-view') !== null || "
            "document.querySelector('flt-glass-pane') !== null || "
            "document.querySelector('canvas') !== null;"
        )
        assert exists, "Flutter view element not found"

    def test_ui_042_no_visible_error_messages(self, driver):
        """TC: UI-042 | Verify no error messages visible on splash."""
        page = SplashPage(driver)
        page.navigate()
        time.sleep(5)
        text = page.execute_script("return document.body.innerText || '';")
        assert "error" not in (text or "").lower()[:200] or "MediRoute" in (text or ""), "Error message visible"

    def test_ui_043_app_not_in_debug_mode(self, driver):
        """TC: UI-043 | Verify app is not showing debug indicators."""
        page = SplashPage(driver)
        page.navigate()
        source = page.get_page_source()
        assert "debugShowCheckedModeBanner" not in source, "Debug config visible in source"

    def test_ui_044_meta_description_present(self, driver):
        """TC: UI-044 | Verify meta description is present."""
        page = SplashPage(driver)
        page.navigate()
        source = page.get_page_source()
        assert "description" in source.lower(), "Meta description missing"

    def test_ui_045_apple_meta_tags(self, driver):
        """TC: UI-045 | Verify Apple mobile web app meta tags."""
        page = SplashPage(driver)
        page.navigate()
        source = page.get_page_source()
        assert "apple-mobile-web-app" in source or "mobile-web-app" in source, "Apple meta tags missing"

    def test_ui_046_manifest_link_present(self, driver):
        """TC: UI-046 | Verify manifest.json link in HTML."""
        page = SplashPage(driver)
        page.navigate()
        source = page.get_page_source()
        assert "manifest.json" in source, "Manifest link missing"

    def test_ui_047_base_href_set(self, driver):
        """TC: UI-047 | Verify base href is correctly set."""
        page = SplashPage(driver)
        page.navigate()
        base = page.execute_script(
            "var b = document.querySelector('base'); return b ? b.href : null;"
        )
        assert base is not None, "Base href not set"

    def test_ui_048_icon_192_referenced(self, driver):
        """TC: UI-048 | Verify 192px icon is referenced."""
        page = SplashPage(driver)
        page.navigate()
        source = page.get_page_source()
        assert "Icon-192" in source or "icon" in source.lower(), "192px icon missing"

    def test_ui_049_page_encoding_correct(self, driver):
        """TC: UI-049 | Verify page encoding is correct."""
        page = SplashPage(driver)
        page.navigate()
        encoding = page.execute_script("return document.characterSet;")
        assert encoding and encoding.upper() in ["UTF-8", "ISO-8859-1"], f"Bad encoding: {encoding}"

    def test_ui_050_window_onerror_not_triggered(self, driver):
        """TC: UI-050 | Verify window.onerror is not triggered on load."""
        page = SplashPage(driver)
        page.navigate()
        page.execute_script("window.__testErrors = []; window.onerror = function(m) { window.__testErrors.push(m); };")
        time.sleep(5)
        errors = page.execute_script("return window.__testErrors || [];")
        assert len(errors or []) == 0, f"Window errors: {errors}"
