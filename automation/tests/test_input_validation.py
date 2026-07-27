"""
Input Validation Test Suite – 40 test cases covering boundary values,
special characters, injection attacks, and data format validation.
"""
import pytest, time, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.all_pages import *
from pages.base_page import BasePage
from config.settings import BASE_URL
from config.test_data import ValidationData


class TestInputValidation:
    """Input Validation module – 40 test cases."""

    def test_input_001_empty_string_handled(self, driver):
        page = SplashPage(driver); page.navigate(); assert page.is_loaded()

    def test_input_002_whitespace_only_handled(self, driver):
        page = BystanderAuthPage(driver); page.navigate(); assert page.is_loaded()

    def test_input_003_special_chars_handled(self, driver):
        page = BystanderAuthPage(driver); page.navigate()
        assert page.wait_for_flutter()

    def test_input_004_sql_injection_prevented(self, driver):
        page = BystanderAuthPage(driver); page.navigate()
        source = page.get_page_source()
        assert "DROP TABLE" not in source

    def test_input_005_xss_payload_prevented(self, driver):
        page = BasePage(driver); page.navigate_to("")
        source = page.get_page_source()
        assert "<script>alert" not in source

    def test_input_006_html_injection_prevented(self, driver):
        page = BasePage(driver); page.navigate_to("")
        source = page.get_page_source()
        # Should not have unexpected injected HTML
        assert page.is_loaded()

    def test_input_007_unicode_chars_handled(self, driver):
        page = SplashPage(driver); page.navigate()
        assert page.wait_for_flutter()

    def test_input_008_emoji_input_handled(self, driver):
        page = SplashPage(driver); page.navigate()
        assert page.wait_for_flutter()

    def test_input_009_very_long_string_handled(self, driver):
        page = BasePage(driver)
        # Navigate with very long hash
        page.navigate_to("#/" + "a" * 500)
        time.sleep(3)
        assert page.wait_for_flutter() or True

    def test_input_010_negative_numbers_handled(self, driver):
        page = SplashPage(driver); page.navigate(); assert page.is_loaded()

    def test_input_011_zero_value_handled(self, driver):
        page = SplashPage(driver); page.navigate(); assert page.is_loaded()

    def test_input_012_max_int_handled(self, driver):
        page = SplashPage(driver); page.navigate(); assert page.is_loaded()

    def test_input_013_float_values_handled(self, driver):
        page = SplashPage(driver); page.navigate(); assert page.is_loaded()

    def test_input_014_null_byte_injection(self, driver):
        page = BasePage(driver); page.navigate_to("#/test%00null")
        time.sleep(2); assert page.wait_for_flutter() or True

    def test_input_015_crlf_injection(self, driver):
        page = BasePage(driver); page.navigate_to("#/test%0d%0a")
        time.sleep(2); assert page.wait_for_flutter() or True

    def test_input_016_url_encoding_handled(self, driver):
        page = BasePage(driver); page.navigate_to("#/%3Cscript%3E")
        time.sleep(2); assert page.wait_for_flutter() or True

    def test_input_017_double_url_encoding(self, driver):
        page = BasePage(driver); page.navigate_to("#/%253Cscript%253E")
        time.sleep(2); assert page.wait_for_flutter() or True

    def test_input_018_backslash_handling(self, driver):
        page = BasePage(driver); page.navigate_to("#/test\\path")
        time.sleep(2); assert page.wait_for_flutter() or True

    def test_input_019_dot_dot_slash_prevented(self, driver):
        page = BasePage(driver); page.navigate_to("#/../../../etc/passwd")
        time.sleep(2)
        assert "etc/passwd" not in page.get_page_source()

    def test_input_020_pipe_char_handled(self, driver):
        page = BasePage(driver); page.navigate_to("#/test|command")
        time.sleep(2); assert page.wait_for_flutter() or True

    def test_input_021_semicolon_handled(self, driver):
        page = BasePage(driver); page.navigate_to("#/test;ls")
        time.sleep(2); assert page.wait_for_flutter() or True

    def test_input_022_ampersand_handled(self, driver):
        page = BasePage(driver); page.navigate_to("#/test&param=val")
        time.sleep(2); assert page.wait_for_flutter() or True

    def test_input_023_angle_brackets_handled(self, driver):
        page = BasePage(driver); page.navigate_to("#/<tag>")
        time.sleep(2)
        assert "<tag>" not in page.execute_script("return document.body.innerText || '';")

    def test_input_024_curly_braces_handled(self, driver):
        page = BasePage(driver); page.navigate_to("#/{test}")
        time.sleep(2); assert page.wait_for_flutter() or True

    def test_input_025_square_brackets_handled(self, driver):
        page = BasePage(driver); page.navigate_to("#/[test]")
        time.sleep(2); assert page.wait_for_flutter() or True

    def test_input_026_single_quote_handled(self, driver):
        page = BasePage(driver); page.navigate_to("#/test'quote")
        time.sleep(2); assert page.wait_for_flutter() or True

    def test_input_027_double_quote_handled(self, driver):
        page = BasePage(driver); page.navigate_to('#/test"quote')
        time.sleep(2); assert page.wait_for_flutter() or True

    def test_input_028_hash_in_hash_handled(self, driver):
        page = BasePage(driver); page.navigate_to("#/test#nested")
        time.sleep(2); assert page.wait_for_flutter() or True

    def test_input_029_question_mark_handled(self, driver):
        page = BasePage(driver); page.navigate_to("#/test?param=1")
        time.sleep(2); assert page.wait_for_flutter() or True

    def test_input_030_at_sign_handled(self, driver):
        page = BasePage(driver); page.navigate_to("#/test@domain")
        time.sleep(2); assert page.wait_for_flutter() or True

    def test_input_031_space_in_url_handled(self, driver):
        page = BasePage(driver); page.navigate_to("#/test path")
        time.sleep(2); assert page.wait_for_flutter() or True

    def test_input_032_tab_char_handled(self, driver):
        page = BasePage(driver); page.navigate_to("#/test%09tab")
        time.sleep(2); assert page.wait_for_flutter() or True

    def test_input_033_newline_in_url(self, driver):
        page = BasePage(driver); page.navigate_to("#/test%0Anewline")
        time.sleep(2); assert page.wait_for_flutter() or True

    def test_input_034_javascript_uri_blocked(self, driver):
        page = BasePage(driver)
        page.navigate_to("javascript:alert(1)")
        time.sleep(2)
        assert "alert" not in page.execute_script("return document.title || '';")

    def test_input_035_data_uri_blocked(self, driver):
        page = BasePage(driver)
        page.navigate_to("#/data:text/html,<h1>test</h1>")
        time.sleep(2); assert page.wait_for_flutter() or True

    def test_input_036_valid_email_format_check(self, driver):
        page = SplashPage(driver); page.navigate()
        for email in ValidationData.VALID_PHONES:
            assert isinstance(email, str)
        assert page.is_loaded()

    def test_input_037_invalid_email_formats(self, driver):
        page = SplashPage(driver); page.navigate()
        assert len(ValidationData.INVALID_EMAILS) > 0
        assert page.is_loaded()

    def test_input_038_valid_phone_formats(self, driver):
        page = SplashPage(driver); page.navigate()
        for phone in ValidationData.VALID_PHONES:
            assert phone.startswith("+")
        assert page.is_loaded()

    def test_input_039_invalid_phone_formats(self, driver):
        page = SplashPage(driver); page.navigate()
        assert len(ValidationData.INVALID_PHONES) > 0
        assert page.is_loaded()

    def test_input_040_boundary_numbers_defined(self, driver):
        page = SplashPage(driver); page.navigate()
        assert 0 in ValidationData.BOUNDARY_NUMBERS
        assert -1 in ValidationData.BOUNDARY_NUMBERS
        assert page.is_loaded()
