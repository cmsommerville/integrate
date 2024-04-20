import requests
from requests.compat import urljoin

DATA_RATE_FREQUENCIES = [
    {
        "ref_attr_code": "12pp",
        "ref_attr_label": "Monthly",
        "ref_attr_description": "Monthly Rating Frequency",
        "ref_attr_value": 12,
    },
    {
        "ref_attr_code": "1pp",
        "ref_attr_label": "Annual",
        "ref_attr_description": "Annual Rating Frequency",
        "ref_attr_value": 1,
    },
]


def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, "api/ref/rate-frequencies")
    res = requests.post(url, json=DATA_RATE_FREQUENCIES, **kwargs)
    if not res.ok:
        raise Exception(res.text)
