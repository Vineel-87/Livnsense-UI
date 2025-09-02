import pytest
import allure
import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

@allure.feature("Dashboard Workflow")
class TestDashboardWorkflow:

    @pytest.fixture(scope="class")
    def driver(self):
        options = Options()
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

    @allure.story("Successful Login")
    def test_login(self, driver):
        with allure.step("Navigate to login page"):
            driver.get("https://alv-vicas.livnsense.com/#/auth/login")
            allure.attach(driver.get_screenshot_as_png(), name="login-page", attachment_type=allure.attachment_type.PNG)

        with allure.step("Enter credentials"):
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Username']")))
            driver.find_element(By.XPATH, "//input[@placeholder='Username']").send_keys("pydi.vineel")
            driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("Vineel@lns123")
            allure.attach(driver.get_screenshot_as_png(), name="credentials-entered", attachment_type=allure.attachment_type.PNG)

        with allure.step("Submit login"):
            driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]").click()

        with allure.step("Verify successful login"):
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//img[@alt='Autoliv']")))
            allure.attach(driver.get_screenshot_as_png(), name="dashboard-loaded", attachment_type=allure.attachment_type.PNG)

    @allure.story("Project Selection")
    def test_project_selection(self, driver):
        with allure.step("Locate project dropdown"):
            dropdown = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "select.dropdown")))
            allure.attach(driver.get_screenshot_as_png(), name="project-dropdown", attachment_type=allure.attachment_type.PNG)

        with allure.step("Verify default project is AIB"):
            select = Select(dropdown)
            assert select.first_selected_option.text == "AIB", f"Expected default project AIB but got {select.first_selected_option.text}"

        with allure.step("Select AIB project"):
            select.select_by_visible_text("AIB")
            time.sleep(1)
            allure.attach(driver.get_screenshot_as_png(), name="aib-selected", attachment_type=allure.attachment_type.PNG)

    @allure.story("Verify Manage Section")
    def test_manage_incidents_section(self, driver):
        with allure.step("Navigate to Manage section"):
            manage_menu = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Manage')]")))
            manage_menu.click()
            allure.attach(driver.get_screenshot_as_png(), name="Manage-incidents-expanded", attachment_type=allure.attachment_type.PNG)

        with allure.step("Click on Manage Users"):
            manage_users = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Manage Users')]")))
            manage_users.click()
            time.sleep(1)
            allure.attach(driver.get_screenshot_as_png(), name="manage_users-selected", attachment_type=allure.attachment_type.PNG)

    @allure.story("Complete User Management Flow from CSV")
    @pytest.mark.usefixtures("driver")
    def test_complete_user_management_flow(self, driver):
        csv_path = os.path.join(os.getcwd(), "test_manage_users1.csv")
        failed_rows = []
        passed_rows = []

        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row_number, row in enumerate(reader, 1):
                with allure.step(f"Processing user #{row_number}: {row['username']}"):
                    try:
                        # ===== 1. INITIATE ADD USER =====
                        try:
                            WebDriverWait(driver, 15).until(
                                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'add-btn')]"))
                            ).click()
                            time.sleep(1)  # Form animation
                        except Exception:
                            driver.refresh()
                            WebDriverWait(driver, 15).until(
                                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'add-btn')]"))
                            ).click()
                            time.sleep(1)

                        # ===== 2. FILL BASIC FIELDS =====
                        field_map = {
                            'email': ("//input[@placeholder='Company mail ID']", row['email']),
                            'username': ("//input[@placeholder='Username']", row['username']),
                            'name': ("//input[@placeholder='Name']", row['name']),
                            'contact': ("//input[@placeholder='Contact number']", row['contact_details'])
                        }

                        for field, (locator, value) in field_map.items():
                            element = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, locator))
                            )
                            element.clear()
                            element.send_keys(value)

                        # ===== 3. HANDLE DROPDOWNS =====
                        Select(driver.find_element(By.ID, "addrole")).select_by_visible_text(row['role'])
                        Select(driver.find_element(By.ID, "addstatus")).select_by_visible_text(row['status'])

                        # ===== 4. GATE SELECTION =====
                        def select_gates():
                            try:
                                gate_dropdown = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.XPATH, "//*[contains(@placeholder, 'Select Gates')]"))
                                )
                                gate_dropdown.click()

                                # Clear existing selections
                                try:
                                    driver.find_element(By.CSS_SELECTOR, ".mat-select-clear, .mat-mdc-select-clear").click()
                                except:
                                    pass

                                gates = [g.strip('"').strip() for g in row['gates'].split(',')]
                                for gate in gates:
                                    WebDriverWait(driver, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, f"//mat-option//span[contains(., '{gate}')]"))
                                    ).click()

                                driver.find_element(By.TAG_NAME, 'body').click()
                            except Exception as e:
                                print(f"Gate selection warning: {str(e)}")
                                raise

                        # ===== 5. VEHICLE SELECTION =====
                        def select_vehicles():
                            try:
                                vehicle_dropdown = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.XPATH, "//*[contains(@placeholder, 'Select Vehicles')]"))
                                )
                                vehicle_dropdown.click()

                                # Clear existing selections
                                try:
                                    driver.find_element(By.CSS_SELECTOR, ".mat-select-clear, .mat-mdc-select-clear").click()
                                except:
                                    pass

                                vehicle = row['vehicles'].strip('"').strip()
                                WebDriverWait(driver, 5).until(
                                    EC.element_to_be_clickable((By.XPATH, f"//mat-option//span[contains(., '{vehicle}')]"))
                                ).click()

                                driver.find_element(By.TAG_NAME, 'body').click()
                            except Exception as e:
                                print(f"Vehicle selection warning: {str(e)}")
                                raise

                        # Retry mechanism for dropdown selections
                        for attempt in range(3):
                            try:
                                select_gates()
                                select_vehicles()
                                break
                            except Exception as e:
                                if attempt == 2:
                                    raise
                                driver.refresh()
                                time.sleep(2)
                                continue

                        # ===== 6. SAVE USER =====
                        save_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'save-button')]"))
                        )
                        save_button.click()

                        try:
                            WebDriverWait(driver, 10).until(
                                EC.invisibility_of_element_located((By.XPATH, "//button[contains(@class, 'save-button')]"))
                            )
                            passed_rows.append(row_number)
                            allure.attach(driver.get_screenshot_as_png(),
                                        name=f"success_row_{row_number}",
                                        attachment_type=allure.attachment_type.PNG)
                        except:
                            raise Exception("Save operation failed")

                        # ===== 7. PREPARE FOR NEXT USER =====
                        WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'add-btn')]"))
                        )

                    except Exception as e:
                        failed_rows.append(row_number)
                        error_msg = f"Row {row_number} failed: {str(e)}"
                        print(error_msg)
                        allure.attach(
                            driver.get_screenshot_as_png(),
                            name=f"failure_row_{row_number}",
                            attachment_type=allure.attachment_type.PNG
                        )
                        allure.attach(error_msg, name="Error Details")

                        # Reset state
                        try:
                            driver.refresh()
                        except:
                            pass
                        continue

        # Final test status
        if failed_rows:
            pytest.fail(f"Test completed with failures in rows: {failed_rows}. Passed rows: {passed_rows}")
        else:
            print(f"All {len(passed_rows)} rows processed successfully")