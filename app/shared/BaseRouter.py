from flask_restx import Api, Resource, Namespace
from typing import List

    
def bind_namespaces(api: Api, namespaces: List[Namespace], prefix: str = None) -> None:
    """
    Binds a list of API routes to the API object
    """
    for ns in namespaces: 
        api.add_namespace(ns, path=prefix)

