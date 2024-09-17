from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

app = FastAPI()

def get_driver():
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    
    driver = webdriver.Firefox(options=firefox_options)
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