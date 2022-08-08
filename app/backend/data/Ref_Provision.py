import requests
from flask_restx import fields

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
]

def load() -> None:
    requests.post(fields.Url('CRUD_RefProvision_List'), DATA_PROVISION)


if __name__ == '__main__':
    load()