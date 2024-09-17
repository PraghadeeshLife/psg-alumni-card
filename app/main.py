from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

app = FastAPI()

# Automatically install the correct version of ChromeDriver
chromedriver_autoinstaller.install()

@app.get("/scrape")
def scrape(url: str, xpath: str):
    # Set up Chrome in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Launch the browser with these options
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Open the URL
        driver.get(url)

        # Find the element using XPath
        element = driver.find_element(By.XPATH, xpath)
        
        # Return the text content of the element
        return {"content": element.text}
    except Exception as e:
        # Return an error if something goes wrong
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        # Quit the browser after scraping
        driver.quit()
