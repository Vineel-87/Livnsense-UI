from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def create_clean_chrome_driver():
    options = Options()

    # ✅ Suppress Chrome automation banners
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--incognito")

    driver = webdriver.Chrome(options=options)
    return driver

def test_login_without_banners():
    driver = create_clean_chrome_driver()
    driver.get("https://alv-vicas.livnsense.com/#/auth/login")

    # Use explicit wait until elements are present
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Username']"))
    )

    # ✅ Use correct locators
    driver.find_element(By.XPATH, "//input[@placeholder='Username']").send_keys("madan")
    driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("Madan@123")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]").click()

    time.sleep(5)
    print("Login successful. URL:", driver.current_url)
    driver.quit()

if __name__ == "__main__":
    test_login_without_banners()
