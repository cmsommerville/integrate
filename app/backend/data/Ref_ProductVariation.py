import requests
from flask_restx import fields

DATA_PRODUCT_VARIATION = [
    {
        "ref_attr_code": "issue_age", 
        "ref_attr_label": "Issue Age", 
        "ref_attr_description": "This is an issue age rated product variation.", 
    },
    {
        "ref_attr_code": "attained_age", 
        "ref_attr_label": "Attained Age", 
        "ref_attr_description": "This is an attained age rated product variation.", 
    },
]

def load() -> None:
    requests.post(fields.Url('CRUD_RefProductVariation_List'), DATA_PRODUCT_VARIATION)


if __name__ == '__main__':
    load()