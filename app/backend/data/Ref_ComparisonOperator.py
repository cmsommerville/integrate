import requests
from flask_restx import fields

DATA_COMPARISON_OPERATOR = [
    {
        "ref_attr_code": "__eq__", 
        "ref_attr_label": "Equals", 
        "ref_attr_description": "Equality operator", 
        "ref_attr_symbol": "="
    },
    {
        "ref_attr_code": "__ne__", 
        "ref_attr_label": "Not equal", 
        "ref_attr_description": "Does not equal operator", 
        "ref_attr_symbol": "!="
    },
    {
        "ref_attr_code": "__gt__", 
        "ref_attr_label": "Greater than", 
        "ref_attr_description": "Greater than operator", 
        "ref_attr_symbol": ">"
    },
    {
        "ref_attr_code": "__ge__", 
        "ref_attr_label": "Greater than or equal", 
        "ref_attr_description": "Greater than or equal operator", 
        "ref_attr_symbol": ">="
    },
    {
        "ref_attr_code": "__lt__", 
        "ref_attr_label": "Less than", 
        "ref_attr_description": "Less than operator", 
        "ref_attr_symbol": "<"
    },
    {
        "ref_attr_code": "__le__", 
        "ref_attr_label": "Less than or equal", 
        "ref_attr_description": "Less than or equal operator", 
        "ref_attr_symbol": "<="
    },
]

def load() -> None:
    requests.post(fields.Url('CRUD_RefComparisonOperator_List'), DATA_COMPARISON_OPERATOR)


if __name__ == '__main__':
    load()