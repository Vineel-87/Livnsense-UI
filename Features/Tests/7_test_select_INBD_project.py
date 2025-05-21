import pytest
import allure
import time
import  csv
import os
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains



@allure.feature("Dashboard Workflow")  # Feature: Dashboard Workflow
class TestDashboardWorkflow:

    @pytest.fixture(scope="class")
    def driver(self):
        driver = webdriver.Chrome()
        driver.maximize_window()
        yield driver
        driver.quit()

    @allure.story("Successful Login")
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

    @allure.story("Verify and Test All Time Period Buttons")
    def test2_all_time_period_buttons(self, driver):
        def reopen1_calendar():
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
                # Open the calendar
                calendar_trigger = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.form-control[style*='pointer']"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", calendar_trigger)
                time.sleep(1)
                calendar_trigger.click()

                # Wait for popup to appear
                popup = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.datepicker-pop-card"))
                )
                assert popup.is_displayed()

                # Get the input field
                date_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Select Date Range']")

                # Get current date value
                current_date = date_input.get_attribute("ng-reflect-model") or date_input.get_attribute("value")
                print(f"Current date in field: {current_date}")

                # Clear the current date range
                date_input.clear()
                time.sleep(1)  # Allow time for the clear to take effect

                # Verify the field is now empty
                cleared_value = date_input.get_attribute("value")
                assert not cleared_value, f"Expected empty field but got {cleared_value}"

                # Verify placeholder shows "Select Date Range"
                placeholder_text = date_input.get_attribute("placeholder")
                assert placeholder_text == "Select Date Range", \
                    f"Expected placeholder 'Select Date Range' but got '{placeholder_text}'"

                allure.attach(driver.get_screenshot_as_png(),
                              name="calendar_cleared",
                              attachment_type=allure.attachment_type.PNG)

                # Reopen calendar to verify cleared state visually
                if reopen1_calendar():
                    # Additional verifications can be added here if needed
                    pass

                allure.attach(driver.get_screenshot_as_png(),
                              name="calendar_opened",
                              attachment_type=allure.attachment_type.PNG)

                # Now test with random date ranges from CSV
                with allure.step("Test with random date ranges from CSV"):
                    try:
                        # Read date ranges from CSV file
                        with open('test_date_range.csv', 'r') as file:
                            reader = csv.reader(file)
                            date_ranges = [row[0] for row in reader if row]  # Skip empty rows

                        if not date_ranges:
                            pytest.skip("No date ranges found in CSV file")

                        # Select a random date range
                        random_date_range = random.choice(date_ranges)
                        print(f"Testing with date range: {random_date_range}")

                        # Enter the random date range
                        date_input.clear()
                        date_input.send_keys(random_date_range)
                        time.sleep(1)  # Allow time for the date to be applied

                        # Verify the date range was applied
                        entered_value = date_input.get_attribute("value")
                        assert entered_value == random_date_range, \
                            f"Expected '{random_date_range}' but got '{entered_value}'"

                        allure.attach(driver.get_screenshot_as_png(),
                                      name="random_date_applied",
                                      attachment_type=allure.attachment_type.PNG)

                        # Optional: Reopen calendar to verify the selected range visually
                        if reopen1_calendar():
                            time.sleep(1)  # Just for visual verification

                    except Exception as e:
                        allure.attach(driver.get_screenshot_as_png(),
                                      name="random_date_failed",
                                      attachment_type=allure.attachment_type.PNG)
                        pytest.fail(f"Failed during random date range test: {str(e)}")

            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(),
                              name="calendar_open_failed",
                              attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Failed during calendar operations: {str(e)}")



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

