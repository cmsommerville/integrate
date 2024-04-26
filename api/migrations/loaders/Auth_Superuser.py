import os
import requests
from requests.compat import urljoin

SYS_USER_NAME = "sys"


def login(hostname, **kwargs):
    PWD = os.getenv("SYS_SUPERUSER_PWD")
    if PWD is None:
        raise ValueError("SYS_SUPERUSER_PWD environment variable is not set")
    url = urljoin(hostname, "api/auth/user/login")
    res = requests.post(
        url, json={"user_name": SYS_USER_NAME, "password": PWD}, **kwargs
    )
    if not res.ok:
        raise Exception(res.text)
    return res
