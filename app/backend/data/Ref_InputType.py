import requests
from requests.compat import urljoin

DATA_INPUT_TYPES = [
    {
        "ref_attr_code": "text", 
        "ref_attr_label": "Text Input", 
        "ref_attr_description": "This is a standard HTML text input field", 
    },
    {
        "ref_attr_code": "number", 
        "ref_attr_label": "Number Field", 
        "ref_attr_description": "This is a numeric input field", 
    },
    {
        "ref_attr_code": "date", 
        "ref_attr_label": "Date Field", 
        "ref_attr_description": "This is a date input field", 
    },
    {
        "ref_attr_code": "url", 
        "ref_attr_label": "URL", 
        "ref_attr_description": "This is a URL input field", 
    },
    {
        "ref_attr_code": "tel", 
        "ref_attr_label": "Telephone", 
        "ref_attr_description": "This is a telephone input field", 
    },
    {
        "ref_attr_code": "email", 
        "ref_attr_label": "Email", 
        "ref_attr_description": "This is a email input field", 
    },
    {
        "ref_attr_code": "password", 
        "ref_attr_label": "Password", 
        "ref_attr_description": "This is a password input field", 
    },
]


def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, 'api/crud/ref/input-type-list')
    res = requests.post(url, json=DATA_INPUT_TYPES)
    if not res.ok: 
        raise Exception(res.text)