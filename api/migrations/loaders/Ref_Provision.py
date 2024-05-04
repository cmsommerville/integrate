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
    {
        "ref_attr_code": "reduction_at_70",
        "ref_attr_label": "Reduction at Age 70",
        "ref_attr_description": "50% Benefit Reduction at Attained Age 70",
    },
]


def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, "api/ref/provisions")
    res = requests.post(url, json=DATA_PROVISION, **kwargs)
    if not res.ok:
        raise Exception(res.text)
