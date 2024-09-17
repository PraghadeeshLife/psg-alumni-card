from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = FastAPI()

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/scrape/{url:path}")
async def scrape(url: str):
    driver = get_driver()
    driver.get(f"https://{url}")
    title = driver.title
    driver.quit()
    return {"url": url, "title": title}
