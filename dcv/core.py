import hashlib
import json
from urllib.parse import urljoin

from logzero import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import settings
from dcv import storage, utils

webdriver = utils.init_webdriver()


class FeatureLayers:
    def __init__(self, url=settings.DRON_PERIMETER_LAYERS_URL, ignore_checked_layers=False):
        self.url = url
        self.layers = self.get_all_layers()
        self.ignore_checked_layers = ignore_checked_layers
        settings.DOWNLOADS_DIR.mkdir(exist_ok=True)

    def get_all_layers(self):
        '''Returns a list with urls for all layers'''
        logger.info('Getting all layers from website')
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
        logger.info('Getting unchecked layers')
        for layer_path in self.layers:
            layer_url = urljoin(settings.ODLP_BASE_URL, layer_path)
            layer = FeatureLayer(layer_url)
            if self.ignore_checked_layers or not layer.is_checked():
                logger.debug(f'Passing layer for processing: {layer_url}')
                yield layer


class FeatureLayer:
    def __init__(self, layer_url: str):
        self.layer_url = layer_url

    def download_shapefile(self):
        logger.info('Downloading shapefile')
        webdriver.get(self.layer_url)
        hub_toolbar = WebDriverWait(webdriver, 10).until(
            EC.presence_of_element_located((By.ID, 'hub-toolbar'))
        )
        # Download button is the second-one
        download_button = list(hub_toolbar.find_elements_by_tag_name('button'))[1]
        logger.debug('Opening download panel')
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
        logger.debug('Clicking download button for shapefile')
        shapefile_download_button.click()

        logger.debug(f'Assigning name {self.slug} to downloaded file')
        self.layer_file = utils.rename_newest_file(
            settings.DOWNLOADS_DIR, self.slug, keep_existing_suffix=True
        )

    @property
    def hash(self):
        return hashlib.md5(self.layer_url.encode()).hexdigest()

    @property
    def slug(self):
        return self.layer_url.rstrip('/').split('/')[-1]

    @staticmethod
    def get_checked_layers() -> list:
        return storage.get_value(
            settings.CHECKED_RESULTS_API_KEY, default=[], cast=json.loads
        )

    def mark_as_checked(self):
        logger.info('Marking layer as checked')
        checked_layers = self.get_checked_layers()
        checked_layers.append(self.hash)
        storage.set_value(settings.CHECKED_RESULTS_API_KEY, json.dumps(checked_layers))

    def is_checked(self):
        checked_layers = self.get_checked_layers()
        return self.hash in checked_layers
