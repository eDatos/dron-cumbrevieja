import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL = (
    'https://www.opendatalapalma.es/search?collection=Dataset'
    '&q=perimetro%20dron&sort=-modified&type=feature%20layer'
)


def init_webdriver():
    options = Options()
    options.headless = False
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.dir', 'downloads')
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip')
    return webdriver.Firefox(
        options=options, firefox_profile=profile, service_log_path=os.devnull
    )


driver = init_webdriver()

driver.get(URL)
search_results = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'search-results'))
)

for result in search_results.find_elements_by_class_name('result-name'):
    print(result.text)
    print(result.get_attribute('href'))

driver.quit()
