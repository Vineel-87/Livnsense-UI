import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Dashboard Workflow")  # Feature: Dashboard Workflow
class TestDashboardWorkflow:

    @pytest.fixture(scope="class")
    def driver(self):
        driver = webdriver.Chrome()
        driver.maximize_window()
        yield driver
        driver.quit()

    @allure.story("Successful Login")  # Scenario: Successful Login
    def test_login(self, driver):
        with allure.step("Navigate to login page"):
            driver.get("https://alv-vicas.livnsense.com/#/auth/login")
            allure.attach(driver.get_screenshot_as_png(),
                          name="login-page",
                          attachment_type=allure.attachment_type.PNG)

        with allure.step("Enter credentials"):
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Username']"))
            )
            driver.find_element(By.XPATH, "//input[@placeholder='Username']").send_keys("madan")
            driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("Madan@123")
            allure.attach(driver.get_screenshot_as_png(),
                          name="credentials-entered",
                          attachment_type=allure.attachment_type.PNG)

        with allure.step("Submit login"):
            driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]").click()

        with allure.step("Verify successful login"):
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//img[@alt='Autoliv']"))
            )
            allure.attach(driver.get_screenshot_as_png(),
                          name="dashboard-loaded",
                          attachment_type=allure.attachment_type.PNG)

    @allure.story("Project Selection")  # Scenario: Project Selection
    def test_project_selection(self, driver):
        with allure.step("Locate project dropdown"):
            dropdown = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "select.dropdown"))
            )
            allure.attach(driver.get_screenshot_as_png(),
                          name="project-dropdown",
                          attachment_type=allure.attachment_type.PNG)

        with allure.step("Verify default project is AIB"):
            select = Select(dropdown)
            assert select.first_selected_option.text == "AIB", \
                f"Expected default project AIB but got {select.first_selected_option.text}"

        with allure.step("Select AIX project"):
            select.select_by_visible_text("AIX")
            allure.attach(driver.get_screenshot_as_png(),
                          name="aix-selected",
                          attachment_type=allure.attachment_type.PNG)

        with allure.step("Verify AIX is selected"):
            selected_option = Select(driver.find_element(By.CSS_SELECTOR, "select.dropdown")).first_selected_option
            assert selected_option.text == "AIX", \
                f"Expected AIX but got {selected_option.text}"

    @allure.story("Verify Available Projects")  # Scenario: Verify Available Projects
    def test_available_projects(self, driver):
        with allure.step("Check all project options"):
            select = Select(WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "select.dropdown"))
            ))
            options = [option.text for option in select.options]
            expected_options = ["AIB", "AIX", "INBD", "TCB"]  # Update this based on real dropdown

            allure.attach("\n".join(options),
                          name="available-projects",
                          attachment_type=allure.attachment_type.TEXT)

            assert set(options) == set(expected_options), \
                f"Project options mismatch. Expected {expected_options} but got {options}"

    @allure.story("Verify PPE Incidents Section")  # Scenario: Verify PPE Incidents Section
    def test_ppe_incidents_section(self, driver):
        with allure.step("Navigate to Gate Incidents section"):
            gate_incidents = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Gate Incidents')]"))
            )
            gate_incidents.click()
            allure.attach(driver.get_screenshot_as_png(),
                          name="gate-incidents-expanded",
                          attachment_type=allure.attachment_type.PNG)

        with allure.step("Click on PPE Incidents sub-menu"):
            ppe_incidents = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'PPE Incidents')]"))
            )
            ppe_incidents.click()
            allure.attach(driver.get_screenshot_as_png(),
                          name="ppe-incidents-selected",
                          attachment_type=allure.attachment_type.PNG)

        with allure.step("Verify 'No Incident' message is displayed"):
            no_incident_msg = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'No Incident')]"))
            )
            assert no_incident_msg.is_displayed(), "No Incident message is not displayed"
            assert "No Incident" in no_incident_msg.text, "Expected 'No Incident' text not found"

            allure.attach(driver.get_screenshot_as_png(),
                          name="no-incident-message",
                          attachment_type=allure.attachment_type.PNG)

    @allure.story("Verify Manage Section")  # Scenario: Verify PPE Incidents Section
    def test_manage_incidents_section(self, driver):
        with allure.step("Navigate to Manage section"):
            gate_incidents = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Manage')]"))
            )
            gate_incidents.click()
            allure.attach(driver.get_screenshot_as_png(),
                          name="gate-incidents-expanded",
                          attachment_type=allure.attachment_type.PNG)

        with allure.step("Click on Manage sub-menu"):
            ppe_incidents = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Manage Users')]"))
            )
            ppe_incidents.click()
            allure.attach(driver.get_screenshot_as_png(),
                          name="ppe-incidents-selected",
                          attachment_type=allure.attachment_type.PNG)

        with allure.step("Click on Second Manage sub-menu"):
            ppe_incidents = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Manage Warehouse')]"))
            )
            ppe_incidents.click()
            allure.attach(driver.get_screenshot_as_png(),
                          name="ppe-incidents-selected",
                          attachment_type=allure.attachment_type.PNG)

    @allure.story("Verify Overall Analytics Section")  # Scenario: Verify PPE Incidents Section
    def test_overall_incidents_section(self, driver):
        with allure.step("Navigate to Overall Analytics section"):
            gate_incidents = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Overall Analytics')]"))
            )
            gate_incidents.click()
            allure.attach(driver.get_screenshot_as_png(),
                          name="gate-incidents-expanded",
                          attachment_type=allure.attachment_type.PNG)

        with allure.step("Click on Overall Analytics sub-menu"):
            ppe_incidents = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Gate Analytics')]"))
            )
            ppe_incidents.click()
            allure.attach(driver.get_screenshot_as_png(),
                          name="ppe-incidents-selected",
                          attachment_type=allure.attachment_type.PNG)


