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
        webdriver.get(self.url)
        search_layers = WebDriverWait(webdriver, 10).until(
            EC.presence_of_element_located((By.ID, "search-results"))
        )
        return search_layers.find_elements_by_class_name("result-name")

    def get_unchecked_layers(self):
        for layer in self.layers:
            layer_url = layer.get_attribute('href')
            if layer_url not in storage.get_value(
                settings.CHECKED_RESULTS_API_KEY, default=''
            ):
                full_layer_url = urljoin(settings.ODLP_BASE_URL, layer_url)
                yield FeatureLayer(full_layer_url)


class FeatureLayer:
    def __init__(self, layer_url: str):
        self.layer_url = layer_url

    def get_shape_download_url(self):
        webdriver.get(self.layer_url)
