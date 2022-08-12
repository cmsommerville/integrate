import requests
from requests.compat import urljoin

DATA_ATTR_MAPPER_TYPE = [
    {
        "ref_attr_code": "composite", 
        "ref_attr_label": "Composite", 
        "ref_attr_description": "This is a composite attribute mapper.", 
    },
    {
        "ref_attr_code": "distinct", 
        "ref_attr_label": "Distinct", 
        "ref_attr_description": "This is a distinct attribute mapper. Typically, it maps an attribute to itself.", 
    },
]

def load(hostname: str) -> None:
    url = urljoin(hostname, 'api/crud/ref/attr-mapper-type-list')
    res = requests.post(url, json=DATA_ATTR_MAPPER_TYPE)
    if not res.ok: 
        raise Exception(res.text)