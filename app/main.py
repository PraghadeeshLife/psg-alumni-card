from fastapi import FastAPI
from playwright.sync_api import sync_playwright

app = FastAPI()

@app.get("/scrape")
def scrape(url: str, selector: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # You can choose Firefox or WebKit
        page = browser.new_page()
        page.goto(url)
        try:
            # Scrape content using CSS selectors
            element = page.query_selector(selector)
            content = element.text_content() if element else None
            return {"content": content}
        except Exception as e:
            return {"error": str(e)}
        finally:
            browser.close()
