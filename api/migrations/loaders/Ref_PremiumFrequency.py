import requests
from requests.compat import urljoin

DATA_PREMIUM_FREQUENCIES = [
    {
        "ref_attr_code": "12pp",
        "ref_attr_label": "Monthly",
        "ref_attr_description": "Monthly deductions",
        "ref_attr_value": 12,
    },
    {
        "ref_attr_code": "24pp",
        "ref_attr_label": "Semi-Monthly",
        "ref_attr_description": "Semi-monthly deductions",
        "ref_attr_value": 24,
    },
    {
        "ref_attr_code": "26pp",
        "ref_attr_label": "Biweekly",
        "ref_attr_description": "Biweekly deductions",
        "ref_attr_value": 26,
    },
    {
        "ref_attr_code": "52pp",
        "ref_attr_label": "Weekly",
        "ref_attr_description": "Weekly deductions",
        "ref_attr_value": 52,
    },
]


def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, "api/ref/premium-frequencies")
    res = requests.post(url, json=DATA_PREMIUM_FREQUENCIES, **kwargs)
    if not res.ok:
        raise Exception(res.text)
