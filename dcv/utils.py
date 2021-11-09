import inspect
import os
import shutil
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import settings


def init_webdriver(
    headless=settings.SELENIUM_HEADLESS, downloads_dir: Path = settings.DOWNLOADS_DIR
):
    options = Options()
    options.headless = headless
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.dir', str(downloads_dir))
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip')
    return webdriver.Firefox(
        options=options, firefox_profile=profile, service_log_path=os.devnull
    )


def qualify_key(func):
    def wrapper(*args, **kwargs):
        key = args[0]
        default_namespace = inspect.signature(func).parameters.get('namespace').default
        namespace = kwargs.get('namespace', default_namespace)
        qualified_key = f'{namespace}:{key}'
        args = list(args)
        args[0] = qualified_key
        return func(*args, **kwargs)

    return wrapper


def prepare_downloads_dir(downloads_dir=settings.DOWNLOADS_DIR):
    shutil.rmtree(settings.DOWNLOADS_DIR, ignore_errors=True)
    settings.DOWNLOADS_DIR.mkdir()
