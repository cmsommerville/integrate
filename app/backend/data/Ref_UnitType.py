import requests
from requests.compat import urljoin

DATA_UNIT_TYPE = [
    {
        "ref_attr_code": "percent",
        "ref_attr_label": "Percentage",
        "ref_attr_symbol": "%",
        "ref_attr_description": "This is a percentage field. 25% is represented by the number 25.00",
    },
    {
        "ref_attr_code": "dollars",
        "ref_attr_label": "Dollars",
        "ref_attr_symbol": "$",
        "ref_attr_description": "This is a dollar amount field.",
    },
]


def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, "api/ref/unit-types")
    res = requests.post(url, json=DATA_UNIT_TYPE, **kwargs)
    if not res.ok:
        raise Exception(res.text)
