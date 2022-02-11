import platform
import os.path
from sys import stderr
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


class Player:
    def __init__(self):
        self.initialize_driver()
        self.default_agree()

    def initialize_driver(self):
        ### select driver based on system ###
        os_name = platform.system()
        if os_name == "Linux":
            driver_path = os.path.join("drivers", "geckodriver")
            binary_path = os.path.abspath(
                os.path.join("drivers", "firefox", "firefox"))
        elif os_name == "Windows":
            driver_path = os.path.abspath(
                os.path.join("drivers", "geckodriver.exe"))
            binary_path = os.path.abspath(os.path.join(
                "drivers", "firefox_win32", "firefox.exe"))
        else:
            print(f"System `{os_name}` not suported", file=stderr)
            exit(1)

        print(f"OS_DETECTED: {os_name}")

        adblock_extension_path = os.path.join(
            "drivers", "adblocker_for_youtubetm-0.3.4-an+fx.xpi")

        ### setup driver ###
        ops = Options()
        ops.binary_location = binary_path
        profile = webdriver.FirefoxProfile()
        profile.set_preference("dom.media.autoplay.autoplay-policy-api", True)
        profile.set_preference("media.autoplay.default", 0)

        serv = Service(driver_path)
        self.browser = webdriver.Firefox(
            service=serv, options=ops, firefox_profile=profile)

        self.browser.install_addon(os.path.abspath(adblock_extension_path))

    def default_agree(self):
        self.browser.get("https://youtube.com")

        ### wait for "agree" popup to load ###
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, "dialog")))

        ### click agree button ###
        agree = self.browser.find_element(
            By.CSS_SELECTOR, 'tp-yt-paper-button[aria-label="Agree to the use of cookies and other data for the purposes described"]')
        agree.click()

    def play(self, url):
        self.browser.get(url)
