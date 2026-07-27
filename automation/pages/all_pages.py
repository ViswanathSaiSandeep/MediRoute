"""Page Objects for all MediRoute screens."""

from selenium.webdriver.common.by import By
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.base_page import BasePage
from config.settings import ROUTES


class SplashPage(BasePage):
    """Splash screen page object."""
    ROUTE = ROUTES["splash"]

    def navigate(self):
        self.navigate_to("")

    def is_loaded(self):
        self.wait_for_page_ready()
        return self.wait_for_flutter()

    def get_title_text(self):
        return self.get_page_title()

    def is_app_logo_present(self):
        return self.is_text_present("MediRoute") or self.is_element_visible(By.TAG_NAME, "canvas")

    def wait_for_splash_complete(self):
        import time
        time.sleep(5)
        return True


class RoleSelectionPage(BasePage):
    """Role selection screen page object."""
    ROUTE = ROUTES["role_selection"]

    def navigate(self):
        self.navigate_to(f"#{self.ROUTE}")

    def is_loaded(self):
        self.wait_for_page_ready()
        return self.wait_for_flutter()

    def is_bystander_role_present(self):
        return self.is_text_present("Bystander") or self.is_text_present("bystander")

    def is_volunteer_role_present(self):
        return self.is_text_present("Volunteer") or self.is_text_present("volunteer")

    def is_hospital_role_present(self):
        return self.is_text_present("Hospital") or self.is_text_present("hospital")

    def select_bystander(self):
        return self.click_text("Bystander")

    def select_volunteer(self):
        return self.click_text("Volunteer")

    def select_hospital(self):
        return self.click_text("Hospital")

    def get_all_roles(self):
        return ["Bystander", "Volunteer", "Hospital"]


class BystanderAuthPage(BasePage):
    """Bystander authentication screen page object."""
    ROUTE = ROUTES["bystander_auth"]

    def navigate(self):
        self.navigate_to(f"#{self.ROUTE}")

    def is_loaded(self):
        self.wait_for_page_ready()
        return self.wait_for_flutter()

    def is_phone_field_present(self):
        return (self.is_text_present("phone") or self.is_text_present("Phone")
                or self.is_text_present("mobile") or self.is_text_present("Mobile"))

    def is_login_button_present(self):
        return (self.is_text_present("Login") or self.is_text_present("Sign")
                or self.is_text_present("Continue") or self.is_text_present("Verify"))

    def has_auth_form(self):
        return self.is_phone_field_present() or self.is_login_button_present()


class HospitalRegisterPage(BasePage):
    """Hospital registration screen page object."""
    ROUTE = ROUTES["hospital_register"]

    def navigate(self):
        self.navigate_to(f"#{self.ROUTE}")

    def is_loaded(self):
        self.wait_for_page_ready()
        return self.wait_for_flutter()

    def has_registration_form(self):
        return (self.is_text_present("Hospital") or self.is_text_present("Register")
                or self.is_text_present("Registration"))

    def is_name_field_present(self):
        return self.is_text_present("Name") or self.is_text_present("name")

    def is_submit_button_present(self):
        return (self.is_text_present("Submit") or self.is_text_present("Register")
                or self.is_text_present("Save"))


class BystanderHomePage(BasePage):
    """Bystander emergency home screen page object."""
    ROUTE = ROUTES["bystander_home"]

    def navigate(self):
        self.navigate_to(f"#{self.ROUTE}")

    def is_loaded(self):
        self.wait_for_page_ready()
        return self.wait_for_flutter()

    def is_sos_button_present(self):
        return (self.is_text_present("SOS") or self.is_text_present("Emergency")
                or self.is_text_present("Help"))

    def has_emergency_types(self):
        return self.is_text_present("Cardiac") or self.is_text_present("emergency")

    def is_map_present(self):
        return self.is_element_visible(By.TAG_NAME, "canvas", timeout=3)


class VolunteerRegisterPage(BasePage):
    """Volunteer registration screen page object."""
    ROUTE = ROUTES["volunteer_register"]

    def navigate(self):
        self.navigate_to(f"#{self.ROUTE}")

    def is_loaded(self):
        self.wait_for_page_ready()
        return self.wait_for_flutter()

    def has_registration_form(self):
        return (self.is_text_present("Volunteer") or self.is_text_present("Register")
                or self.is_text_present("volunteer"))


class VolunteerDashboardPage(BasePage):
    """Volunteer dashboard screen page object."""
    ROUTE = ROUTES["volunteer_dashboard"]

    def navigate(self):
        self.navigate_to(f"#{self.ROUTE}")

    def is_loaded(self):
        self.wait_for_page_ready()
        return self.wait_for_flutter()

    def has_dashboard_content(self):
        return self.is_text_present("Dashboard") or self.is_text_present("Volunteer")


class HospitalDashboardPage(BasePage):
    """Hospital dashboard screen page object."""
    ROUTE = ROUTES["hospital_dashboard"]

    def navigate(self):
        self.navigate_to(f"#{self.ROUTE}")

    def is_loaded(self):
        self.wait_for_page_ready()
        return self.wait_for_flutter()

    def has_dashboard_content(self):
        return self.is_text_present("Hospital") or self.is_text_present("Dashboard")


class EmergencyHistoryPage(BasePage):
    """Emergency history screen page object."""
    ROUTE = ROUTES["history"]

    def navigate(self):
        self.navigate_to(f"#{self.ROUTE}")

    def is_loaded(self):
        self.wait_for_page_ready()
        return self.wait_for_flutter()

    def has_history_content(self):
        return self.is_text_present("History") or self.is_text_present("history")


class ProfilePage(BasePage):
    """Profile screen page object."""
    ROUTE = ROUTES["profile"]

    def navigate(self):
        self.navigate_to(f"#{self.ROUTE}")

    def is_loaded(self):
        self.wait_for_page_ready()
        return self.wait_for_flutter()

    def has_profile_content(self):
        return self.is_text_present("Profile") or self.is_text_present("profile")


class CommonElements(BasePage):
    """Shared UI elements across pages."""

    def has_app_bar(self):
        return self.is_text_present("MediRoute") or self.is_element_visible(By.TAG_NAME, "header", timeout=3)

    def has_navigation(self):
        return self.is_element_visible(By.CSS_SELECTOR, "[role='navigation']", timeout=3)

    def get_all_links(self):
        return self.find_elements(By.TAG_NAME, "a")

    def get_all_buttons(self):
        return self.find_elements(By.CSS_SELECTOR, "[role='button'], button")

    def get_all_images(self):
        return self.find_elements(By.TAG_NAME, "img")

    def has_footer(self):
        return self.is_element_visible(By.TAG_NAME, "footer", timeout=3)
