import requests
from flask_restx import fields

DATA_INPUT_TYPES = [
    {
        "ref_attr_code": "text", 
        "ref_attr_label": "Text Input", 
        "ref_attr_description": "This is a standard HTML text input field", 
    },
    {
        "ref_attr_code": "number", 
        "ref_attr_label": "Number Field", 
        "ref_attr_description": "This is a numeric input field", 
    },
    {
        "ref_attr_code": "date", 
        "ref_attr_label": "Date Field", 
        "ref_attr_description": "This is a date input field", 
    },
    {
        "ref_attr_code": "url", 
        "ref_attr_label": "URL", 
        "ref_attr_description": "This is a URL input field", 
    },
    {
        "ref_attr_code": "tel", 
        "ref_attr_label": "Telephone", 
        "ref_attr_description": "This is a telephone input field", 
    },
    {
        "ref_attr_code": "email", 
        "ref_attr_label": "Email", 
        "ref_attr_description": "This is a email input field", 
    },
    {
        "ref_attr_code": "password", 
        "ref_attr_label": "Password", 
        "ref_attr_description": "This is a password input field", 
    },
]

def load() -> None:
    requests.post(fields.Url('CRUD_RefInputTypes_List'), DATA_INPUT_TYPES)


if __name__ == '__main__':
    load()