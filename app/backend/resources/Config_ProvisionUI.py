from flask import request
from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigProvisionUI, Model_ConfigProvisionUI_Input, Model_ConfigProvisionUI_Checkbox, Model_ConfigProvisionUI_Select
from ..schemas import Schema_ConfigProvisionUI, Schema_ConfigProvisionUI_Input, Schema_ConfigProvisionUI_Checkbox, Schema_ConfigProvisionUI_Select


def discriminator(item): 
    models = [Model_ConfigProvisionUI_Input, Model_ConfigProvisionUI_Checkbox, Model_ConfigProvisionUI_Select]
    schemas = [Schema_ConfigProvisionUI_Input, Schema_ConfigProvisionUI_Checkbox, Schema_ConfigProvisionUI_Select]
    for ix, model in enumerate(models):
        if model.__mapper_args__.get('polymorphic_identity') == item.get('component_type_code'):
            schema = schemas[ix]
            return model, schema
    return None, None

class CRUD_ConfigProvisionUI(BaseCRUDResource): 
    model = Model_ConfigProvisionUI
    schema = Schema_ConfigProvisionUI()

    @classmethod
    def post(cls, *args, **kwargs):
        data = request.get_json()
        try: 
            model, schema = discriminator(data)
            if not model:  
                return {"status": "error", "message": str(e)}, 400
            _schema = schema()
            obj = _schema.load(data)
            res = model.save_to_db(obj)
            output = _schema.dump(res)
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400
        
        return output, 201
        
        

class CRUD_ConfigProvisionUI_List(BaseCRUDResourceList): 
    model = Model_ConfigProvisionUI
    schema = Schema_ConfigProvisionUI(many=True)

    @classmethod
    def post(cls, *args, **kwargs):
        data = request.get_json()
        try: 
            for item in data: 
                model, schema = discriminator(item)
                if not model:  
                    continue
                _schema = schema()
                obj = _schema.load(item)
                model.save_to_db(obj)
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

        return data, 201