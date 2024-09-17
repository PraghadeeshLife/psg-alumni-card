import logging
from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import WebDriverException

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_driver():
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    firefox_options.add_argument("--no-sandbox")
    firefox_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(executable_path='/usr/local/bin/geckodriver')
    
    try:
        driver = webdriver.Firefox(options=firefox_options, service=service)
        return driver
    except WebDriverException as e:
        logger.error(f"Failed to initialize WebDriver: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to initialize WebDriver")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/scrape/{url:path}")
async def scrape(url: str):
    driver = None
    try:
        driver = get_driver()
        driver.get(f"https://{url}")
        title = driver.title
        return {"url": url, "title": title}
    except WebDriverException as e:
        logger.error(f"WebDriver error while scraping {url}: {str(e)}")
        raise HTTPException(status_code=500, detail="WebDriver error occurred during scraping")
    finally:
        if driver:
            driver.quit()

@app.on_event("startup")
async def startup_event():
    logger.info("Checking WebDriver setup...")
    try:
        driver = get_driver()
        driver.quit()
        logger.info("WebDriver setup successful")
    except Exception as e:
        logger.error(f"WebDriver setup failed: {str(e)}")