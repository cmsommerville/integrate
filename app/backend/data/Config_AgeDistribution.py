import requests
from requests.compat import urljoin

DATA_AGE_DISTRIBUTION = [
    {
        "config_age_distribution_set_label": "Normal(45,15) Age Distribution", 
        "age_distribution": [
            { 'age_value': 18, 'weight': 49.6 },
            { 'age_value': 19, 'weight': 55.9 },
            { 'age_value': 20, 'weight': 62.7 },
            { 'age_value': 21, 'weight': 70.1 },
            { 'age_value': 22, 'weight': 78.0 },
            { 'age_value': 23, 'weight': 86.4 },
            { 'age_value': 24, 'weight': 95.2 },
            { 'age_value': 25, 'weight': 104.5 },
            { 'age_value': 26, 'weight': 114.3 },
            { 'age_value': 27, 'weight': 124.3 },
            { 'age_value': 28, 'weight': 134.7 },
            { 'age_value': 29, 'weight': 145.2 },
            { 'age_value': 30, 'weight': 155.9 },
            { 'age_value': 31, 'weight': 166.7 },
            { 'age_value': 32, 'weight': 177.4 },
            { 'age_value': 33, 'weight': 187.9 },
            { 'age_value': 34, 'weight': 198.2 },
            { 'age_value': 35, 'weight': 208.1 },
            { 'age_value': 36, 'weight': 217.6 },
            { 'age_value': 37, 'weight': 226.5 },
            { 'age_value': 38, 'weight': 234.7 },
            { 'age_value': 39, 'weight': 242.1 },
            { 'age_value': 40, 'weight': 248.6 },
            { 'age_value': 41, 'weight': 254.2 },
            { 'age_value': 42, 'weight': 258.8 },
            { 'age_value': 43, 'weight': 262.2 },
            { 'age_value': 44, 'weight': 264.6 },
            { 'age_value': 45, 'weight': 265.8 },
            { 'age_value': 46, 'weight': 265.8 },
            { 'age_value': 47, 'weight': 264.6 },
            { 'age_value': 48, 'weight': 262.2 },
            { 'age_value': 49, 'weight': 258.8 },
            { 'age_value': 50, 'weight': 254.2 },
            { 'age_value': 51, 'weight': 248.6 },
            { 'age_value': 52, 'weight': 242.1 },
            { 'age_value': 53, 'weight': 234.7 },
            { 'age_value': 54, 'weight': 226.5 },
            { 'age_value': 55, 'weight': 217.6 },
            { 'age_value': 56, 'weight': 208.1 },
            { 'age_value': 57, 'weight': 198.2 },
            { 'age_value': 58, 'weight': 187.9 },
            { 'age_value': 59, 'weight': 177.4 },
            { 'age_value': 60, 'weight': 166.7 },
            { 'age_value': 61, 'weight': 155.9 },
            { 'age_value': 62, 'weight': 145.2 },
            { 'age_value': 63, 'weight': 134.7 },
            { 'age_value': 64, 'weight': 124.3 },
            { 'age_value': 65, 'weight': 114.3 },
            { 'age_value': 66, 'weight': 104.5 },
            { 'age_value': 67, 'weight': 95.2 },
            { 'age_value': 68, 'weight': 86.4 },
            { 'age_value': 69, 'weight': 78.0 },
            { 'age_value': 70, 'weight': 70.1 },
            { 'age_value': 71, 'weight': 62.7 },
            { 'age_value': 72, 'weight': 55.9 },
            { 'age_value': 73, 'weight': 49.6 },
            { 'age_value': 74, 'weight': 43.8 },
            { 'age_value': 75, 'weight': 38.5 },
            { 'age_value': 76, 'weight': 33.7 },
            { 'age_value': 77, 'weight': 29.3 },
            { 'age_value': 78, 'weight': 25.5 },
            { 'age_value': 79, 'weight': 22.0 },
        ]
    }, 
]

def load(hostname: str) -> None:
    url = urljoin(hostname, 'api/crud/config/age-distribution-set-list')
    res = requests.post(url, json=DATA_AGE_DISTRIBUTION)
    if not res.ok: 
        raise Exception(res.text)