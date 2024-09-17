from fastapi import FastAPI
from pydantic import BaseModel
from playwright.sync_api import sync_playwright

app = FastAPI()

class URLPayload(BaseModel):
    url: str

@app.get("/scrape")
def scrape(payload: URLPayload):
    with sync_playwright() as p:
        url = payload.url
        # url = 'https://alumni.psgitech.ac.in/icard/verify?id=1323433&name=96d669e0dbb9ab6b19b56d3f9fb74e7a'
        browser = p.chromium.launch(headless=True)  # You can choose Firefox or WebKit
        page = browser.new_page()
        page.goto(url)
        try:
            # Scrape content using CSS selectors
            xpath_1 = '/html/body/div[1]/div/div[2]/ui-view/div/div/div/div[1]/div[3]'
            xpath_2 = '/html/body/div[1]/div/div[2]/ui-view/div/div/div/div[1]/div[5]/div[4]/span'
            xpath_3 = '/html/body/div[1]/div/div[2]/ui-view/div/div/div/div[1]/div[5]/div[5]/span'
            # Find the element using XPath and extract its text content
            name_play = page.locator(f'xpath={xpath_1}')
            name = name_play.text_content()
            print(name)
            dept_play = page.locator(f'xpath={xpath_2}')
            dept = dept_play.text_content()
            print(dept)
            enroll_play = page.locator(f'xpath={xpath_3}')
            enroll = enroll_play.text_content()
            print(enroll)
            return {"name": name, "dept": dept, "enroll": enroll}
        except Exception as e:
            return {"error": str(e)}
        finally:
            browser.close()
