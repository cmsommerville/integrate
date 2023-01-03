from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigProvision_Product, Model_ConfigProvision_RateTable
from ..schemas import Schema_ConfigProvision_Product, Schema_ConfigProvision_RateTable

class CRUD_ConfigProvision_Product(BaseCRUDResource): 
    model = Model_ConfigProvision_Product
    schema = Schema_ConfigProvision_Product()

class CRUD_ConfigProvision_Product_List(BaseCRUDResourceList): 
    model = Model_ConfigProvision_Product
    schema = Schema_ConfigProvision_Product(many=True)

class CRUD_ConfigProvision_RateTable(BaseCRUDResource): 
    model = Model_ConfigProvision_RateTable
    schema = Schema_ConfigProvision_RateTable()

class CRUD_ConfigProvision_RateTable_List(BaseCRUDResourceList): 
    model = Model_ConfigProvision_RateTable
    schema = Schema_ConfigProvision_RateTable(many=True)



DISCRIMINATOR = {
    'prd': CRUD_ConfigProvision_Product, 
    'rt': CRUD_ConfigProvision_RateTable, 
}

LIST_DISCRIMINATOR = {
    'prd': CRUD_ConfigProvision_Product_List, 
    'rt': CRUD_ConfigProvision_RateTable_List, 
}

class CRUD_ConfigProvision(BaseCRUDResource):

    @classmethod
    def get(cls, provision_type: str, *args, **kwargs): 
        resource = DISCRIMINATOR.get(provision_type)
        if resource is None: 
            try: 
                return {"status": "error", "message": f"Cannot find resource with provision_type: `${provision_type}`"}, 404
            except Exception as e: 
                return {"status": "error", "message": str(e)}, 500
        return resource.get(**kwargs)

    @classmethod
    def post(cls, provision_type: str, *args, **kwargs): 
        resource = DISCRIMINATOR.get(provision_type)
        if resource is None: 
            try: 
                return {"status": "error", "message": f"Cannot find resource with provision_type: `${provision_type}`"}, 404
            except Exception as e: 
                return {"status": "error", "message": str(e)}, 500
        return resource.post(**kwargs)

    @classmethod
    def patch(cls, provision_type: str, *args, **kwargs): 
        resource = DISCRIMINATOR.get(provision_type)
        if resource is None: 
            try: 
                return {"status": "error", "message": f"Cannot find resource with provision_type: `${provision_type}`"}, 404
            except Exception as e: 
                return {"status": "error", "message": str(e)}, 500
        return resource.patch(**kwargs)

    @classmethod
    def put(cls, provision_type: str, *args, **kwargs): 
        resource = DISCRIMINATOR.get(provision_type)
        if resource is None: 
            try: 
                return {"status": "error", "message": f"Cannot find resource with provision_type: `${provision_type}`"}, 404
            except Exception as e: 
                return {"status": "error", "message": str(e)}, 500
        return resource.put(**kwargs)

    @classmethod
    def delete(cls, provision_type: str, *args, **kwargs): 
        resource = DISCRIMINATOR.get(provision_type)
        if resource is None: 
            try: 
                return {"status": "error", "message": f"Cannot find resource with provision_type: `${provision_type}`"}, 404
            except Exception as e: 
                return {"status": "error", "message": str(e)}, 500
        return resource.delete(**kwargs)



class CRUD_ConfigProvision_List(BaseCRUDResource):

    @classmethod
    def get(cls, provision_type: str, *args, **kwargs): 
        resource = LIST_DISCRIMINATOR.get(provision_type)
        if resource is None: 
            try: 
                return {"status": "error", "message": f"Cannot find resource with provision_type: `${provision_type}`"}, 404
            except Exception as e: 
                return {"status": "error", "message": str(e)}, 500
        return resource.get(**kwargs)

    @classmethod
    def post(cls, provision_type: str, *args, **kwargs): 
        resource = LIST_DISCRIMINATOR.get(provision_type)
        if resource is None: 
            try: 
                return {"status": "error", "message": f"Cannot find resource with provision_type: `${provision_type}`"}, 404
            except Exception as e: 
                return {"status": "error", "message": str(e)}, 500
        return resource.post(**kwargs)
