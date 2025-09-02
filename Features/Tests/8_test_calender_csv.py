import pytest
import allure
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature("Dashboard Workflow")
class TestDashboardWorkflow:

    @pytest.fixture(scope="class", autouse=True)
    def driver(self, request):
        driver = webdriver.Chrome()
        driver.maximize_window()
        request.cls.driver = driver
        yield driver
        driver.quit()

    @allure.story("Login to VICAS Dashboard")
    def test_login(self, driver):
        driver.get("https://alv-vicas.livnsense.com/#/auth/login")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Username']")))

        driver.find_element(By.XPATH, "//input[@placeholder='Username']").send_keys("pydi.vineel")
        driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("Vineel@lns123")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]").click()

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//img[@alt='Autoliv']")))
        allure.attach(driver.get_screenshot_as_png(), name="logged-in", attachment_type=allure.attachment_type.PNG)

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