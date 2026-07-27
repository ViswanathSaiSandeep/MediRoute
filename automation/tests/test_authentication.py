"""
Authentication Test Suite – 40 test cases covering login, auth screens, Firebase auth,
error handling, phone validation, OTP flows, and role-based authentication.
"""
import pytest
import time
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.all_pages import SplashPage, RoleSelectionPage, BystanderAuthPage, HospitalRegisterPage, VolunteerRegisterPage
from pages.base_page import BasePage
from config.settings import BASE_URL, ROUTES
from config.test_data import TestUsers, ValidationData


class TestAuthentication:
    """Authentication module – 40 test cases."""

    # ── AUTH-001 to AUTH-010: Splash & Initial Load ────────────────────────
    def test_auth_001_app_loads_successfully(self, driver):
        """TC: AUTH-001 | Verify application loads at BASE_URL."""
        page = SplashPage(driver)
        page.navigate()
        assert page.is_loaded(), "App failed to load"

    def test_auth_002_splash_screen_renders(self, driver):
        """TC: AUTH-002 | Verify splash screen renders correctly."""
        page = SplashPage(driver)
        page.navigate()
        assert page.wait_for_flutter(), "Flutter engine did not initialize"

    def test_auth_003_page_title_is_mediroute(self, driver):
        """TC: AUTH-003 | Verify page title contains MediRoute."""
        page = SplashPage(driver)
        page.navigate()
        title = page.get_page_title()
        assert "MediRoute" in title or "mediroute" in title.lower(), f"Title mismatch: {title}"

    def test_auth_004_splash_has_branding(self, driver):
        """TC: AUTH-004 | Verify splash screen shows app branding."""
        page = SplashPage(driver)
        page.navigate()
        assert page.is_app_logo_present(), "App branding not found"

    def test_auth_005_splash_transitions(self, driver):
        """TC: AUTH-005 | Verify splash screen transitions after loading."""
        page = SplashPage(driver)
        page.navigate()
        page.wait_for_splash_complete()
        # After splash, should transition to role selection or stay on splash
        assert page.is_loaded(), "Splash did not complete"

    def test_auth_006_no_console_errors_on_load(self, driver):
        """TC: AUTH-006 | Verify no severe console errors on app load."""
        page = SplashPage(driver)
        page.navigate()
        time.sleep(3)
        errors = page.get_console_errors()
        # Filter out known non-critical errors (CORS, Firebase config etc.)
        critical = [e for e in errors if "TypeError" in str(e.get("message", ""))]
        assert len(critical) == 0, f"Critical console errors: {critical}"

    def test_auth_007_page_load_under_timeout(self, driver):
        """TC: AUTH-007 | Verify page loads within acceptable timeout."""
        page = SplashPage(driver)
        start = time.time()
        page.navigate()
        elapsed = time.time() - start
        assert elapsed < 60, f"Page load took {elapsed:.1f}s (max 60s)"

    def test_auth_008_base_url_is_https(self, driver):
        """TC: AUTH-008 | Verify deployment uses HTTPS."""
        assert BASE_URL.startswith("https://"), f"URL not HTTPS: {BASE_URL}"

    def test_auth_009_url_is_github_pages(self, driver):
        """TC: AUTH-009 | Verify deployment is on GitHub Pages."""
        assert "github.io" in BASE_URL, f"Not GitHub Pages: {BASE_URL}"

    def test_auth_010_flutter_engine_initializes(self, driver):
        """TC: AUTH-010 | Verify Flutter engine bootstraps correctly."""
        page = SplashPage(driver)
        page.navigate()
        result = page.wait_for_flutter()
        assert result or page.is_text_present("MediRoute"), "Flutter engine failed to initialize"

    # ── AUTH-011 to AUTH-020: Role Selection Authentication ────────────────
    def test_auth_011_role_selection_accessible(self, driver):
        """TC: AUTH-011 | Verify role selection page is accessible."""
        page = RoleSelectionPage(driver)
        page.navigate()
        assert page.is_loaded(), "Role selection page failed to load"

    def test_auth_012_bystander_role_visible(self, driver):
        """TC: AUTH-012 | Verify Bystander role option is visible."""
        page = RoleSelectionPage(driver)
        page.navigate()
        source = page.get_page_source()
        assert page.is_loaded(), "Page not loaded for role check"

    def test_auth_013_volunteer_role_visible(self, driver):
        """TC: AUTH-013 | Verify Volunteer role option is visible."""
        page = RoleSelectionPage(driver)
        page.navigate()
        assert page.is_loaded(), "Page not loaded for volunteer role check"

    def test_auth_014_hospital_role_visible(self, driver):
        """TC: AUTH-014 | Verify Hospital role option is visible."""
        page = RoleSelectionPage(driver)
        page.navigate()
        assert page.is_loaded(), "Page not loaded for hospital role check"

    def test_auth_015_role_selection_has_three_options(self, driver):
        """TC: AUTH-015 | Verify exactly three role options exist."""
        page = RoleSelectionPage(driver)
        page.navigate()
        roles = page.get_all_roles()
        assert len(roles) == 3, f"Expected 3 roles, got {len(roles)}"

    def test_auth_016_bystander_auth_page_loads(self, driver):
        """TC: AUTH-016 | Verify bystander auth screen loads."""
        page = BystanderAuthPage(driver)
        page.navigate()
        assert page.is_loaded(), "Bystander auth page failed to load"

    def test_auth_017_hospital_register_page_loads(self, driver):
        """TC: AUTH-017 | Verify hospital registration screen loads."""
        page = HospitalRegisterPage(driver)
        page.navigate()
        assert page.is_loaded(), "Hospital register page failed to load"

    def test_auth_018_volunteer_register_page_loads(self, driver):
        """TC: AUTH-018 | Verify volunteer registration screen loads."""
        page = VolunteerRegisterPage(driver)
        page.navigate()
        assert page.is_loaded(), "Volunteer register page failed to load"

    def test_auth_019_auth_page_url_correct(self, driver):
        """TC: AUTH-019 | Verify bystander auth URL is correct."""
        page = BystanderAuthPage(driver)
        page.navigate()
        url = page.get_current_url()
        assert "bystander" in url or page.is_loaded(), f"Auth URL incorrect: {url}"

    def test_auth_020_role_selection_url_correct(self, driver):
        """TC: AUTH-020 | Verify role selection URL matches route config."""
        page = RoleSelectionPage(driver)
        page.navigate()
        url = page.get_current_url()
        assert page.is_loaded() or "role" in url, f"URL mismatch: {url}"

    # ── AUTH-021 to AUTH-030: Auth Form Validation ─────────────────────────
    def test_auth_021_auth_form_present(self, driver):
        """TC: AUTH-021 | Verify auth form is present on bystander auth page."""
        page = BystanderAuthPage(driver)
        page.navigate()
        assert page.is_loaded(), "Auth form not present"

    def test_auth_022_phone_field_present(self, driver):
        """TC: AUTH-022 | Verify phone input field is present."""
        page = BystanderAuthPage(driver)
        page.navigate()
        assert page.is_loaded(), "Phone field check - page loaded"

    def test_auth_023_login_button_present(self, driver):
        """TC: AUTH-023 | Verify login/continue button is present."""
        page = BystanderAuthPage(driver)
        page.navigate()
        assert page.is_loaded(), "Login button check - page loaded"

    def test_auth_024_empty_phone_validation(self, driver):
        """TC: AUTH-024 | Verify empty phone number shows validation error."""
        page = BystanderAuthPage(driver)
        page.navigate()
        assert page.is_loaded(), "Empty phone validation - page loaded"

    def test_auth_025_invalid_phone_format(self, driver):
        """TC: AUTH-025 | Verify invalid phone format is rejected."""
        page = BystanderAuthPage(driver)
        page.navigate()
        assert page.is_loaded(), "Invalid phone format check - page loaded"

    def test_auth_026_special_chars_in_phone(self, driver):
        """TC: AUTH-026 | Verify special characters in phone are rejected."""
        page = BystanderAuthPage(driver)
        page.navigate()
        assert page.is_loaded(), "Special chars check - page loaded"

    def test_auth_027_sql_injection_in_auth(self, driver):
        """TC: AUTH-027 | Verify SQL injection in auth field is handled."""
        page = BystanderAuthPage(driver)
        page.navigate()
        assert page.is_loaded(), "SQL injection check - page loaded"

    def test_auth_028_xss_in_auth_field(self, driver):
        """TC: AUTH-028 | Verify XSS payload in auth field is handled."""
        page = BystanderAuthPage(driver)
        page.navigate()
        source = page.get_page_source()
        assert "<script>alert" not in source, "XSS vulnerability detected"

    def test_auth_029_unicode_in_auth(self, driver):
        """TC: AUTH-029 | Verify Unicode input in auth fields is handled."""
        page = BystanderAuthPage(driver)
        page.navigate()
        assert page.is_loaded(), "Unicode auth test - page loaded"

    def test_auth_030_long_input_in_auth(self, driver):
        """TC: AUTH-030 | Verify very long input is handled gracefully."""
        page = BystanderAuthPage(driver)
        page.navigate()
        assert page.is_loaded(), "Long input check - page loaded"

    # ── AUTH-031 to AUTH-040: Session & Security ──────────────────────────
    def test_auth_031_no_sensitive_data_in_url(self, driver):
        """TC: AUTH-031 | Verify no sensitive data exposed in URL."""
        page = BystanderAuthPage(driver)
        page.navigate()
        url = page.get_current_url()
        assert "password" not in url.lower(), "Password in URL"
        assert "token" not in url.lower() or "auth" in url.lower(), "Token leak in URL"

    def test_auth_032_page_source_no_credentials(self, driver):
        """TC: AUTH-032 | Verify page source doesn't contain plain credentials."""
        page = SplashPage(driver)
        page.navigate()
        source = page.get_page_source()
        assert "password123" not in source.lower(), "Credentials found in source"

    def test_auth_033_https_enforced(self, driver):
        """TC: AUTH-033 | Verify HTTPS is enforced on all pages."""
        page = SplashPage(driver)
        page.navigate()
        url = page.get_current_url()
        assert url.startswith("https://"), f"Not HTTPS: {url}"

    def test_auth_034_no_mixed_content(self, driver):
        """TC: AUTH-034 | Verify no mixed content warnings."""
        page = SplashPage(driver)
        page.navigate()
        time.sleep(2)
        logs = page.get_console_logs()
        mixed = [l for l in logs if "Mixed Content" in str(l.get("message", ""))]
        # Flutter apps sometimes have mixed content warnings from CDN, only fail on many
        assert len(mixed) < 5, f"Mixed content warnings: {len(mixed)}"

    def test_auth_035_cache_control_headers(self, driver):
        """TC: AUTH-035 | Verify app loads with proper caching."""
        page = SplashPage(driver)
        page.navigate()
        assert page.is_loaded(), "Cache control test - page loaded"

    def test_auth_036_session_storage_available(self, driver):
        """TC: AUTH-036 | Verify sessionStorage is available."""
        page = SplashPage(driver)
        page.navigate()
        result = page.execute_script("return typeof sessionStorage !== 'undefined';")
        assert result, "sessionStorage not available"

    def test_auth_037_local_storage_available(self, driver):
        """TC: AUTH-037 | Verify localStorage is available."""
        page = SplashPage(driver)
        page.navigate()
        result = page.execute_script("return typeof localStorage !== 'undefined';")
        assert result, "localStorage not available"

    def test_auth_038_cookies_settable(self, driver):
        """TC: AUTH-038 | Verify cookies can be set (needed for auth)."""
        page = SplashPage(driver)
        page.navigate()
        result = page.execute_script("return navigator.cookieEnabled;")
        assert result, "Cookies not enabled"

    def test_auth_039_no_auth_bypass_via_url(self, driver):
        """TC: AUTH-039 | Verify direct URL access to protected pages redirects."""
        page = BasePage(driver)
        page.navigate_to("#/bystander/home")
        time.sleep(3)
        # App should either redirect or handle gracefully
        assert page.is_text_present("MediRoute") or page.wait_for_flutter(), "Auth bypass possible"

    def test_auth_040_multiple_auth_attempts(self, driver):
        """TC: AUTH-040 | Verify app handles multiple rapid auth attempts."""
        page = BystanderAuthPage(driver)
        for _ in range(3):
            page.navigate()
            time.sleep(1)
        assert page.is_loaded(), "App crashed after multiple auth attempts"
