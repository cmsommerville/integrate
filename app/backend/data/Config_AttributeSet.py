import requests
from requests.compat import urljoin

DATA = [
    {
        "config_attr_set_code": "gender",
        "config_attr_set_label": "Standard Genders",
        "attributes": [
            {
                "config_attr_detail_code": "M",
                "config_attr_detail_label": "Male",
                "is_composite_id": False,
            },
            {
                "config_attr_detail_code": "F",
                "config_attr_detail_label": "Female",
                "is_composite_id": False,
            },
            {
                "config_attr_detail_code": "X",
                "config_attr_detail_label": "Composite",
                "is_composite_id": True,
            },
        ],
    },
    {
        "config_attr_set_code": "smoker_status",
        "config_attr_set_label": "Standard N/T/U",
        "attributes": [
            {
                "config_attr_detail_code": "N",
                "config_attr_detail_label": "Non-Tobacco",
                "is_composite_id": False,
            },
            {
                "config_attr_detail_code": "T",
                "config_attr_detail_label": "Tobacco",
                "is_composite_id": False,
            },
            {
                "config_attr_detail_code": "U",
                "config_attr_detail_label": "Composite",
                "is_composite_id": True,
            },
        ],
    },
    {
        "config_attr_set_code": "relationship",
        "config_attr_set_label": "Standard EE/SP/CH",
        "attributes": [
            {
                "config_attr_detail_code": "EE",
                "config_attr_detail_label": "Employee",
                "is_composite_id": False,
            },
            {
                "config_attr_detail_code": "SP",
                "config_attr_detail_label": "Spouse",
                "is_composite_id": False,
            },
            {
                "config_attr_detail_code": "CH",
                "config_attr_detail_label": "Children",
                "is_composite_id": False,
            },
        ],
    },
]


def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, "api/config/attribute/sets")
    res = requests.post(url, json=DATA, **kwargs)
    if not res.ok:
        raise Exception(res.text)
