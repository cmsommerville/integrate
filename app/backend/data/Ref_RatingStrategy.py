import requests
from flask_restx import fields

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

def load() -> None:
    requests.post(fields.Url('CRUD_RefRatingStrategy_List'), DATA_RATING_STRATEGY)


if __name__ == '__main__':
    load()