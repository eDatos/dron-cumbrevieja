from pathlib import Path
from urllib.parse import urljoin

from prettyconf import config

PROJECT_DIR = Path(__file__).resolve().parent
PROJECT_NAME = PROJECT_DIR.name

# Open Data La Palma
ODLP_BASE_URL = config('ODLP_BASE_URL', default='https://www.opendatalapalma.es/')
DRON_PERIMETER_LAYERS_REL_URL = config(
    'DRON_PERIMETER_LAYERS_REL_URL',
    default='/search?collection=Dataset'
    '&q=perimetro%20dron&sort=-modified&type=feature%20layer',
)
DRON_PERIMETER_LAYERS_URL = urljoin(ODLP_BASE_URL, DRON_PERIMETER_LAYERS_REL_URL)

KEYVALUE_API_URL = config('KEYVALUE_API_URL')
KEYVALUE_API_NAMESPACE = config('KEYVALUE_API_NAMESPACE', default=PROJECT_NAME)
CHECKED_RESULTS_API_KEY = config('CHECKED_RESULTS_API_KEY', default='checked-results')

SELENIUM_HEADLESS = config('SELENIUM_HEADLESS', default=True, cast=lambda v: bool(int(v)))

DOWNLOADS_DIR = config('DOWNLOADS_DIR', default=PROJECT_DIR / 'downloads', cast=Path)

LOGFILE = config('LOGFILE', default=PROJECT_DIR / (PROJECT_NAME + '.log'), cast=Path)
LOGFILE_SIZE = config('LOGFILE_SIZE', cast=float, default=1e6)
LOGFILE_BACKUP_COUNT = config('LOGFILE_BACKUP_COUNT', cast=int, default=3)
