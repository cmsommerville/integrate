import requests
from requests.compat import urljoin

DATA_PRODUCT_VARIATION = [
    {
        "ref_attr_code": "issue_age",
        "ref_attr_label": "Issue Age",
        "ref_attr_description": "This is an issue age rated product variation.",
    },
    {
        "ref_attr_code": "attained_age",
        "ref_attr_label": "Attained Age",
        "ref_attr_description": "This is an attained age rated product variation.",
    },
]


def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, "api/ref/product-variations")
    res = requests.post(url, json=DATA_PRODUCT_VARIATION, **kwargs)
    if not res.ok:
        raise Exception(res.text)
