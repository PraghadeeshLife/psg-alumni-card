from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = FastAPI()

@app.get("/scrape")
def scrape():
    # Setup Selenium (Example using Chrome WebDriver)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Ensure headless mode for servers
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

    # Point to the Chromium binary explicitly
    options.binary_location = "/usr/bin/chromium"
    driver = webdriver.Chrome(options=options)

    # Open a webpage
    driver.get('https://alumni.psgitech.ac.in/icard/verify?id=1323433&name=96d669e0dbb9ab6b19b56d3f9fb74e7a')

    wait = WebDriverWait(driver, 10)

    # Use XPath to extract content
    element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/ui-view/div/div/div/div[1]/div[3]")))
    content = element.text

    driver.quit()
    return {"content": content}
