## pip install selenium
## pip install selenium-stealth
## sudo apt install chromium-chromedriver

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium_stealth import stealth

## init ##
service = Service(executable_path='/usr/bin/chromedriver')
options = webdriver.ChromeOptions()
options.add_argument('--headless') 
options.add_argument('--no-sandbox')
options.add_argument("--single-process")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")

## Define Function ##
def get_selenium(url) :
    browser = webdriver.Chrome(service=service, options=options)

    # Bypass Cloudflare Detection
    # https://stackoverflow.com/questions/68289474/selenium-headless-how-to-bypass-cloudflare-detection-using-selenium
    stealth(browser,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win64",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    browser.get(url) 

    result = browser.page_source

    browser.quit()

    return result
        