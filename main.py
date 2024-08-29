from selenium import webdriver # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
import time
import os

SPOTIFY_DOWN_URL = "https://spotifymate.com/en"
DRIVER_ADDRESS = '/Users/bedantsharma/Desktop/selenium/chromedriver.exe'
SONG_ADDRESS = 'https://open.spotify.com/track/7e89621JPkKaeDSTQ3avtg'
DOWNLOAD_DIR = '/Users/bedantsharma/Downloads'  # Update with your download directory

service = Service(DRIVER_ADDRESS)
options = webdriver.ChromeOptions()
prefs = {"download.default_directory": DOWNLOAD_DIR}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(service=service, options=options)

def wait_for_download_complete(download_dir):
    while True:
        if any([file.endswith(".crdownload") for file in os.listdir(download_dir)]):
            time.sleep(1)
        else:
            break

try:
    driver.get(SPOTIFY_DOWN_URL)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'form-control')))

    input_element = driver.find_element(By.CLASS_NAME, 'form-control')
    input_element.clear()
    input_element.send_keys(SONG_ADDRESS + Keys.ENTER)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'abutton')))

    download_button = driver.find_element(By.CLASS_NAME, 'abutton')
    download_button.click()
    print("Download started")

    wait_for_download_complete(DOWNLOAD_DIR)
    print("Download complete")
finally:
    driver.quit()
