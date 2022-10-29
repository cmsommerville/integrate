import requests
from requests.compat import urljoin

DATA_RATING_STRATEGY = [
    {
        "ref_attr_code": "rating", 
        "ref_attr_label": "Rated By", 
        "ref_attr_description": "Rating Strategy: RATED BY. This means that rates vary by the attribute to which this strategy is attached.", 
    },
    {
        "ref_attr_code": "uw", 
        "ref_attr_label": "Underwritten By", 
        "ref_attr_description": "Rating Strategy: UNDERWRITTEN BY. This means that rates do not vary by the attribute to which this strategy is attached. However, distribution assumptions are exposed for factor application.", 
    },
    {
        "ref_attr_code": "none", 
        "ref_attr_label": "None", 
        "ref_attr_description": "Rating Strategy: NONE. This means that neither rates or factors vary by this attribute.", 
    },
]


def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, 'api/crud/ref/rating-strategy-list')
    res = requests.post(url, json=DATA_RATING_STRATEGY)
    if not res.ok: 
        raise Exception(res.text)