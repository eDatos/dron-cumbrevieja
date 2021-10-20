import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def init_webdriver():
    options = Options()
    options.headless = False
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.dir", "downloads")
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip")
    return webdriver.Firefox(
        options=options, firefox_profile=profile, service_log_path=os.devnull
    )
