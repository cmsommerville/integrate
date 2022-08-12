import requests
from requests.compat import urljoin

DATA_PROVISION = [
    {
        "ref_attr_code": "group_size", 
        "ref_attr_label": "Group Size", 
        "ref_attr_description": "Group Size", 
    },
    {
        "ref_attr_code": "sic_code", 
        "ref_attr_label": "SIC Code", 
        "ref_attr_description": "Standard Industrial Classification Code", 
    },
]


def load(hostname: str) -> None:
    url = urljoin(hostname, 'api/crud/ref/provision-list')
    res = requests.post(url, json=DATA_PROVISION)
    if not res.ok: 
        raise Exception(res.text)