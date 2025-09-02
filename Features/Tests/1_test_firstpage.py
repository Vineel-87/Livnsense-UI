import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Login and Project Selection")
@allure.story("Login to Autoliv dashboard and verify project selection")
def test_login_and_project_selection():
    with allure.step("Open browser and go to Autoliv dashboard login"):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://alv-vicas.livnsense.com/#/auth/login")

    try:
        with allure.step("Login with valid credentials"):
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Username']"))
            )
            driver.find_element(By.XPATH, "//input[@placeholder='Username']").send_keys("pydi.vineel")
            driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("vineel@lns123")
            driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]").click()

        with allure.step("Verify Autoliv logo is visible"):
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//img[@alt='Autoliv']"))
            )

        with allure.step("Wait for project dropdown to be visible"):
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.region-container select.dropdown"))
            )

        with allure.step("Click and select 'AIB' project from dropdown"):
            dropdown = driver.find_element(By.CSS_SELECTOR, "div.region-container select.dropdown")
            select = Select(dropdown)
            print("Available options:")
            for option in select.options:
                print(option.text)
            select.select_by_visible_text("AIB")

        with allure.step("Verify AIB is selected"):
            selected_option = select.first_selected_option
            assert selected_option.text.strip() == "AIB", \
                f"Expected 'AIB' but got {selected_option.text.strip()}"

        with allure.step("Take success screenshot"):
            driver.save_screenshot("aib_selected_final.png")
            allure.attach.file("aib_selected_final.png", name="AIB Selected", attachment_type=allure.attachment_type.PNG)

    except Exception as e:
        driver.save_screenshot("error_final.png")
        allure.attach.file("error_final.png", name="Error Screenshot", attachment_type=allure.attachment_type.PNG)
        pytest.fail(f"Test failed: {str(e)}")

    finally:
        driver.quit()
