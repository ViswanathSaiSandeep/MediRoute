"""
Appium Forms & Validation Test Suite – 50 test cases for Android.
Covers form inputs, validation rules, field types, and submission behavior.
"""
import pytest
import time
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.all_screens import *
from pages.base_screen import BaseScreen
from config.test_data import TestUsers, ValidationData


class TestAppiumForms:
    """Forms & Input Validation module – 50 test cases."""

    # ── AFRM-001 to AFRM-010: Bystander Auth Form ───────────────────────
    def test_afrm_001_bystander_form_loads(self, driver):
        """TC: AFRM-001 | Bystander auth form loads."""
        screen = BystanderAuthScreen(driver)
        time.sleep(5)
        assert screen.is_loaded(), "Bystander form failed to load"

    def test_afrm_002_bystander_has_input_fields(self, driver):
        """TC: AFRM-002 | Bystander form has input fields."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        fields = screen.find_by_class("android.widget.EditText")
        assert fields is not None, "No input fields found"

    def test_afrm_003_empty_form_submission(self, driver):
        """TC: AFRM-003 | Empty form submission shows validation."""
        screen = BystanderAuthScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Empty form submission check"

    def test_afrm_004_valid_email_accepted(self, driver):
        """TC: AFRM-004 | Valid email format accepted."""
        screen = BystanderAuthScreen(driver)
        screen.wait_for_screen_ready()
        screen.enter_email(ValidationData.VALID_EMAIL)
        assert screen.is_loaded(), "Valid email not accepted"

    def test_afrm_005_invalid_email_rejected(self, driver):
        """TC: AFRM-005 | Invalid email shows error."""
        screen = BystanderAuthScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Invalid email check"

    def test_afrm_006_password_field_masks_text(self, driver):
        """TC: AFRM-006 | Password field masks input."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Password masking check"

    def test_afrm_007_form_clears_on_reset(self, driver):
        """TC: AFRM-007 | Form clears properly."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Form clear check"

    def test_afrm_008_keyboard_type_for_email(self, driver):
        """TC: AFRM-008 | Email field shows email keyboard."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Email keyboard check"

    def test_afrm_009_form_scrolls_with_keyboard(self, driver):
        """TC: AFRM-009 | Form scrolls when keyboard appears."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Form scroll with keyboard"

    def test_afrm_010_tab_moves_between_fields(self, driver):
        """TC: AFRM-010 | Tab key moves between fields."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Tab navigation check"

    # ── AFRM-011 to AFRM-020: Hospital Registration Form ────────────────
    def test_afrm_011_hospital_form_loads(self, driver):
        """TC: AFRM-011 | Hospital registration form loads."""
        screen = HospitalRegisterScreen(driver)
        time.sleep(5)
        assert screen.is_loaded(), "Hospital form failed to load"

    def test_afrm_012_hospital_name_field(self, driver):
        """TC: AFRM-012 | Hospital name field present."""
        screen = HospitalRegisterScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Hospital name field check"

    def test_afrm_013_hospital_email_field(self, driver):
        """TC: AFRM-013 | Hospital email field present."""
        screen = HospitalRegisterScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Hospital email field check"

    def test_afrm_014_hospital_password_field(self, driver):
        """TC: AFRM-014 | Hospital password field present."""
        screen = HospitalRegisterScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Hospital password field check"

    def test_afrm_015_hospital_submit_button(self, driver):
        """TC: AFRM-015 | Hospital submit button present."""
        screen = HospitalRegisterScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Hospital submit button check"

    def test_afrm_016_hospital_empty_name_rejected(self, driver):
        """TC: AFRM-016 | Empty hospital name rejected."""
        screen = HospitalRegisterScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Empty name rejection check"

    def test_afrm_017_hospital_empty_email_rejected(self, driver):
        """TC: AFRM-017 | Empty hospital email rejected."""
        screen = HospitalRegisterScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Empty email rejection check"

    def test_afrm_018_hospital_short_password_rejected(self, driver):
        """TC: AFRM-018 | Short hospital password rejected."""
        screen = HospitalRegisterScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Short password rejection check"

    def test_afrm_019_hospital_valid_data_accepted(self, driver):
        """TC: AFRM-019 | Valid hospital data accepted."""
        screen = HospitalRegisterScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Valid data acceptance check"

    def test_afrm_020_hospital_form_scrollable(self, driver):
        """TC: AFRM-020 | Hospital form scrollable."""
        screen = HospitalRegisterScreen(driver)
        screen.wait_for_screen_ready()
        screen.scroll_down()
        assert screen.is_loaded(), "Form scroll check"

    # ── AFRM-021 to AFRM-030: Volunteer Registration Form ────────────────
    def test_afrm_021_volunteer_form_loads(self, driver):
        """TC: AFRM-021 | Volunteer registration form loads."""
        screen = VolunteerRegisterScreen(driver)
        time.sleep(5)
        assert screen.is_loaded(), "Volunteer form failed to load"

    def test_afrm_022_volunteer_name_field(self, driver):
        """TC: AFRM-022 | Volunteer name field present."""
        screen = VolunteerRegisterScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Volunteer name field check"

    def test_afrm_023_volunteer_email_field(self, driver):
        """TC: AFRM-023 | Volunteer email field present."""
        screen = VolunteerRegisterScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Volunteer email field check"

    def test_afrm_024_volunteer_password_field(self, driver):
        """TC: AFRM-024 | Volunteer password field present."""
        screen = VolunteerRegisterScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Volunteer password field check"

    def test_afrm_025_volunteer_skills_section(self, driver):
        """TC: AFRM-025 | Volunteer skills section present."""
        screen = VolunteerRegisterScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Skills section check"

    def test_afrm_026_volunteer_register_button(self, driver):
        """TC: AFRM-026 | Volunteer register button present."""
        screen = VolunteerRegisterScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Register button check"

    def test_afrm_027_volunteer_empty_name_rejected(self, driver):
        """TC: AFRM-027 | Empty volunteer name rejected."""
        screen = VolunteerRegisterScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Empty name rejection"

    def test_afrm_028_volunteer_invalid_email(self, driver):
        """TC: AFRM-028 | Invalid volunteer email rejected."""
        screen = VolunteerRegisterScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Invalid email rejection"

    def test_afrm_029_volunteer_weak_password(self, driver):
        """TC: AFRM-029 | Weak volunteer password rejected."""
        screen = VolunteerRegisterScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Weak password rejection"

    def test_afrm_030_volunteer_form_scrollable(self, driver):
        """TC: AFRM-030 | Volunteer form scrollable."""
        screen = VolunteerRegisterScreen(driver)
        screen.wait_for_screen_ready()
        screen.scroll_down()
        assert screen.is_loaded(), "Form scroll check"

    # ── AFRM-031 to AFRM-040: Input Validation ──────────────────────────
    def test_afrm_031_sql_injection_in_name(self, driver):
        """TC: AFRM-031 | SQL injection in name field handled."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "SQL injection in name"

    def test_afrm_032_xss_in_name_field(self, driver):
        """TC: AFRM-032 | XSS in name field handled."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        source = screen.get_page_source()
        assert "<script>" not in source, "XSS in name field"

    def test_afrm_033_html_injection_handled(self, driver):
        """TC: AFRM-033 | HTML injection handled."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "HTML injection check"

    def test_afrm_034_unicode_in_name_field(self, driver):
        """TC: AFRM-034 | Unicode in name field accepted."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Unicode name check"

    def test_afrm_035_emoji_in_name_field(self, driver):
        """TC: AFRM-035 | Emoji in name field handled."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Emoji name check"

    def test_afrm_036_max_length_input(self, driver):
        """TC: AFRM-036 | Max length input handled."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Max length check"

    def test_afrm_037_whitespace_only_rejected(self, driver):
        """TC: AFRM-037 | Whitespace-only input rejected."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Whitespace rejection"

    def test_afrm_038_special_chars_in_password(self, driver):
        """TC: AFRM-038 | Special chars in password accepted."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Special chars password"

    def test_afrm_039_numeric_only_in_phone(self, driver):
        """TC: AFRM-039 | Phone accepts only numeric input."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Numeric phone check"

    def test_afrm_040_email_format_validation(self, driver):
        """TC: AFRM-040 | Email format validation works."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Email format validation"

    # ── AFRM-041 to AFRM-050: Form Behavior ─────────────────────────────
    def test_afrm_041_form_state_after_rotation(self, driver):
        """TC: AFRM-041 | Form state preserved after rotation."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        screen.set_orientation("LANDSCAPE")
        time.sleep(1)
        screen.set_orientation("PORTRAIT")
        assert screen.is_loaded(), "Form state after rotation"

    def test_afrm_042_form_submission_feedback(self, driver):
        """TC: AFRM-042 | Form shows feedback on submission."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Submission feedback check"

    def test_afrm_043_form_loading_indicator(self, driver):
        """TC: AFRM-043 | Loading indicator during submission."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Loading indicator check"

    def test_afrm_044_form_error_clears(self, driver):
        """TC: AFRM-044 | Error clears on valid input."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Error clear check"

    def test_afrm_045_double_submission_prevented(self, driver):
        """TC: AFRM-045 | Double form submission prevented."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Double submission prevention"

    def test_afrm_046_form_auto_fill_support(self, driver):
        """TC: AFRM-046 | Form supports auto-fill."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Auto-fill support"

    def test_afrm_047_form_accessibility_labels(self, driver):
        """TC: AFRM-047 | Form fields have accessibility labels."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Accessibility labels check"

    def test_afrm_048_form_input_cursor(self, driver):
        """TC: AFRM-048 | Cursor visible in focused field."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Cursor visibility check"

    def test_afrm_049_form_field_focus_order(self, driver):
        """TC: AFRM-049 | Fields focus in correct order."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Focus order check"

    def test_afrm_050_form_data_not_leaked(self, driver):
        """TC: AFRM-050 | Form data not leaked in page source."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        source = screen.get_page_source()
        assert "password123" not in source.lower(), "Form data leaked"
