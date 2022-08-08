import requests
from flask_restx import fields

DATA_UNIT_TYPE = [
    {
        "ref_attr_code": "percent", 
        "ref_attr_label": "Percentage", 
        "ref_attr_symbol": "%", 
        "ref_attr_description": "This is a percentage field. 25% is represented by the number 25.00", 
    },
    {
        "ref_attr_code": "dollars", 
        "ref_attr_label": "Dollars", 
        "ref_attr_symbol": "$", 
        "ref_attr_description": "This is a dollar amount field.", 
    },
]

def load() -> None:
    requests.post(fields.Url('CRUD_RefUnitType_List'), DATA_UNIT_TYPE)


if __name__ == '__main__':
    load()