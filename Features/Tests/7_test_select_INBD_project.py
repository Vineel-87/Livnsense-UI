import pytest
import allure
import time
import csv
import os
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

@allure.feature("Dashboard Workflow")  # Feature: Dashboard Workflow
class TestDashboardWorkflow:

    @pytest.fixture(scope="class")
    def driver(self):
        options = Options()
        # Add all your clean options here exactly as in your first script
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--no-default-browser-check")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--incognito")

        driver = webdriver.Chrome(options=options)
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

        with allure.step("Select INBD project"):
            select.select_by_visible_text("INBD")
            allure.attach(driver.get_screenshot_as_png(),
                          name="inbd-selected",
                          attachment_type=allure.attachment_type.PNG)

        with allure.step("Verify INBD is selected"):
            selected_option = Select(driver.find_element(By.CSS_SELECTOR, "select.dropdown")).first_selected_option
            assert selected_option.text == "INBD", \
                f"Expected INBD but got {selected_option.text}"

    @allure.story("Verify Available Projects")  # Scenario: Verify Available Projects
    def test_available_projects(self, driver):
        with allure.step("Check all project options"):
            select = Select(WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "select.dropdown"))
            ))
            options = [option.text for option in select.options]
            expected_options = ["AIB", "AIX", "AKR", "INBD", "TCB"]  # Update this based on real dropdown

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

    @allure.story("Verify Configuration Section")  # Scenario: Verify PPE Incidents Section
    def test_security_incidents_section(self, driver):
        with allure.step("Navigate to Configuration section"):
            config_incidents = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Configuration')]"))
            )
            config_incidents.click()
            allure.attach(driver.get_screenshot_as_png(),
                          name="Config-incidents-expanded",
                          attachment_type=allure.attachment_type.PNG)

        with allure.step("Click on Configuration sub-menu"):
            permission_incidents = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Manage Permission')]"))
            )
            permission_incidents.click()
            allure.attach(driver.get_screenshot_as_png(),
                          name="permission-incidents-selected",
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

    @allure.story("Verify and Test All Time Period Buttons")
    def test_all_time_period_buttons(self, driver):
        def reopen_calendar():
            try:
                calendar_trigger = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.form-control[style*='pointer']"))
                )
                calendar_trigger.click()
                WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.datepicker-pop-card"))
                )
                return True
            except Exception as e:
                print(f"Failed to reopen calendar: {str(e)}")
                return False

        with allure.step("Open calendar popup initially"):
            try:
                calendar_trigger = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.form-control[style*='pointer']"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", calendar_trigger)
                time.sleep(1)
                calendar_trigger.click()

                popup = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.datepicker-pop-card"))
                )
                assert popup.is_displayed()
                allure.attach(driver.get_screenshot_as_png(),
                              name="calendar_opened",
                              attachment_type=allure.attachment_type.PNG)

            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(),
                              name="calendar_open_failed",
                              attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Failed to open calendar popup initially: {str(e)}")

        with allure.step("Test Today button functionality"):
            try:
                today_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Today')]"))
                )
                today_btn.click()

                WebDriverWait(driver, 5).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.datepicker-pop-card"))
                )
                print("Today button worked successfully")

            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(),
                              name="today_button_failed",
                              attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Today button test failed: {str(e)}")

        with allure.step("Test Week button functionality"):
            if not reopen_calendar():
                pytest.fail("Could not reopen calendar for Week button test")

            try:
                week_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Week')]"))
                )
                driver.execute_script("arguments[0].style.border='2px solid red';", week_btn)
                time.sleep(0.5)

                week_btn.click()

                WebDriverWait(driver, 5).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.datepicker-pop-card"))
                )

                date_display = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.form-control"))
                ).text
                assert " - " in date_display, f"Expected week range but got: {date_display}"
                print(f"Week button worked successfully. Selected range: {date_display}")

            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(),
                              name="week_button_failed",
                              attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Week button test failed: {str(e)}")

        with allure.step("Test Month button functionality"):
            if not reopen_calendar():
                pytest.fail("Could not reopen calendar for Month button test")

            try:
                month_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Month')]"))
                )
                # Highlight button for visibility
                driver.execute_script("arguments[0].style.border='2px solid blue';", month_btn)
                time.sleep(0.5)

                month_btn.click()

                WebDriverWait(driver, 5).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.datepicker-pop-card"))
                )

                date_display = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.form-control"))
                ).text
                # Accept either "Month Year" or "01-Month-YYYY - 30-Month-YYYY" format
                assert (len(date_display.split()) == 2 or " - " in date_display), \
                    f"Unexpected month format: {date_display}"
                print(f"Month button worked successfully. Selected: {date_display}")

            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(),
                              name="month_button_failed",
                              attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Month button test failed: {str(e)}")
    
    @allure.story("Apply Date & Time Ranges from CSV")
    def test_date_and_time_ranges_from_csv(self, driver):
        with open('test_date_range.csv', 'r') as file:
            reader = csv.DictReader(file)
            for idx, row in enumerate(reader, start=1):
                date_range = row['date_range'].strip()
                start_time = row['start_time'].strip()
                end_time = row['end_time'].strip()

                with allure.step(f"[{idx}] Open calendar"):
                    calendar = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[@class='calendar-container ng-star-inserted']"))
                    )
                    calendar.click()
                    time.sleep(1)

                with allure.step(f"[{idx}] Clear existing date range"):
                    date_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "input[bsdaterangepicker][placeholder='Select Date Range']"))
                    )
                    driver.execute_script("arguments[0].value = '';", date_input)
                    driver.execute_script("arguments[0].dispatchEvent(new Event('input'))", date_input)
                    time.sleep(1)

                with allure.step(f"[{idx}] Set new date range: {date_range}"):
                    date_input.send_keys(date_range)
                    time.sleep(1)

                with allure.step(f"[{idx}] Set start time: {start_time}"):
                    start_time_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@type='time' and @placeholder='Start Time']"))
                    )
                    start_time_input.clear()
                    start_time_input.send_keys(start_time)
                    time.sleep(1)

                with allure.step(f"[{idx}] Set end time: {end_time}"):
                    end_time_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@type='time' and @placeholder='End Time']"))
                    )
                    end_time_input.clear()
                    end_time_input.send_keys(end_time)
                    time.sleep(1)

                allure.attach(driver.get_screenshot_as_png(), name=f"before-apply-{idx}", attachment_type=allure.attachment_type.PNG)

                with allure.step(f"[{idx}] Click Apply"):
                    apply_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'apply-btn')]"))
                    )
                    apply_button.click()
                    time.sleep(2)

                allure.attach(driver.get_screenshot_as_png(), name=f"after-apply-{idx}", attachment_type=allure.attachment_type.PNG)



    @allure.story("Verify Incidents Distribution Elements")
    def test_incidents_distribution_names(self, driver):
        with allure.step("Check if all expected names exist"):
            expected_names = {
                "Incidents Distribution": "//div[contains(@class, 'card_heading')]",
                "Total": "//span[contains(@class, 'table_heading')]/span[contains(., 'Total')]",
                "Total Area/Gate": "//span[contains(@class, 'table_heading')]/span[contains(., 'Total Area/Gate')]",
                "Pedestrian": "//span[contains(@class, 'table_heading')]/span[contains(., 'Pedestrian')]",
                "Vehicle": "//span[contains(@class, 'table_heading')]/span[contains(., 'Vehicle')]",
                "CPOF": "//span[contains(@class, 'table_heading')]/span[contains(., 'CPOF')]",
                "Total PPE": "//span[contains(@class, 'table_heading')]/span[contains(., 'Total PPE')]",
                "Vest": "//span[contains(@class, 'table_heading')]/span[contains(., 'Vest')]",
                "Helmet": "//span[contains(@class, 'table_heading')]/span[contains(., 'Helmet')]",
            }

            missing_names = []

            for name, xpath in expected_names.items():
                try:
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, xpath))
                    )
                    if not element.is_displayed():
                        missing_names.append(name)
                except Exception:
                    missing_names.append(name)
                    allure.attach(
                        driver.get_screenshot_as_png(),
                        name=f"missing_{name}",
                        attachment_type=allure.attachment_type.PNG
                    )

            assert not missing_names, f"Missing names: {missing_names}"

    @allure.story("User Sign Out")  # Scenario: User Sign Out
    def test_sign_out(self, driver):
        with allure.step("Click user dropdown"):
            dropdown_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.bi-chevron-down"))
        )
        dropdown_icon.click()
        allure.attach(driver.get_screenshot_as_png(),
                      name="dropdown-opened",
                      attachment_type=allure.attachment_type.PNG)

        with allure.step("Click sign out button"):
            signout_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'sign-out-btn')]"))
        )
        signout_button.click()
        allure.attach(driver.get_screenshot_as_png(),
                      name="signout-clicked",
                      attachment_type=allure.attachment_type.PNG)

        with allure.step("Verify sign out successful"):
            WebDriverWait(driver, 10).until(
            EC.url_contains("/auth/login")
        )
        allure.attach(driver.get_screenshot_as_png(),
                      name="signout-confirmed",
                      attachment_type=allure.attachment_type.PNG)
