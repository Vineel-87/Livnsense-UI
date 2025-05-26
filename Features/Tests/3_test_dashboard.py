import pytest
import allure
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@allure.feature("Autoliv Dashboard")
@allure.story("Login and AIB Project Selection")
def test_autoliv_login_and_project_selection(driver):
    with allure.step("Open login page"):
        driver.get("https://alv-vicas.livnsense.com/#/auth/login")

    with allure.step("Login to Autoliv"):
        driver.find_element(By.XPATH, "//input[@placeholder='Username']").send_keys("pydi.vineel")
        driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("Vineel@lns123")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]").click()

    with allure.step("Verify Autoliv logo is displayed"):
        logo = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//img[@alt='Autoliv']"))
        )
        assert logo.is_displayed()


@allure.feature("Autoliv Dashboard")
@allure.story("Dashboard Element Validation after AIB Project Load")
def test_aib_dashboard_elements(driver):
    with allure.step("Ensure AIB is selected from dropdown"):
        dropdown = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "select.dropdown"))
        )
        select = Select(dropdown)
        if select.first_selected_option.text.strip() != "AIB":
            select.select_by_visible_text("AIB")
        assert select.first_selected_option.text.strip() == "AIB"

    with allure.step("Check visibility of dashboard sections"):
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Overall Analytics')]"))
        )
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Overall Distribution')]"))
        )

    with allure.step("Verify 'No Incident' message is shown"):
        no_incident_msg = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.no-data-message"))
        )
        assert no_incident_msg.text.strip() == "No Incident"

    with allure.step("Validate all safety components in Incident Distribution"):
        labels = [
            'Total', 'Total Area/Gate', 'Unattended-Material', 'Pedestrian',
            'Vehicle', 'Total PPE', 'Vest', 'Helmet'
        ]
        for label in labels:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(), '{label}')]"))
            )
