from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import settings
from dcv import storage, utils

webdriver = utils.init_webdriver()


class FeatureLayers:
    def __init__(self, url=settings.DRON_PERIMETER_LAYERS_URL):
        self.url = url
        self.layers = self.get_all_layers()

    def get_all_layers(self):
        '''Returns a list with urls for all layers'''
        webdriver.get(self.url)
        search_layers = WebDriverWait(webdriver, 10).until(
            EC.presence_of_element_located((By.ID, 'search-results'))
        )
        return [
            e.get_attribute('href')
            for e in search_layers.find_elements_by_class_name('result-name')
        ]

    def get_unchecked_layers(self):
        '''Generator with urls for unchecked layers'''
        for layer_url in self.layers:
            if layer_url not in storage.get_value(
                settings.CHECKED_RESULTS_API_KEY, default=''
            ):
                full_layer_url = urljoin(settings.ODLP_BASE_URL, layer_url)
                yield FeatureLayer(full_layer_url)


class FeatureLayer:
    def __init__(self, layer_url: str):
        self.layer_url = layer_url

    def download_shapefile(self):
        webdriver.get(self.layer_url)
        hub_toolbar = WebDriverWait(webdriver, 10).until(
            EC.presence_of_element_located((By.ID, 'hub-toolbar'))
        )
        # Download button is the second-one
        download_button = list(hub_toolbar.find_elements_by_tag_name('button'))[1]
        download_button.click()

        WebDriverWait(webdriver, 10).until(
            EC.element_to_be_clickable((By.TAG_NAME, 'hub-download-card'))
        )

        # Shapefile is in the third block
        shape_download_card = list(
            webdriver.find_elements_by_tag_name('hub-download-card')
        )[2]

        # Manage shadow elements with javascript
        script = "return arguments[0].shadowRoot.querySelector('calcite-button')"
        shapefile_download_button = webdriver.execute_script(script, shape_download_card)
        shapefile_download_button.click()
