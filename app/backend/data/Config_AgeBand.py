import requests
from requests.compat import urljoin

DATA_AGE_BANDS = [
    {
        "config_age_band_set_label": "Standard 10 Year Age Bands", 
        "age_bands": [
            { 'age_band_lower': 18, 'age_band_upper': 29 },
            { 'age_band_lower': 30, 'age_band_upper': 39 },
            { 'age_band_lower': 40, 'age_band_upper': 49 },
            { 'age_band_lower': 50, 'age_band_upper': 59 },
            { 'age_band_lower': 60, 'age_band_upper': 99 },
        ]
    }, 
    {
        "config_age_band_set_label": "Standard 5 Year Age Bands", 
        "age_bands": [
            { 'age_band_lower': 18, 'age_band_upper': 24 },
            { 'age_band_lower': 25, 'age_band_upper': 29 },
            { 'age_band_lower': 30, 'age_band_upper': 34 },
            { 'age_band_lower': 35, 'age_band_upper': 39 },
            { 'age_band_lower': 40, 'age_band_upper': 44 },
            { 'age_band_lower': 45, 'age_band_upper': 49 },
            { 'age_band_lower': 50, 'age_band_upper': 54 },
            { 'age_band_lower': 55, 'age_band_upper': 59 },
            { 'age_band_lower': 60, 'age_band_upper': 64 },
            { 'age_band_lower': 65, 'age_band_upper': 69 },
        ]
    }, 
]


def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, 'api/crud/config/age-band-set-list')
    res = requests.post(url, json=DATA_AGE_BANDS, **kwargs)
    if not res.ok: 
        raise Exception(res.text)