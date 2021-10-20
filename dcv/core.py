from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import settings
from dcv import utils


class Scraper:
    def __init__(self, url=settings.ODLP_BASE_URL):
        self.driver = utils.init_webdriver()
        self.url = url
        self.results = self.get_all_results()

    def get_all_results(self):
        self.driver.get(self.url)
        search_results = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "search-results"))
        )
        return search_results.find_elements_by_class_name("result-name")

    def __del__(self):
        self.driver.quit()
