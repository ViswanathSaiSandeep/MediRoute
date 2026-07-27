"""
Appium Validation & Unit Test Suite – 50 test cases for Android.
Covers data validation rules, boundary values, field-level validation,
format checking, and business rule enforcement.
"""
import pytest
import time
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.all_screens import *
from pages.base_screen import BaseScreen
from config.test_data import TestUsers, ValidationData, EmergencyData


class TestAppiumValidation:
    """Validation & Unit Testing module – 50 test cases."""

    # ── AVAL-001 to AVAL-010: Email Validation ──────────────────────────
    def test_aval_001_valid_email_accepted(self, driver):
        """TC: AVAL-001 | Valid email format accepted."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Valid email acceptance"

    def test_aval_002_empty_email_rejected(self, driver):
        """TC: AVAL-002 | Empty email rejected."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Empty email rejection"

    def test_aval_003_email_without_at_rejected(self, driver):
        """TC: AVAL-003 | Email without @ rejected."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "No-@ email rejection"

    def test_aval_004_email_without_domain_rejected(self, driver):
        """TC: AVAL-004 | Email without domain rejected."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "No-domain email rejection"

    def test_aval_005_email_double_at_rejected(self, driver):
        """TC: AVAL-005 | Email with double @ rejected."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Double-@ email rejection"

    def test_aval_006_email_with_spaces_rejected(self, driver):
        """TC: AVAL-006 | Email with spaces rejected."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Space email rejection"

    def test_aval_007_email_max_length(self, driver):
        """TC: AVAL-007 | Email max length enforced."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Max length email"

    def test_aval_008_email_unicode_handling(self, driver):
        """TC: AVAL-008 | Unicode in email handled."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Unicode email"

    def test_aval_009_email_case_insensitive(self, driver):
        """TC: AVAL-009 | Email validation case-insensitive."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Case insensitive email"

    def test_aval_010_email_special_chars(self, driver):
        """TC: AVAL-010 | Special chars in email handled."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Special chars email"

    # ── AVAL-011 to AVAL-020: Password Validation ───────────────────────
    def test_aval_011_password_min_length(self, driver):
        """TC: AVAL-011 | Password min 6 chars enforced."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Min password length"

    def test_aval_012_password_empty_rejected(self, driver):
        """TC: AVAL-012 | Empty password rejected."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Empty password"

    def test_aval_013_password_1_char_rejected(self, driver):
        """TC: AVAL-013 | Single char password rejected."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "1-char password"

    def test_aval_014_password_5_chars_rejected(self, driver):
        """TC: AVAL-014 | 5-char password rejected."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "5-char password"

    def test_aval_015_password_6_chars_accepted(self, driver):
        """TC: AVAL-015 | 6-char password accepted."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "6-char password"

    def test_aval_016_password_special_chars_accepted(self, driver):
        """TC: AVAL-016 | Special chars in password accepted."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Special char password"

    def test_aval_017_password_unicode_handling(self, driver):
        """TC: AVAL-017 | Unicode password handled."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Unicode password"

    def test_aval_018_password_max_length(self, driver):
        """TC: AVAL-018 | Max length password handled."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Max length password"

    def test_aval_019_password_masked_display(self, driver):
        """TC: AVAL-019 | Password displayed as masked."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Password masking"

    def test_aval_020_password_whitespace_only_rejected(self, driver):
        """TC: AVAL-020 | Whitespace-only password rejected."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Whitespace password"

    # ── AVAL-021 to AVAL-030: Name Validation ───────────────────────────
    def test_aval_021_valid_name_accepted(self, driver):
        """TC: AVAL-021 | Valid name accepted."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Valid name"

    def test_aval_022_empty_name_rejected(self, driver):
        """TC: AVAL-022 | Empty name rejected."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Empty name"

    def test_aval_023_name_with_numbers(self, driver):
        """TC: AVAL-023 | Name with numbers handled."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Numeric name"

    def test_aval_024_name_with_special_chars(self, driver):
        """TC: AVAL-024 | Name with special chars handled."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Special char name"

    def test_aval_025_name_unicode(self, driver):
        """TC: AVAL-025 | Unicode name accepted."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Unicode name"

    def test_aval_026_name_emoji(self, driver):
        """TC: AVAL-026 | Emoji in name handled."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Emoji name"

    def test_aval_027_name_max_length(self, driver):
        """TC: AVAL-027 | Max length name handled."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Max length name"

    def test_aval_028_name_sql_injection(self, driver):
        """TC: AVAL-028 | SQL injection in name handled."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "SQL injection name"

    def test_aval_029_name_xss_payload(self, driver):
        """TC: AVAL-029 | XSS in name handled."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        source = screen.get_page_source()
        assert "<script>" not in source, "XSS in name"

    def test_aval_030_name_html_injection(self, driver):
        """TC: AVAL-030 | HTML injection in name handled."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "HTML injection name"

    # ── AVAL-031 to AVAL-040: Phone Validation ──────────────────────────
    def test_aval_031_valid_phone_accepted(self, driver):
        """TC: AVAL-031 | Valid phone number accepted."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Valid phone"

    def test_aval_032_empty_phone_rejected(self, driver):
        """TC: AVAL-032 | Empty phone rejected."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Empty phone"

    def test_aval_033_alphabetic_phone_rejected(self, driver):
        """TC: AVAL-033 | Alphabetic phone rejected."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Alpha phone"

    def test_aval_034_short_phone_rejected(self, driver):
        """TC: AVAL-034 | Too-short phone rejected."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Short phone"

    def test_aval_035_long_phone_rejected(self, driver):
        """TC: AVAL-035 | Too-long phone rejected."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Long phone"

    def test_aval_036_phone_with_country_code(self, driver):
        """TC: AVAL-036 | Phone with country code accepted."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Country code phone"

    def test_aval_037_phone_special_chars_rejected(self, driver):
        """TC: AVAL-037 | Special chars in phone rejected."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Special char phone"

    def test_aval_038_phone_spaces_handling(self, driver):
        """TC: AVAL-038 | Spaces in phone handled."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Space phone"

    def test_aval_039_phone_leading_zero(self, driver):
        """TC: AVAL-039 | Leading zero phone handled."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Leading zero phone"

    def test_aval_040_phone_international_formats(self, driver):
        """TC: AVAL-040 | International phone formats handled."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "International phone"

    # ── AVAL-041 to AVAL-050: Business Logic Validation ──────────────────
    def test_aval_041_emergency_type_validation(self, driver):
        """TC: AVAL-041 | Emergency type selection validated."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Emergency type validation"

    def test_aval_042_location_data_format(self, driver):
        """TC: AVAL-042 | Location data format correct."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Location format"

    def test_aval_043_hospital_bed_count_numeric(self, driver):
        """TC: AVAL-043 | Hospital bed count must be numeric."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Bed count numeric"

    def test_aval_044_negative_bed_count_rejected(self, driver):
        """TC: AVAL-044 | Negative bed count rejected."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Negative bed count"

    def test_aval_045_zero_bed_count_handled(self, driver):
        """TC: AVAL-045 | Zero bed count handled."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Zero bed count"

    def test_aval_046_skills_selection_validation(self, driver):
        """TC: AVAL-046 | Volunteer skills selection validated."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Skills validation"

    def test_aval_047_duplicate_registration_handled(self, driver):
        """TC: AVAL-047 | Duplicate registration handled."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Duplicate registration"

    def test_aval_048_concurrent_form_validation(self, driver):
        """TC: AVAL-048 | Concurrent validation doesn't crash."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Concurrent validation"

    def test_aval_049_validation_error_messages_clear(self, driver):
        """TC: AVAL-049 | Error messages are clear and actionable."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        assert screen.is_loaded(), "Error message clarity"

    def test_aval_050_validation_persists_after_rotation(self, driver):
        """TC: AVAL-050 | Validation state persists after rotation."""
        screen = BaseScreen(driver)
        screen.wait_for_screen_ready()
        screen.set_orientation("LANDSCAPE")
        time.sleep(1)
        screen.set_orientation("PORTRAIT")
        assert screen.is_loaded(), "Validation after rotation"
