import requests
from requests.compat import urljoin
from itertools import product
from app.models import Model_ConfigProvision, Model_ConfigBenefit, Model_ConfigProduct


def PRODUCT(code: str):
    return Model_ConfigProduct.find_one_by_attr({"config_product_code": code})


def PROVISIONS(product_id: int):
    return Model_ConfigProvision.find_by_product(product_id)


def BENEFITS(product_id: int):
    return Model_ConfigBenefit.find_by_product(product_id)


def DATA_BENEFIT_PROVISIONS(product_id: int):
    data = []
    provs = PROVISIONS(product_id)
    bnfts = BENEFITS(product_id)
    for prov, bnft in product(provs, bnfts):
        data.append(
            {
                "config_benefit_id": bnft.config_benefit_id,
                "config_provision_id": prov.config_provision_id,
                "is_enabled": True,
            }
        )
    return data


def load(hostname: str, *args, **kwargs) -> None:
    product = PRODUCT("CI21000")
    provisions = PROVISIONS(product.config_product_id)
    benefits = BENEFITS(product.config_product_id)
    for provision in provisions:
        data = {"config_benefit_id": [b.config_benefit_id for b in benefits]}
        url = urljoin(
            hostname,
            f"api/config/provision/{provision.config_provision_id}/benefits",
        )
        res = requests.post(url, json=data, **kwargs)
        if not res.ok:
            raise Exception(res.text)
