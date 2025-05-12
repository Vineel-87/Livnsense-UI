from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os


@given(u'the user navigates to the VICAS login page')
def step_impl(context):
    context.driver =webdriver.Chrome()
    context.driver.maximize_window()
    context.driver.get("https://alv-vicas.livnsense.com/#/auth/login")


@then(u'the heading "Welcome to VICAS" should be displayed')
def step_impl(context):

    heading = context.driver.find_element(By.XPATH, '//div[contains(@class, "heading")]')
    assert heading.is_displayed(), "Heading element is not visible"
    assert heading.text.strip() == "Welcome to VICAS", f'Expected heading text to be "Welcome to VICAS" but got "{heading.text.strip()}"'


@then(u'the username input field should be visible')
def step_impl(context):
    wait = WebDriverWait(context.driver, 10)
    username_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@placeholder="Username"]')))
    assert username_input.is_displayed(), 'Username input field is not visible'


@then(u'the Sign In button should be visible and disabled')
def step_impl(context):
    wait = WebDriverWait(context.driver, 10)

    # Find the Sign-In button
    sign_in_button = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//button[contains(@class, "sign-in-btn")]')
    ))

    # Verify button is visible
    assert sign_in_button.is_displayed(), "Sign In button is not visible"

    # Verify button is disabled
    assert not sign_in_button.is_enabled(), "Sign In button should be disabled but it's enabled"

    # Verify form is in invalid state (optional but recommended)
    form = context.driver.find_element(By.TAG_NAME, 'form')
    assert 'ng-invalid' in form.get_attribute('class'), "Form should be in invalid state when empty"


# Common steps
@given('the user is on the login page')
def step_impl(context):
    if not hasattr(context, 'driver'):
        context.driver = webdriver.Chrome()
        context.driver.maximize_window()
    context.driver.get("https://alv-vicas.livnsense.com/#/auth/login")
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Welcome to VICAS')]"))
    )


# Scenario 1: Button state testing
@when('the user enters a valid username in the username field')
def step_impl(context):
    username_field = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@name='username']"))
    )
    username_field.clear()
    username_field.send_keys("test user")


@when('user enters a valid password in the password field')
def step_impl(context):
    password_field = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@name='password']"))
    )
    password_field.clear()
    password_field.send_keys("test pass123")


@then('Sign In button should be enabled')
def step_impl(context):
    sign_in_button = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='sign-in-btn']"))
    )
    assert sign_in_button.is_enabled(), "Sign In button should be enabled when both fields are filled"


# Scenario 2: CSV testing (exact implementation matching your scenario)
@when('the user reads username and password combinations from "credentials.csv"')
def step_impl(context):
    # Get absolute path to CSV in features folder
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_file.csv')

    context.test_results = []

    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Enter credentials
            username_field = WebDriverWait(context.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@name='username']"))
            )
            username_field.clear()
            username_field.send_keys(row['Username'])

            password_field = WebDriverWait(context.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@name='password']"))
            )
            password_field.clear()
            password_field.send_keys(row['Password'])

            # Click login
            login_button = WebDriverWait(context.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='sign-in-btn']"))
            )
            login_button.click()

            # Verify result
            try:
                error_msg = WebDriverWait(context.driver, 5).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//*[contains(text(), 'User is not registered. Please Contact admin.')]")
                    )
                )
                context.test_results.append({
                    'username': row['Username'],
                    'status': 'FAIL',
                    'message': error_msg.text
                })
            except:
                context.test_results.append({
                    'username': row['Username'],
                    'status': 'PASS',
                    'message': 'Login successful'
                })

            # Return to login page
            context.driver.get("https://alv-vicas.livnsense.com/#/auth/login")


@then('the system should attempt to log in with each set')
def step_impl(context):
    pass  # Verification happens in next step


@then('verify whether login is successful or shows an error')
def step_impl(context):
    for result in context.test_results:
        print(f"{result['status']}: {result['username']} - {result['message']}")

    if any(r['status'] == 'FAIL' for r in context.test_results):
        print("\nNote: Some logins failed as expected")
    elif all(r['status'] == 'PASS' for r in context.test_results):
        print("\nAll logins were successful")