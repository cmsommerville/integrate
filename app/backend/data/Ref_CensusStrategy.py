import requests
from flask_restx import fields

DATA_CENSUS_STRATEGY = [
    {
        "ref_attr_code": "required", 
        "ref_attr_label": "Required", 
        "ref_attr_description": "A census is required for rating", 
    },
    {
        "ref_attr_code": "optional", 
        "ref_attr_label": "Optional", 
        "ref_attr_description": "A census is optional for rating", 
    },
    {
        "ref_attr_code": "prohibited", 
        "ref_attr_label": "Prohibited", 
        "ref_attr_description": "A census is prohibited", 
    },
]

def load() -> None:
    requests.post(fields.Url('CRUD_RefCensusStrategy_List'), DATA_CENSUS_STRATEGY)


if __name__ == '__main__':
    load()