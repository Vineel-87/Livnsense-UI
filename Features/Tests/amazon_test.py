import csv
import time
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

@allure.feature("Amazon Fashion Search")
class TestAmazonSearch:

    @pytest.fixture(scope="class")
    def driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=chrome_options)
        yield driver
        driver.quit()

    @allure.story("Keyword Search on Amazon Fashion")
    def test_keyword_search(self, driver):
        """Search Amazon Fashion using 100 keywords from file"""
        try:
            # Load keywords
            with open("keywords.txt", "r") as f:
                keywords = [line.strip() for line in f.readlines()[:100]]  # Limit to 100
            
            results = []
            
            # Navigate to Amazon
            driver.get("https://www.amazon.in")
            time.sleep(2)
            
            # Close location popup if appears
            try:
                driver.find_element(By.XPATH, "//input[@data-action-type='DISMISS']").click()
                time.sleep(1)
            except:
                pass
            
            # Click on Fashion category
            driver.find_element(By.XPATH, "//a[contains(text(),'Fashion')]").click()
            time.sleep(3)
            
            # Perform searches
            for idx, keyword in enumerate(keywords, 1):
                try:
                    # Enter keyword in search box
                    search_box = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@id='twotabsearchtextbox']"))
                    )
                    search_box.clear()
                    search_box.send_keys(keyword)
                    search_box.send_keys(Keys.RETURN)
                    time.sleep(3)  # Wait for results
                    
                    # Get result count
                    result_count = driver.find_element(By.XPATH, "//div[@data-cel-widget='search_result_0']")
                    results.append({
                        "S.No": idx,
                        "Keyword": keyword,
                        "Results": "Found" if result_count else "Not Found",
                        "Status": "Success"
                    })
                    
                    # Go back to fashion page
                    driver.find_element(By.XPATH, "//a[contains(text(),'Fashion')]").click()
                    time.sleep(2)
                    
                except Exception as e:
                    results.append({
                        "S.No": idx,
                        "Keyword": keyword,
                        "Results": "Error",
                        "Status": f"Failed: {str(e)}"
                    })
                    # Recover by reloading fashion page
                    driver.get("https://www.amazon.in/fashion")
                    time.sleep(3)
            
            # Save to CSV
            with open("keywords.txt", "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["S.No", "Keyword", "Results", "Status"])
                writer.writeheader()
                writer.writerows(results)
                
            allure.attach.file("amazon_search_results.csv", name="search-results", attachment_type=allure.attachment_type.CSV)
            
        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(), name="error", attachment_type=allure.attachment_type.PNG)
            pytest.fail(f"Amazon search failed: {str(e)}")

if __name__ == "__main__":
    pytest.main(["-v", "--alluredir=./reports"])