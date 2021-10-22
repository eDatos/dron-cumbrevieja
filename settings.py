from pathlib import Path

from prettyconf import config

PROJECT_DIR = Path(__file__).resolve().parent
PROJECT_NAME = PROJECT_DIR.name

# Open Data La Palma
ODLP_BASE_URL = config(
    "ODLP_BASE_URL",
    default=(
        "https://www.opendatalapalma.es/search?collection=Dataset"
        "&q=perimetro%20dron&sort=-modified&type=feature%20layer"
    ),
)

KEYVALUE_API_URL = config('KEYVALUE_API_URL')
KEYVALUE_API_NAMESPACE = config('KEYVALUE_API_NAMESPACE', default=PROJECT_NAME)
CHECKED_RESULTS_API_KEY = config('CHECKED_RESULTS_API_KEY', default='checked-results')

SELENIUM_HEADLESS = config('SELENIUM_HEADLESS', default=True, cast=int)
