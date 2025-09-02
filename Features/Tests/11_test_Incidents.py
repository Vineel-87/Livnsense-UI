import pytest
import allure
import time
import csv
import os
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

@allure.feature("Dashboard Workflow")  # Feature: Dashboard Workflow
class TestDashboardWorkflow:

    @pytest.fixture(scope="class")
    def driver(self):
        options = Options()
        # Add all your clean options here exactly as in your first script
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

    @allure.story("Successful Login")  # Scenario: Successful Login
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
            driver.find_element(By.XPATH, "//input[@placeholder='Username']").send_keys("pydi.vineel")
            driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("Vineel@lns123")
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
                          attachment_type=allure.attachment_type.PNG)\

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

        with allure.step("Select AIB project"):
            select.select_by_visible_text("AIB")

            time.sleep(1)
            allure.attach(driver.get_screenshot_as_png(),
                          name="aib-selected",
                          attachment_type=allure.attachment_type.PNG)
 
    @allure.story("Verify Gate Incidents Section")  # Scenario: Verify Gate Incidents Section
    def test_gate_incidents_section(self, driver):
        with allure.step("Navigate to Gate Incidents section"):
            gate_incidents = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Gate Incidents')]"))
            )
            gate_incidents.click()
            allure.attach(driver.get_screenshot_as_png(),
                          name="gate-incidents-expanded",
                          attachment_type=allure.attachment_type.PNG)


        with allure.step("Click on Gate Incidents sub-menu"):
            gate1_incidents = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Gate Incidents')]"))
            )
            gate1_incidents.click()

            time.sleep(1)
            allure.attach(driver.get_screenshot_as_png(),
                          name="gate1-incidents-selected",
                          attachment_type=allure.attachment_type.PNG)   

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
        
    @allure.story("Gate Video Incidents Test")
    def test_gate_video_incidents(self, driver):
        # Step 1: Open incident details
        with allure.step("Click first View details button and verify"):
            try:
                first_view_details = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.view-details"))
                )
                first_view_details.click()

                WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, ".details-container"))
                )
                allure.attach(driver.get_screenshot_as_png(),
                            name="details-opened",
                            attachment_type=allure.attachment_type.PNG)

            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(),
                            name="view-details-failed",
                            attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Failed to open details view: {str(e)}")

        # Step 2: Switch to video view mode
        with allure.step("Switch to video view mode"):
            try:
                video_mode_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".view-mode-btn:not(.disabled)"))
                )
                video_mode_btn.click()
                time.sleep(2)

                allure.attach(driver.get_screenshot_as_png(),
                            name="video-mode-activated",
                            attachment_type=allure.attachment_type.PNG)

            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(),
                            name="video-mode-failed",
                            attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Failed to switch to video mode: {str(e)}")

        # Step 3: Verify video playback
        with allure.step("Verify video playback"):
            try:
                video_player = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "video-player, [class*='video-container']"))
                )

                video_duration = 10  # default fallback
                try:
                    duration_element = driver.find_element(By.CSS_SELECTOR, ".duration, .video-time")
                    duration_text = duration_element.text
                    if ":" in duration_text:
                        mins, secs = map(int, duration_text.split(':'))
                        video_duration = mins * 60 + secs
                except:
                    pass  # fallback to default if parsing fails

                wait_time = video_duration + 5
                print(f"Waiting {wait_time} seconds for video playback")
                time.sleep(wait_time)

                allure.attach(driver.get_screenshot_as_png(),
                            name="video-playback-complete",
                            attachment_type=allure.attachment_type.PNG)

                print("Video playback completed (assumed)")

            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(),
                            name="video-playback-error",
                            attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Video playback verification failed: {str(e)}")

       
        with allure.step("Close video using close button"):
            try:
                close_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.close-icon"))
                )
                # Scroll into view if needed
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", close_btn)
                time.sleep(0.5)
                
                close_btn.click()
                time.sleep(1)  # Small pause for the close action
                
                # Verify video is closed
                WebDriverWait(driver, 5).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, "video-player")))
                
                allure.attach(driver.get_screenshot_as_png(),
                            name="video-closed",
                            attachment_type=allure.attachment_type.PNG)
                
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(),
                            name="close-video-failed",
                            attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Failed to close video: {str(e)}")