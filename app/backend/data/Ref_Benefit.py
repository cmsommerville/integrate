import requests
import json
from requests.compat import urljoin

DATA_BENEFIT = [
    {
        "ref_attr_code": "cancer",
        "ref_attr_label": "Internal Cancer",
        "ref_attr_description": "Internal Cancer",
    },
    {
        "ref_attr_code": "heart_attack",
        "ref_attr_label": "Heart Attack",
        "ref_attr_description": "Heart Attack",
    },
    {
        "ref_attr_code": "stroke",
        "ref_attr_label": "Stroke",
        "ref_attr_description": "Stroke",
    },
    {
        "ref_attr_code": "renal_failure",
        "ref_attr_label": "Renal Failure",
        "ref_attr_description": "Renal Failure",
    },
    {
        "ref_attr_code": "transplant",
        "ref_attr_label": "Major Organ Transplant",
        "ref_attr_description": "Major Organ Transplant",
    },
    {
        "ref_attr_code": "alzheimers",
        "ref_attr_label": "Advanced Alzheimer's",
        "ref_attr_description": "Advanced Alzheimer's",
    },
    {
        "ref_attr_code": "ms",
        "ref_attr_label": "Multiple Sclerosis",
        "ref_attr_description": "Multiple Sclerosis",
    },
    {
        "ref_attr_code": "als",
        "ref_attr_label": "Amytrophic Lateral Sclerosis (ALS)",
        "ref_attr_description": "Amytrophic Lateral Sclerosis (ALS)",
    },
    {
        "ref_attr_code": "cis",
        "ref_attr_label": "Carcinoma in Situ",
        "ref_attr_description": "Carcinoma in Situ",
    },
    {
        "ref_attr_code": "cabg",
        "ref_attr_label": "Coronary Artery Bypass Graft",
        "ref_attr_description": "Coronary Artery Bypass Graft",
    },
    {
        "ref_attr_code": "hsb",
        "ref_attr_label": "Health Screening Benefit",
        "ref_attr_description": "Health Screening Benefit",
    },
    {
        "ref_attr_code": "skin_cancer",
        "ref_attr_label": "Skin Cancer",
        "ref_attr_description": "Skin Cancer",
    },
]


def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, "api/ref/benefits")
    res = requests.post(url, json=DATA_BENEFIT, **kwargs)
    if not res.ok:
        raise Exception(res.text)
