import glob
import os
import re
from pathlib import Path

import logzero
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import settings


def init_logger():
    console_logformat = (
        '%(asctime)s '
        '%(color)s'
        '[%(levelname)-8s] '
        '%(end_color)s '
        '%(message)s '
        '%(color)s'
        '(%(filename)s:%(lineno)d)'
        '%(end_color)s'
    )
    # remove colors on logfile
    file_logformat = re.sub(r'%\((end_)?color\)s', '', console_logformat)

    console_formatter = logzero.LogFormatter(fmt=console_logformat)
    file_formatter = logzero.LogFormatter(fmt=file_logformat)
    logzero.setup_default_logger(formatter=console_formatter)
    logzero.logfile(
        settings.LOGFILE,
        maxBytes=settings.LOGFILE_SIZE,
        backupCount=settings.LOGFILE_BACKUP_COUNT,
        formatter=file_formatter,
    )
    return logzero.logger


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


def get_newest_file(target_folder: Path):
    '''Get the newest (last-modified) file in target_folder.'''
    if list_of_files := glob.glob(str(target_folder / '*')):
        newest_filename = max(list_of_files, key=os.path.getctime)
        return Path(newest_filename)


def rename_newest_file(
    target_folder: Path, replace_filename: str, *, keep_existing_suffix=False
) -> Path:
    '''Rename newest (last-modified) file in target_folder to replace_filename.
    If keep_existing_suffix is True, the suffix of the newest file remains.'''
    newest_file = get_newest_file(target_folder)

    if keep_existing_suffix:
        replace_filename += newest_file.suffix
    replace_file = target_folder / replace_filename

    return newest_file.rename(replace_file)


def num_files_in_folder(target_folder: Path):
    list_of_files = glob.glob(str(target_folder / '*'))
    return len(list_of_files)
