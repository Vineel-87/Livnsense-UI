from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time


@given(u'the user has logged into the Autoliv dashboard')
def step_impl(context):
    context.driver.get("https://alv-vicas.livnsense.com/#/auth/login")

    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Username']"))
    )

    context.driver.find_element(By.XPATH, "//input[@placeholder='Username']").send_keys("madan")
    context.driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("Madan@123")
    context.driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]").click()

    WebDriverWait(context.driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//img[@alt='Autoliv']"))
    )


@then(u'the Autoliv logo should be visible at the top left')
def step_impl(context):
    logo = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//img[@alt='Autoliv']"))
    )
    assert logo.is_displayed(), "Autoliv logo is not visible at the top left."


@when(u'the user clicks the project dropdown')
def step_impl(context):
    WebDriverWait(context.driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.region-container select.dropdown"))
    )


@when(u'selects "AIB" from the list')
def step_impl(context):
    dropdown = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.region-container select.dropdown"))
    )
    select = Select(dropdown)

    # Re-select "AIB" if not already selected
    if select.first_selected_option.text.strip() != "AIB":
        select.select_by_visible_text("AIB")

    # Confirm dropdown reflects "AIB"
    WebDriverWait(context.driver, 10).until(
        lambda d: Select(d.find_element(By.CSS_SELECTOR, "div.region-container select.dropdown")).first_selected_option.text.strip() == "AIB"
    )


@then(u'the "AIB" project should be loaded successfully')
def step_impl(context):
    dropdown = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.region-container select.dropdown"))
    )
    selected_option = Select(dropdown).first_selected_option.text.strip()
    assert selected_option == "AIB", f"Expected 'AIB' but found '{selected_option}'"


@when('the "AIB" project is successfully loaded')
def step_impl(context):
    try:
        WebDriverWait(context.driver, 30).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )

        dropdown = WebDriverWait(context.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "select.dropdown"))
        )

        select = Select(dropdown)
        options = [opt.text.strip() for opt in select.options]

        if "AIB" not in options:
            raise AssertionError("AIB option not found in dropdown")

        if select.first_selected_option.text.strip() != "AIB":
            select.select_by_visible_text("AIB")

        WebDriverWait(context.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Overall Analytics')]"))
        )

    except Exception as e:
        context.driver.save_screenshot("aib_load_error.png")
        raise AssertionError(f"Failed to load AIB project: {str(e)}")


@then('the following elements should be visible')
def step_impl(context):
    expected_elements = [line.strip('- ').strip() for line in context.text.split('\n') if line.strip()]

    locators = {
        'Overall Analytics section': (By.XPATH, "//*[contains(text(), 'Overall Analytics')]"),
        'Overall Distribution section': (By.XPATH, "//*[contains(text(), 'Overall Distribution')]"),
        'Configuration button': (By.XPATH, "//*[contains(text(), 'Configuration')]"),
    }

    missing = []
    for element in expected_elements:
        try:
            WebDriverWait(context.driver, 10).until(
                EC.visibility_of_element_located(locators[element])
            )
        except:
            missing.append(element)

    if missing:
        raise AssertionError(f"Missing elements: {', '.join(missing)}")


@then('the Overall Distribution section should show no incidents')
def step_impl(context):
    try:
        message = WebDriverWait(context.driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.no-data-message"))
        )
        assert message.text.strip() == "No Incident", \
            f"Expected 'No Incident' but got '{message.text.strip()}'"
    except Exception as e:
        context.driver.save_screenshot("no_incident_error.png")
        raise AssertionError(f"No Incident validation failed: {str(e)}")

@then('the Incident Distribution section should display all safety components')
def step_impl(context):
    components = {
        'Total': (By.XPATH, "//*[contains(text(), 'Total')]"),
        'Total Area/Gate': (By.XPATH, "//*[contains(text(), 'Total Area/Gate')]"),
        'Unattended-Material': (By.XPATH, "//*[contains(text(), 'Unattended-Material')]"),
        'Pedestrian': (By.XPATH, "//*[contains(text(), 'Pedestrian')]"),
        'Vehicle': (By.XPATH, "//*[contains(text(), 'Vehicle')]"),
        'Total PPE': (By.XPATH, "//*[contains(text(), 'Total PPE')]"),
        'Vest': (By.XPATH, "//*[contains(text(), 'Vest')]"),
        'Helmet': (By.XPATH, "//*[contains(text(), 'Helmet')]")
    }

    errors = []
    for name, locator in components.items():
        try:
            element = WebDriverWait(context.driver, 10).until(
                EC.visibility_of_element_located(locator)
            )
            print(f"{name} component text: {element.text}")
        except Exception as e:
            errors.append(f"{name}: {str(e)}")

    if errors:
        raise AssertionError("Safety component issues:\n- " + "\n- ".join(errors))

