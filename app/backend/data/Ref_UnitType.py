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

def load(hostname: str) -> None:
    url = urljoin(hostname, 'api/crud/ref/unit-code-list')
    res = requests.post(url, json=DATA_UNIT_TYPE)
    if not res.ok: 
        raise Exception(res.text)