import requests
from requests.compat import urljoin

DATA = [
    {
        "config_dropdown_set_label": "SIC Codes",
        "is_numeric": False,
        "detail_display_strategy_code": "label_only",
        "sort_by_code": True,
        "dropdown_details": [
            {
                "config_dropdown_detail_code": "2011",
                "config_dropdown_detail_label": "Meat Packing Plants",
                "is_restricted": True,
                "acl": [
                    {"auth_role_code": "superuser"},
                    {"auth_role_code": "uw1000"},
                ],
            },
            {
                "config_dropdown_detail_code": "5411",
                "config_dropdown_detail_label": "Grocery Stores",
            },
            {
                "config_dropdown_detail_code": "8011",
                "config_dropdown_detail_label": "Offices & Clinics of Doctors of Medicine",
            },
            {
                "config_dropdown_detail_code": "8051",
                "config_dropdown_detail_label": "Skilled Nursing Care Facilities",
            },
            {
                "config_dropdown_detail_code": "8082",
                "config_dropdown_detail_label": "Home Health Care Services",
            },
        ],
    }
]


def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, "api/config/dropdown/sets")
    res = requests.post(url, json=DATA, **kwargs)
    if not res.ok:
        raise Exception(res.text)
