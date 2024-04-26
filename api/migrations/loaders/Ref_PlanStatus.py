import requests
from requests.compat import urljoin

DATA = [
    {
        "ref_attr_code": "in_progress",
        "ref_attr_label": "In Progress",
        "ref_attr_description": "In Progress",
    },
    {
        "ref_attr_code": "quoted",
        "ref_attr_label": "Quoted",
        "ref_attr_description": "Quoted",
    },
    {
        "ref_attr_code": "sold",
        "ref_attr_label": "Sold",
        "ref_attr_description": "Sold",
    },
    {
        "ref_attr_code": "declined",
        "ref_attr_label": "Declined",
        "ref_attr_description": "Declined",
    },
    {
        "ref_attr_code": "lost",
        "ref_attr_label": "Lost",
        "ref_attr_description": "Lost",
    },
]


def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, "api/ref/plan-statuses")
    res = requests.post(url, json=DATA, **kwargs)
    if not res.ok:
        raise Exception(res.text)
