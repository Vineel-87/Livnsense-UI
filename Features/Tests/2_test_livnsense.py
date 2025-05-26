import pytest
import allure
import time
import csv
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains




@pytest.fixture(scope="module")
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@allure.feature("VICAS Login Tests")
class TestLoginFunctionality:

    @allure.story("UI Elements Verification")
    def test_login_page_elements(self, browser):
        """Verify all required UI elements exist"""
        browser.get("https://alv-vicas.livnsense.com/#/auth/login")

        with allure.step("Check welcome heading"):
            heading = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Welcome to VICAS')]"))
            )
            assert heading.is_displayed()

        with allure.step("Verify username field exists"):
            username = browser.find_element(By.XPATH, "//input[@name='username']")
            assert username.is_displayed()

        with allure.step("Verify password field exists"):
            password = browser.find_element(By.XPATH, "//input[@name='password']")
            assert password.is_displayed()

    @allure.story("Login Button State")
    def test_button_enable_logic(self, browser):
        """Test button enables only with valid credentials"""
        browser.get("https://alv-vicas.livnsense.com/#/auth/login")

        with allure.step("Check initial disabled state"):
            btn = browser.find_element(By.XPATH, "//button[@class='sign-in-btn']")
            assert not btn.is_enabled()

        with allure.step("Test with valid credentials"):
            browser.find_element(By.XPATH, "//input[@name='username']").send_keys("valid_user")
            browser.find_element(By.XPATH, "//input[@name='password']").send_keys("valid_pass")
            assert browser.find_element(By.XPATH, "//button[@class='sign-in-btn']").is_enabled()

    @allure.story("CSV Data Driven Tests")
    def test_credentials_from_csv(self, browser):
        """Test all credentials from CSV file and capture screenshots on both success and failure"""

        csv_path = os.path.join(os.path.dirname(__file__), 'test_file.csv')

        if not os.path.exists(csv_path):
            pytest.fail(f"CSV file not found at: {csv_path}")

        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                username = row['Username'].strip()
                password = row['Password'].strip()

                with allure.step(f"Testing with username: {username}"):
                    browser.get("https://alv-vicas.livnsense.com/#/auth/login")

                    # Fill username and password
                    username_field = browser.find_element(By.XPATH, "//input[@name='username']")
                    username_field.clear()
                    username_field.send_keys(username)

                    password_field = browser.find_element(By.XPATH, "//input[@name='password']")
                    password_field.clear()
                    password_field.send_keys(password)

                    login_button = browser.find_element(By.XPATH, "//button[@class='sign-in-btn']")
                    login_button.click()

                    time.sleep(1)  # Allow time for the login to process and page to render

                    try:
                        # Wait and check for failure message
                        WebDriverWait(browser, 3).until(
                            EC.visibility_of_element_located(
                                (By.XPATH, "//*[contains(text(), 'User is not registered. Please Contact admin.')]"))
                        )

                    except Exception:
                        # No failure message found = assumed success
                        allure.attach(
                            browser.get_screenshot_as_png(),
                            name=f"Success_{username}",
                            attachment_type=allure.attachment_type.PNG
                        )
                    else:
                        # If failure message was found
                        allure.attach(
                            browser.get_screenshot_as_png(),
                            name=f"Failure_{username}",
                            attachment_type=allure.attachment_type.PNG
                        )
                        pytest.fail(f"Login failed for {username}")