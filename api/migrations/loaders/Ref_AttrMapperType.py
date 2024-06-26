import requests
from requests.compat import urljoin
from app.backend.resources import CRUD_RefAttrMapperType_List

DATA_ATTR_MAPPER_TYPE = [
    {
        "ref_attr_code": "composite",
        "ref_attr_label": "Composite",
        "ref_attr_description": "This is a composite attribute mapper.",
    },
    {
        "ref_attr_code": "distinct",
        "ref_attr_label": "Distinct",
        "ref_attr_description": "This is a distinct attribute mapper. Typically, it maps an attribute to itself.",
    },
]


def load(hostname: str, *args, **kwargs) -> None:
    CRUD_RefAttrMapperType_List.bulk_create(DATA_ATTR_MAPPER_TYPE)
    # url = urljoin(hostname, "api/ref/attr-mapper-types")
    # res = requests.post(url, json=DATA_ATTR_MAPPER_TYPE, **kwargs)
    # if not res.ok:
    #     raise Exception(res.text)
