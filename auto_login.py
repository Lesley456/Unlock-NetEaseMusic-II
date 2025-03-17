# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00A76D3BDCA0BFD9CBBC081FA5828EB783DE9138B31C44653536605FA54B3886489659A10A989CDFCF16F028E701D730E03C475121223E0366DB953C4D70EF56933380D1C42A1F46D95B48DF898D58529E3CD62EAF8B48C8BC398C0092CB398555909546093B1FCE85FF13637E624B624D4FC1BC2516636D13BBE9916D6F202B9043C218CDE1D790B60D531837D6D745F3DB7E9FE82D6042AE816FCA16040F3F2564075FCA57AE24E37CB82145C7CC4DF6C4DE8B92489211B59080516CE67CE7A2BF6FD30F11B300DAF0557D9334419A076B53122B433E8C6B0B953C4055C925D28511EA59F8A0A1F473AE75ADA6A1C2457A1F148D45B42E5824ABFBA94FE7883E7214AB905017472742150CFFF45C203DECFDC8ECC73496814F47691C9FB4C219402AC508B760556A60AAD0A8CC5F56FC979A6286522E364D71C31A5CD8A4D17AF5DEAEDC910A6C60632089B66A7BC2B2649F10BE2B8ACD35B785C1F40D8086E0"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
