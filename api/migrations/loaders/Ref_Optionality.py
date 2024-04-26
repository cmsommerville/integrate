import requests
import json
from requests.compat import urljoin

DATA_OPTIONALITY = [
    {
        "ref_attr_code": "required", 
        "ref_attr_label": "Required", 
        "ref_attr_description": "Required", 
    },
    {
        "ref_attr_code": "optional", 
        "ref_attr_label": "Optional", 
        "ref_attr_description": "Optional", 
    },
    {
        "ref_attr_code": "prohibited", 
        "ref_attr_label": "Prohibited", 
        "ref_attr_description": "Prohibited", 
    },
]


def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, 'api/ref/optionalities')
    res = requests.post(url, json=DATA_OPTIONALITY, **kwargs)
    if not res.ok: 
        raise Exception(res.text)