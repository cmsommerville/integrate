import requests
from requests.compat import urljoin

DATA_AGE_DISTRIBUTION = [
    {
        "config_age_distribution_set_label": "Normal(45,15) Age Distribution",
        "age_distribution": [
            {"age_value": 18, "rate_table_age_value": 22, "weight": 49.6},
            {"age_value": 19, "rate_table_age_value": 22, "weight": 55.9},
            {"age_value": 20, "rate_table_age_value": 22, "weight": 62.7},
            {"age_value": 21, "rate_table_age_value": 22, "weight": 70.1},
            {"age_value": 22, "rate_table_age_value": 22, "weight": 78.0},
            {"age_value": 23, "rate_table_age_value": 22, "weight": 86.4},
            {"age_value": 24, "rate_table_age_value": 22, "weight": 95.2},
            {"age_value": 25, "rate_table_age_value": 27, "weight": 104.5},
            {"age_value": 26, "rate_table_age_value": 27, "weight": 114.3},
            {"age_value": 27, "rate_table_age_value": 27, "weight": 124.3},
            {"age_value": 28, "rate_table_age_value": 27, "weight": 134.7},
            {"age_value": 29, "rate_table_age_value": 27, "weight": 145.2},
            {"age_value": 30, "rate_table_age_value": 32, "weight": 155.9},
            {"age_value": 31, "rate_table_age_value": 32, "weight": 166.7},
            {"age_value": 32, "rate_table_age_value": 32, "weight": 177.4},
            {"age_value": 33, "rate_table_age_value": 32, "weight": 187.9},
            {"age_value": 34, "rate_table_age_value": 32, "weight": 198.2},
            {"age_value": 35, "rate_table_age_value": 37, "weight": 208.1},
            {"age_value": 36, "rate_table_age_value": 37, "weight": 217.6},
            {"age_value": 37, "rate_table_age_value": 37, "weight": 226.5},
            {"age_value": 38, "rate_table_age_value": 37, "weight": 234.7},
            {"age_value": 39, "rate_table_age_value": 37, "weight": 242.1},
            {"age_value": 40, "rate_table_age_value": 42, "weight": 248.6},
            {"age_value": 41, "rate_table_age_value": 42, "weight": 254.2},
            {"age_value": 42, "rate_table_age_value": 42, "weight": 258.8},
            {"age_value": 43, "rate_table_age_value": 42, "weight": 262.2},
            {"age_value": 44, "rate_table_age_value": 42, "weight": 264.6},
            {"age_value": 45, "rate_table_age_value": 47, "weight": 265.8},
            {"age_value": 46, "rate_table_age_value": 47, "weight": 265.8},
            {"age_value": 47, "rate_table_age_value": 47, "weight": 264.6},
            {"age_value": 48, "rate_table_age_value": 47, "weight": 262.2},
            {"age_value": 49, "rate_table_age_value": 47, "weight": 258.8},
            {"age_value": 50, "rate_table_age_value": 52, "weight": 254.2},
            {"age_value": 51, "rate_table_age_value": 52, "weight": 248.6},
            {"age_value": 52, "rate_table_age_value": 52, "weight": 242.1},
            {"age_value": 53, "rate_table_age_value": 52, "weight": 234.7},
            {"age_value": 54, "rate_table_age_value": 52, "weight": 226.5},
            {"age_value": 55, "rate_table_age_value": 57, "weight": 217.6},
            {"age_value": 56, "rate_table_age_value": 57, "weight": 208.1},
            {"age_value": 57, "rate_table_age_value": 57, "weight": 198.2},
            {"age_value": 58, "rate_table_age_value": 57, "weight": 187.9},
            {"age_value": 59, "rate_table_age_value": 57, "weight": 177.4},
            {"age_value": 60, "rate_table_age_value": 62, "weight": 166.7},
            {"age_value": 61, "rate_table_age_value": 62, "weight": 155.9},
            {"age_value": 62, "rate_table_age_value": 62, "weight": 145.2},
            {"age_value": 63, "rate_table_age_value": 62, "weight": 134.7},
            {"age_value": 64, "rate_table_age_value": 62, "weight": 124.3},
            {"age_value": 65, "rate_table_age_value": 67, "weight": 114.3},
            {"age_value": 66, "rate_table_age_value": 67, "weight": 104.5},
            {"age_value": 67, "rate_table_age_value": 67, "weight": 95.2},
            {"age_value": 68, "rate_table_age_value": 67, "weight": 86.4},
            {"age_value": 69, "rate_table_age_value": 67, "weight": 78.0},
            {"age_value": 70, "rate_table_age_value": 67, "weight": 70.1},
            {"age_value": 71, "rate_table_age_value": 67, "weight": 62.7},
            {"age_value": 72, "rate_table_age_value": 67, "weight": 55.9},
            {"age_value": 73, "rate_table_age_value": 67, "weight": 49.6},
            {"age_value": 74, "rate_table_age_value": 67, "weight": 43.8},
            {"age_value": 75, "rate_table_age_value": 67, "weight": 38.5},
            {"age_value": 76, "rate_table_age_value": 67, "weight": 33.7},
            {"age_value": 77, "rate_table_age_value": 67, "weight": 29.3},
            {"age_value": 78, "rate_table_age_value": 67, "weight": 25.5},
            {"age_value": 79, "rate_table_age_value": 67, "weight": 22.0},
        ],
    },
]


def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, "api/config/age-dist-sets")
    res = requests.post(url, json=DATA_AGE_DISTRIBUTION, **kwargs)
    if not res.ok:
        raise Exception(res.text)
