import inspect
import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import settings


def init_webdriver(headless=settings.SELENIUM_HEADLESS):
    options = Options()
    options.headless = headless
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.dir", "downloads")
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip")
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
