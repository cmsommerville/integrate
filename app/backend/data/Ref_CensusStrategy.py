import requests
import json
from requests.compat import urljoin

DATA_CENSUS_STRATEGY = [
    {
        "ref_attr_code": "required", 
        "ref_attr_label": "Required", 
        "ref_attr_description": "A census is required for rating", 
    },
    {
        "ref_attr_code": "optional", 
        "ref_attr_label": "Optional", 
        "ref_attr_description": "A census is optional for rating", 
    },
    {
        "ref_attr_code": "prohibited", 
        "ref_attr_label": "Prohibited", 
        "ref_attr_description": "A census is prohibited", 
    },
]


def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, 'api/ref/census-strategies')
    res = requests.post(url, json=DATA_CENSUS_STRATEGY)
    if not res.ok: 
        raise Exception(res.text)