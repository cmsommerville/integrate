import requests
from requests.compat import urljoin
from app.backend.models import Model_ConfigProduct, Model_ConfigProvision


PROVISION_CODES = ["group_size", "sic_code", "reduction_at_70"]


def PRODUCT(product_code: str):
    return Model_ConfigProduct.find_one_by_attr({"config_product_code": product_code})


def PROVISION(provision_code: str):
    return Model_ConfigProvision.find_one_by_attr(
        {"config_provision_code": provision_code}
    )


def PROVISION_STATES(product: Model_ConfigProduct):
    return {code: [state for state in product.states] for code in PROVISION_CODES}


def DATA_PROVISION_STATES(
    product: Model_ConfigProduct, provision: Model_ConfigProvision
):
    provision_states = PROVISION_STATES(product)[provision.config_provision_code]
    return [
        {
            "config_provision_id": provision.config_provision_id,
            "state_id": state.state_id,
            "config_provision_state_effective_date": str(
                product.config_product_effective_date
            ),
            "config_provision_state_expiration_date": str(
                product.config_product_expiration_date
            ),
        }
        for state in provision_states
    ]


def load(hostname: str, *args, **kwargs) -> None:
    product = PRODUCT("CI21000")
    for prov_code in PROVISION_CODES:
        provision = PROVISION(prov_code)
        url = urljoin(
            hostname,
            f"api/config/provision/{provision.config_provision_id}/states",
        )
        res = requests.post(
            url, json=DATA_PROVISION_STATES(product, provision), **kwargs
        )
        if not res.ok:
            raise Exception(res.text)
