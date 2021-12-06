import hashlib
import json
import re
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import urljoin

from logzero import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import settings
from dcv import storage, utils

webdriver = utils.init_webdriver()


class LayersHandler:
    def __init__(
        self,
        url=settings.DRON_PERIMETER_LAYERS_URL,
        ignore_checked_layers=False,
        max_layers_to_process=settings.MAX_LAYERS_TO_PROCESS,
    ):
        logger.debug(f'BASE URL: {url}')
        self.url = url
        self.layers = self.get_all_layers()
        self.ignore_checked_layers = ignore_checked_layers
        self.max_layers_to_process = max_layers_to_process
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
        unchecked_layers = []
        for layer_path in self.layers:
            layer_url = urljoin(settings.ODLP_BASE_URL, layer_path)
            layer = FeatureLayer(layer_url)
            logger.debug(layer)
            if self.ignore_checked_layers or not layer.is_checked():
                logger.debug('└ Passing layer for processing')
                unchecked_layers.append(layer)
                if len(unchecked_layers) == self.max_layers_to_process:
                    break
            else:
                logger.debug('└ Layer is already checked. Omitting')
        return unchecked_layers


class FeatureLayer:
    def __init__(self, layer_url: str):
        self.layer_url = layer_url
        self.extract_layer_time()

    def extract_layer_time(self):
        logger.info('Extracting layer time')
        self.layer_time = settings.DEFAULT_LAYER_TIME
        webdriver.get(self.layer_url)
        summary = WebDriverWait(webdriver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'content-summary'))
        )
        description = summary.find_element_by_tag_name('p')
        if description:
            if m := re.search(r'a las *(\d+:\d+)', description.text):
                self.layer_time = m.group(1)

    def download_shapefile(self):
        logger.info(f'↓ Downloading shapefile for "{self.id}"')
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

        num_downloaded_files = utils.num_files_in_folder(settings.DOWNLOADS_DIR)

        # Manage shadow elements with javascript
        script = "return arguments[0].shadowRoot.querySelector('calcite-button')"
        shapefile_download_button = webdriver.execute_script(script, shape_download_card)
        logger.debug('Clicking download button for shapefile')
        shapefile_download_button.click()

        if num_downloaded_files == utils.num_files_in_folder(settings.DOWNLOADS_DIR):
            return None

        logger.debug('Getting downloaded file')
        self.layer_file = utils.rename_newest_file(
            settings.DOWNLOADS_DIR, self.id, keep_existing_suffix=True
        )
        return self.layer_file

    @property
    def hash(self):
        return hashlib.md5(self.layer_url.encode()).hexdigest()

    @property
    def id(self):
        clean_url = self.layer_url.rstrip('/').split('/')[-1].replace('-', '_')
        # drop layer time if exists
        clean_url = re.sub(r'_\d{4}$', '', clean_url)
        clean_time = self.layer_time.replace(':', '')
        return f'{clean_url}_{clean_time}'

    @staticmethod
    def get_checked_layers() -> list:
        return storage.get_value(
            settings.CHECKED_RESULTS_API_KEY, default=[], cast=json.loads
        )

    def mark_as_checked(self):
        logger.debug('Marking layer as checked')
        checked_layers = self.get_checked_layers()
        checked_layers.append(self.hash)
        storage.set_value(settings.CHECKED_RESULTS_API_KEY, json.dumps(checked_layers))

    def is_checked(self):
        checked_layers = self.get_checked_layers()
        return self.hash in checked_layers

    def notify(self):
        logger.info('Initializing notification handler')
        smtp = smtplib.SMTP(
            settings.SMTP_SERVER,
            port=settings.SMTP_PORT,
            timeout=settings.SMTP_CONNECTION_TIMEOUT,
        )
        smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)

        send_from = settings.NOTIFICATION_FROM_ADDR
        send_to = settings.NOTIFICATION_TO_ADDRS

        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = ','.join(send_to)
        msg['Subject'] = f'Actualización Dron - Cumbre Vieja [{self.id}]'

        logger.debug('Building content')
        buf = []
        buf.append('Nueva actualización Dron - Cumbre Vieja')
        buf.append('Open Data La Palma')
        buf.append(self.id)
        content = '<br>'.join(buf)
        msg.attach(MIMEText(content, 'html'))

        logger.debug('Adding attachment')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(self.layer_file.read_bytes())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition', f'attachment; filename={self.layer_file.name}'
        )
        msg.attach(part)

        logger.info('Sending message with attached files')
        smtp.sendmail(send_from, send_to, msg.as_string())

        smtp.quit()

    def __str__(self):
        return self.id
