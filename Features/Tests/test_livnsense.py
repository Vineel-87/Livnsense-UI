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
        """Test all credentials from CSV file"""
        # Ensure that the CSV file is correctly located
        csv_path = os.path.join(os.path.dirname(__file__), 'test_file.csv')

        # Check if the file exists
        if not os.path.exists(csv_path):
            pytest.fail(f"CSV file not found at: {csv_path}")

        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                username = row['Username'].strip()  # Remove any leading/trailing spaces
                password = row['Password'].strip()  # Remove any leading/trailing spaces

                with allure.step(f"Testing: {username}"):
                    browser.get("https://alv-vicas.livnsense.com/#/auth/login")

                    # Clear the fields and enter credentials
                    username_field = browser.find_element(By.XPATH, "//input[@name='username']")
                    username_field.clear()  # Clear any existing value
                    username_field.send_keys(username)  # Enter username

                    password_field = browser.find_element(By.XPATH, "//input[@name='password']")
                    password_field.clear()  # Clear any existing value
                    password_field.send_keys(password)  # Enter password

                    # Click the login button
                    login_button = browser.find_element(By.XPATH, "//button[@class='sign-in-btn']")
                    login_button.click()

                    # Verification
                    try:
                        error = WebDriverWait(browser, 5).until(
                            EC.visibility_of_element_located(
                                (By.XPATH, "//*[contains(text(), 'User is not registered. Please Contact admin.')]"))
                        )
                        allure.attach(
                            browser.get_screenshot_as_png(),
                            name=f"failure_{username}",
                            attachment_type=allure.attachment_type.PNG
                        )
                        pytest.fail(f"Login failed for {username}")
                    except:
                        allure.attach(
                            browser.get_screenshot_as_png(),
                            name=f"success_{username}",
                            attachment_type=allure.attachment_type.PNG
                        )
