import requests
from requests.compat import urljoin
from itertools import product
from  ..models import Model_ConfigProvision, Model_ConfigBenefit

def PROVISIONS():
    return Model_ConfigProvision.find_all()

def BENEFITS():
    return Model_ConfigBenefit.find_all()


def DATA_BENEFIT_PROVISIONS():
    data = []
    for prov, bnft in product(PROVISIONS(), BENEFITS()):
        data.append({
            'config_benefit_id': bnft.config_benefit_id, 
            'config_provision_id': prov.config_provision_id, 
            'is_enabled': True
        })
    return data
    

def load(hostname: str) -> None:
    url = urljoin(hostname, 'api/crud/config/benefit-provision-list')
    res = requests.post(url, json=DATA_BENEFIT_PROVISIONS())
    if not res.ok: 
        raise Exception(res.text)