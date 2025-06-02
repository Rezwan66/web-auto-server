from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def fill_form(title: str, details: str):
    # 1. Launch headless chrome
    chrome_options = Options()
    #chrome_options.add_argument("--headless") #sets headless mode
    driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
    # 2. point to our form-filling page route
    driver.get("http://localhost:5173/form")
    time.sleep(3) #page loading time
    # 3. finding the inputs by their 'name' atributes
    title_input = driver.find_element(By.NAME, "title")
    details_input = driver.find_element(By.NAME, "details")
    # 4. Typing in the values
    title_input.send_keys(title)
    details_input.send_keys(details)
    # 5. clicking the "Post" button (by its visible text)
    post_button = driver.find_element(By.XPATH, "//button[text()='Post']")
    post_button.click()

    time.sleep(3) #waiting for form submission
    driver.quit()

if __name__=="__main__":
    # need to change here to test
    fill_form("Automated test title", "Automated test details of story")
    print("✅ Script ran—check your React UI to see if the form submitted.")
