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

# ---------------------- WebDriver Setup ----------------------

@pytest.fixture(scope="module")
def driver():
    """Initialize and teardown the WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


# ---------------------- Login Test ----------------------

@allure.feature("Autoliv Dashboard")
@allure.story("Login and AIB Project Selection")
def test_autoliv_login_and_project_selection(driver):
    with allure.step("Open Autoliv login page"):
        driver.get("https://alv-vicas.livnsense.com/#/auth/login")

    with allure.step("Enter login credentials and sign in"):
        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Username']"))
        )
        username.send_keys("madan")

        password = driver.find_element(By.XPATH, "//input[@placeholder='Password']")
        password.send_keys("Madan@123")

        signin_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
        signin_btn.click()

    with allure.step("Verify successful login by checking Autoliv logo"):
        logo = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//img[@alt='Autoliv']"))
        )
        assert logo.is_displayed(), "Autoliv logo not displayed. Login may have failed."


# ---------------------- AIB Project Selection ----------------------

@allure.feature("Autoliv Dashboard")
@allure.story("Dashboard Element Validation after AIB Project Load")
def test_aib_dashboard_elements(driver):
    with allure.step("Select 'AIB' project from dropdown if not already selected"):
        dropdown = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "select.dropdown"))
        )
        select = Select(dropdown)
        if select.first_selected_option.text.strip() != "AIB":
            select.select_by_visible_text("AIB")
        assert select.first_selected_option.text.strip() == "AIB", "Failed to select AIB project."


# ---------------------- Calendar Popup Interaction ----------------------

@allure.feature("Calendar - Date Popup")
@allure.story("Dashboard Calendar Interaction")
def test_calendar_popup_interaction(driver):
    with allure.step("Ensure popup is not already open"):
        try:
            popup_open = driver.find_elements(By.CSS_SELECTOR, "div.datepicker-pop-card")
            if popup_open and popup_open[0].is_displayed():
                ActionChains(driver).move_by_offset(10, 10).click().perform()
                time.sleep(1)
        except Exception as e:
            print(f"Error during popup close: {e}")

    with allure.step("Open calendar popup"):
        try:
            calendar_trigger = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.form-control[style*='pointer']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", calendar_trigger)
            time.sleep(1)
            calendar_trigger.click()
            print("Clicked calendar trigger")

            # Retry for up to 10 seconds for popup to appear
            popup = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.datepicker-pop-card"))
            )

            assert popup.is_displayed(), "Calendar popup is not visible after click"
            allure.attach(driver.get_screenshot_as_png(), name="calendar_popup_open", attachment_type=allure.attachment_type.PNG)

        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(), name="calendar_popup_error", attachment_type=allure.attachment_type.PNG)
            pytest.fail(f"Failed to open calendar popup: {str(e)}")

    with allure.step("Click Today and verify popup closes"):
        try:
            today_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Today')]"))
            )
            today_button.click()
            print("Clicked 'Today' button")

            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.datepicker-pop-card"))
            )
        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(), name="calendar_interaction_error", attachment_type=allure.attachment_type.PNG)
            pytest.fail(f"Failed interacting with calendar: {str(e)}")

# ---------------------- Verify Calendar Time Period Buttons ----------------------


@allure.feature("Calendar - Date Popup")
@allure.story("Verify and Test All Time Period Buttons")
def test_all_time_period_buttons(driver):
    def reopen_calendar():
        """Helper function to reopen calendar popup"""
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
            # Highlight button for visibility
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

    # ------- CONTINUATION: DATE RANGE SELECTION TEST -------
    @allure.feature("Calendar - Date Popup")
    @allure.story("Verify Date Range Selection Functionality")
    def test_date_range_selection(driver):
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

        with allure.step("Open calendar popup for date range selection"):
            if not reopen_calendar():
                pytest.fail("Could not reopen calendar for date range selection test")

        with allure.step("Clear existing selection if visible"):
            try:
                clear_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Clear')]"))
                )
                clear_btn.click()
                print("Cleared previous date selection")
            except:
                print("No previous range to clear")

        with allure.step("Select custom date range"):
            try:
                # Select first date (start date)
                start_date = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//td[@class='available' or @class='today']"))
                )
                start_date.click()
                print("Selected start date")

                # Select end date
                end_date = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "(//td[@class='available'])[last()]"))
                )
                end_date.click()
                print("Selected end date")

                # Verify popup closed
                WebDriverWait(driver, 5).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.datepicker-pop-card"))
                )
                allure.attach(driver.get_screenshot_as_png(), name="date_range_selected",
                              attachment_type=allure.attachment_type.PNG)

            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="date_range_error",
                              attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Custom date range selection failed: {str(e)}")

        with allure.step("Verify date range displayed correctly"):
            try:
                date_display = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.form-control"))
                )
                assert "-" in date_display.text, f"Expected date range but found: {date_display.text}"
                print(f"Date range successfully selected: {date_display.text}")

            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="date_range_verify_error",
                              attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Failed to verify date range: {str(e)}")

        with allure.step("Select custom date range from CSV"):
          try:
            # Read test data from CSV
            csv_path = os.path.join(os.path.dirname(__file__), 'test_date_range.csv')

            if not os.path.exists(csv_path):
                pytest.fail(f"CSV file not found at: {csv_path}")

            with open('csv_path', mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                test_data = next(csv_reader)  # Get first row

            start_date_str = test_data['start_date']  # Expected format: DD/MM/YYYY
            end_date_str = test_data['end_date']  # Expected format: DD/MM/YYYY

            # Parse dates from CSV
            start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
            end_date = datetime.strptime(end_date_str, "%d/%m/%Y")

            # Format for verification (same as shown in screenshot)
            expected_display = f"{start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}"

            # Select start date
            start_day = start_date.day
            start_month = start_date.strftime("%b")  # Short month name (Mar, Apr, etc.)
            start_year = start_date.year

            # Select end date
            end_day = end_date.day
            end_month = end_date.strftime("%b")
            end_year = end_date.year

            # Navigate to start date month/year
            current_month_year = driver.find_element(By.CSS_SELECTOR, "div.datepicker-month-year").text
            target_start = f"{start_month} {start_year}"

            while current_month_year != target_start:
                prev_btn = driver.find_element(By.CSS_SELECTOR, "button.datepicker-prev")
                prev_btn.click()
                current_month_year = driver.find_element(By.CSS_SELECTOR, "div.datepicker-month-year").text

            # Click start date
            start_date_element = driver.find_element(By.XPATH,
                                                     f"//div[@class='datepicker-day' and text()='{start_day}']")
            start_date_element.click()

            # Navigate to end date month/year if different
            current_month_year = driver.find_element(By.CSS_SELECTOR, "div.datepicker-month-year").text
            target_end = f"{end_month} {end_year}"

            while current_month_year != target_end:
                next_btn = driver.find_element(By.CSS_SELECTOR, "button.datepicker-next")
                next_btn.click()
                current_month_year = driver.find_element(By.CSS_SELECTOR, "div.datepicker-month-year").text

            # Click end date
            end_date_element = driver.find_element(By.XPATH,
                                                   f"//div[@class='datepicker-day' and text()='{end_day}']")
            end_date_element.click()

            # Set time range (as shown in screenshot)
            start_time_input = driver.find_element(By.XPATH, "//input[@placeholder='12:00 AM']")
            start_time_input.clear()
            start_time_input.send_keys("12:00 AM")

            end_time_input = driver.find_element(By.XPATH, "//input[@placeholder='11:59 PM']")
            end_time_input.clear()
            end_time_input.send_keys("11:59 PM")

            # Click Apply button
            apply_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Apply')]")
            apply_btn.click()

            # Verify the displayed range matches expected format
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.datepicker-pop-card"))
            )

            date_display = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.form-control"))
            ).text

            assert date_display == expected_display, (
                f"Date range display mismatch. Expected: {expected_display}, Actual: {date_display}"
            )

            allure.attach(driver.get_screenshot_as_png(),
                          name="date_range_selected",
                          attachment_type=allure.attachment_type.PNG)
            print(f"Successfully selected date range: {date_display}")

          except Exception as e:
            allure.attach(driver.get_screenshot_as_png(),
                          name="date_range_selection_failed",
                          attachment_type=allure.attachment_type.PNG)
            pytest.fail(f"Date range selection test failed: {str(e)}")