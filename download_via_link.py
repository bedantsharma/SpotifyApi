from selenium import webdriver # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver import Keys, ActionChains # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
import time
import os

SPOTIFY_DOWN_URL = "https://spotifymate.com/en"
DRIVER_ADDRESS = '/Users/bedantsharma/Desktop/selenium/chromedriver.exe'
SONG_ADDRESS = 'https://open.spotify.com/track/6kooDsorCpWVMGc994XjWN'
DOWNLOAD_DIR = '/Users/bedantsharma/Downloads/'  # Update with your download directory

class DownloadSong:
    def __init__(self, id_number):
        self.id_number = id_number
        self.download_path = os.path.join(DOWNLOAD_DIR, f'{self.id_number}')
        os.makedirs(self.download_path, exist_ok=True)
        
        self.service = Service(DRIVER_ADDRESS)
        self.options = webdriver.ChromeOptions()
        self.prefs = {"download.default_directory": self.download_path}
        self.options.add_experimental_option("prefs", self.prefs)
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

    def wait_for_download_complete(self):
        while True:
            if any([file.endswith(".crdownload") for file in os.listdir(self.download_path)]):
                time.sleep(1)
            else:
                break

    def main(self, song_link):
        try:
            self.driver.get(SPOTIFY_DOWN_URL)

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'form-control')))

            input_element = self.driver.find_element(By.CLASS_NAME, 'form-control')
            input_element.clear()
            input_element.send_keys(song_link + Keys.ENTER)

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'abutton')))

            download_button = self.driver.find_element(By.CLASS_NAME, 'abutton')
            download_link = download_button.get_attribute('href')
            self.driver.get(download_link)
            print("Download started")

            # Wait for the download to start
            time.sleep(5)

            self.wait_for_download_complete()
            
            print("Download complete")
            
        finally:
            self.driver.quit()
            return 1
        
if __name__ == "__main__":
    downloader = DownloadSong("1234")  # Pass the id_number as an argument
    downloader.main(SONG_ADDRESS)
