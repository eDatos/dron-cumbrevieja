from urllib.parse import urljoin

import requests

import settings
from dcv.utils import qualify_key


@qualify_key
def set_value(key, value, /, *, namespace=settings.KEYVALUE_API_NAMESPACE):
    path = f'/set/{key}?value={value}'
    url = urljoin(settings.KEYVALUE_API_URL, path)
    response = requests.get(url)
    data = response.json()
    return data['data'][key]['value']


@qualify_key
def get_value(key, /, *, default=None, cast=str, namespace=settings.KEYVALUE_API_NAMESPACE):
    path = f'/get/{key}'
    url = urljoin(settings.KEYVALUE_API_URL, path)
    response = requests.get(url)
    data = response.json()
    return cast(data['value']) if data else default
