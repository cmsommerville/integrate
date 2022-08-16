import requests
from requests.compat import urljoin

DATA_DATA_TYPES = [
    {
        "ref_attr_code": "number", 
        "ref_attr_label": "Numeric Type", 
        "ref_attr_description": "This is a numeric field", 
    },
    {
        "ref_attr_code": "string", 
        "ref_attr_label": "String Type", 
        "ref_attr_description": "This is a string field", 
    },
    {
        "ref_attr_code": "boolean", 
        "ref_attr_label": "Boolean Type", 
        "ref_attr_description": "This is a boolean field", 
    },
]

def load(hostname: str) -> None:
    url = urljoin(hostname, 'api/crud/ref/data-type-list')
    res = requests.post(url, json=DATA_DATA_TYPES)
    if not res.ok: 
        raise Exception(res.text)