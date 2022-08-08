import requests
from flask_restx import fields

DATA_DATA_TYPES = [
    {
        "ref_attr_code": "number", 
        "ref_attr_label": "Numeric Type", 
        "ref_attr_description": "This is a numeric field", 
    },
    {
        "ref_attr_code": "string", 
        "ref_attr_label": "String Type", 
        "ref_attr_description": "This is a string field", 
    },
    {
        "ref_attr_code": "boolean", 
        "ref_attr_label": "Boolean Type", 
        "ref_attr_description": "This is a boolean field", 
    },
]

float, str, int, 

def load() -> None:
    requests.post(fields.Url('CRUD_RefDataTypes_List'), DATA_DATA_TYPES)


if __name__ == '__main__':
    load()