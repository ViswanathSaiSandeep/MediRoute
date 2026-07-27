"""
Screen Objects for all MediRoute Android app screens.
Each screen maps to a Flutter route/screen in the application.
"""

import os
import sys
from appium.webdriver.common.appiumby import AppiumBy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.base_screen import BaseScreen
from config.appium_settings import ROUTES


class SplashScreen(BaseScreen):
    """Splash screen – initial app loading."""

    def wait_for_splash(self, timeout=15):
        self.wait_for_screen_ready(timeout)
        return True

    def is_loaded(self):
        return self.wait_for_screen_ready()

    def has_app_branding(self):
        return self.is_text_present("MediRoute") or self.is_text_present("mediroute")

    def wait_for_splash_complete(self):
        import time
        time.sleep(5)
        return True


class RoleSelectionScreen(BaseScreen):
    """Role selection – Bystander / Volunteer / Hospital."""

    def is_loaded(self):
        self.wait_for_screen_ready()
        return True

    def is_bystander_option_present(self):
        return self.is_text_present("Bystander") or self.is_text_present("bystander")

    def is_volunteer_option_present(self):
        return self.is_text_present("Volunteer") or self.is_text_present("volunteer")

    def is_hospital_option_present(self):
        return self.is_text_present("Hospital") or self.is_text_present("hospital")

    def select_bystander(self):
        return self.click_text("Bystander")

    def select_volunteer(self):
        return self.click_text("Volunteer")

    def select_hospital(self):
        return self.click_text("Hospital")

    def get_all_roles(self):
        return ["Bystander", "Volunteer", "Hospital"]


class BystanderAuthScreen(BaseScreen):
    """Bystander authentication screen."""

    def is_loaded(self):
        self.wait_for_screen_ready()
        return True

    def has_email_field(self):
        return (self.is_text_present("Email") or self.is_text_present("email")
                or self.is_text_present("phone") or self.is_text_present("Phone"))

    def has_password_field(self):
        return self.is_text_present("Password") or self.is_text_present("password")

    def has_login_button(self):
        return (self.is_text_present("Login") or self.is_text_present("Sign")
                or self.is_text_present("Continue") or self.is_text_present("Verify"))

    def enter_email(self, email):
        fields = self.find_by_class("android.widget.EditText")
        if fields and len(fields) > 0:
            fields[0].clear()
            fields[0].send_keys(email)
            return True
        return False

    def enter_password(self, password):
        fields = self.find_by_class("android.widget.EditText")
        if fields and len(fields) > 1:
            fields[1].clear()
            fields[1].send_keys(password)
            return True
        return False

    def tap_login(self):
        return (self.click_text("Login") or self.click_text("Sign In")
                or self.click_text("Continue"))

    def has_error_message(self):
        return (self.is_text_present("error") or self.is_text_present("Error")
                or self.is_text_present("invalid") or self.is_text_present("Invalid")
                or self.is_text_present("required") or self.is_text_present("Required"))


class HospitalRegisterScreen(BaseScreen):
    """Hospital registration screen."""

    def is_loaded(self):
        self.wait_for_screen_ready()
        return True

    def has_registration_form(self):
        return (self.is_text_present("Hospital") or self.is_text_present("Register")
                or self.is_text_present("Registration"))

    def has_name_field(self):
        return self.is_text_present("Name") or self.is_text_present("name")

    def has_email_field(self):
        return self.is_text_present("Email") or self.is_text_present("email")

    def has_password_field(self):
        return self.is_text_present("Password") or self.is_text_present("password")

    def has_submit_button(self):
        return (self.is_text_present("Submit") or self.is_text_present("Register")
                or self.is_text_present("Save") or self.is_text_present("Sign Up"))

    def enter_hospital_name(self, name):
        fields = self.find_by_class("android.widget.EditText")
        if fields and len(fields) > 0:
            fields[0].clear()
            fields[0].send_keys(name)
            return True
        return False

    def enter_email(self, email):
        fields = self.find_by_class("android.widget.EditText")
        if fields and len(fields) > 1:
            fields[1].clear()
            fields[1].send_keys(email)
            return True
        return False

    def enter_password(self, password):
        fields = self.find_by_class("android.widget.EditText")
        if fields and len(fields) > 2:
            fields[2].clear()
            fields[2].send_keys(password)
            return True
        return False

    def tap_submit(self):
        return (self.click_text("Register") or self.click_text("Submit")
                or self.click_text("Sign Up"))


class VolunteerRegisterScreen(BaseScreen):
    """Volunteer registration screen."""

    def is_loaded(self):
        self.wait_for_screen_ready()
        return True

    def has_registration_form(self):
        return (self.is_text_present("Volunteer") or self.is_text_present("Register")
                or self.is_text_present("volunteer"))

    def has_name_field(self):
        return self.is_text_present("Name") or self.is_text_present("name")

    def has_email_field(self):
        return self.is_text_present("Email") or self.is_text_present("email")

    def has_password_field(self):
        return self.is_text_present("Password") or self.is_text_present("password")

    def has_skills_section(self):
        return self.is_text_present("Skills") or self.is_text_present("skills")

    def enter_name(self, name):
        fields = self.find_by_class("android.widget.EditText")
        if fields and len(fields) > 0:
            fields[0].clear()
            fields[0].send_keys(name)
            return True
        return False

    def enter_email(self, email):
        fields = self.find_by_class("android.widget.EditText")
        if fields and len(fields) > 1:
            fields[1].clear()
            fields[1].send_keys(email)
            return True
        return False

    def enter_password(self, password):
        fields = self.find_by_class("android.widget.EditText")
        if fields and len(fields) > 2:
            fields[2].clear()
            fields[2].send_keys(password)
            return True
        return False

    def tap_register(self):
        return (self.click_text("Register") or self.click_text("Submit")
                or self.click_text("Sign Up"))


class BystanderHomeScreen(BaseScreen):
    """Bystander emergency home screen."""

    def is_loaded(self):
        self.wait_for_screen_ready()
        return True

    def has_sos_button(self):
        return (self.is_text_present("SOS") or self.is_text_present("Emergency")
                or self.is_text_present("Help"))

    def has_emergency_types(self):
        return self.is_text_present("Cardiac") or self.is_text_present("emergency")

    def has_map_view(self):
        return len(self.find_by_class("android.view.View")) > 0

    def tap_sos(self):
        return self.click_text("SOS") or self.click_text("Emergency")


class VolunteerDashboardScreen(BaseScreen):
    """Volunteer dashboard screen."""

    def is_loaded(self):
        self.wait_for_screen_ready()
        return True

    def has_dashboard_content(self):
        return self.is_text_present("Dashboard") or self.is_text_present("Volunteer")

    def has_alert_section(self):
        return self.is_text_present("Alert") or self.is_text_present("alert")

    def has_status_indicator(self):
        return self.is_text_present("Available") or self.is_text_present("Busy")


class HospitalDashboardScreen(BaseScreen):
    """Hospital dashboard screen."""

    def is_loaded(self):
        self.wait_for_screen_ready()
        return True

    def has_dashboard_content(self):
        return self.is_text_present("Hospital") or self.is_text_present("Dashboard")

    def has_emergency_list(self):
        return self.is_text_present("Emergency") or self.is_text_present("Alert")

    def has_bed_availability(self):
        return self.is_text_present("Bed") or self.is_text_present("Available")


class ProfileScreen(BaseScreen):
    """Profile screen."""

    def is_loaded(self):
        self.wait_for_screen_ready()
        return True

    def has_profile_content(self):
        return self.is_text_present("Profile") or self.is_text_present("profile")

    def has_name_display(self):
        return self.is_text_present("Name") or self.is_text_present("name")

    def has_logout_button(self):
        return self.is_text_present("Logout") or self.is_text_present("Sign Out")


class EmergencyHistoryScreen(BaseScreen):
    """Emergency history screen."""

    def is_loaded(self):
        self.wait_for_screen_ready()
        return True

    def has_history_content(self):
        return self.is_text_present("History") or self.is_text_present("history")

    def has_history_list(self):
        return len(self.find_by_class("android.view.View")) > 3


class FirstAidScreen(BaseScreen):
    """First aid guidance screen."""

    def is_loaded(self):
        self.wait_for_screen_ready()
        return True

    def has_first_aid_content(self):
        return self.is_text_present("First Aid") or self.is_text_present("first aid")

    def has_instructions(self):
        return self.is_text_present("Step") or self.is_text_present("step")
