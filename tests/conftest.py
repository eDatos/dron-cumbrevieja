import shutil

import pytest

import settings
from dcv import core

MAX_LAYERS_TO_PROCESS = 3


@pytest.fixture
def max_layers_to_process():
    return MAX_LAYERS_TO_PROCESS


@pytest.fixture
def downloads_dir(scope='module'):
    return settings.DOWNLOADS_DIR


@pytest.fixture
def layers_handler(scope='module'):
    yield core.LayersHandler(
        ignore_checked_layers=True, max_layers_to_process=MAX_LAYERS_TO_PROCESS
    )
    shutil.rmtree(settings.DOWNLOADS_DIR, ignore_errors=True)
