import shutil

import pytest

import settings
from dcv import core

MAX_LAYERS_TO_PROCESS = 3


@pytest.fixture(scope='module', autouse=True)
def cleanup():
    yield
    shutil.rmtree(settings.DOWNLOADS_DIR, ignore_errors=True)


@pytest.fixture
def max_layers_to_process():
    return MAX_LAYERS_TO_PROCESS


@pytest.fixture(scope='module')
def downloads_dir():
    return settings.DOWNLOADS_DIR


@pytest.fixture(scope='module')
def layers_handler():
    return core.LayersHandler(
        ignore_checked_layers=True, max_layers_to_process=MAX_LAYERS_TO_PROCESS
    )


@pytest.fixture(scope='module')
def feature_layer():
    return core.FeatureLayer(
        'https://www.opendatalapalma.es/datasets/perimetro-dron-211108-1300/'
    )
