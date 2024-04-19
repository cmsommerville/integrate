from flask import request
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigAttributeDetail
from ..schemas import Schema_ConfigAttributeDetail


class CRUD_ConfigAttributeDetail(BaseCRUDResource):
    model = Model_ConfigAttributeDetail
    schema = Schema_ConfigAttributeDetail()


class CRUD_ConfigAttributeDetail_List(BaseCRUDResourceList):
    model = Model_ConfigAttributeDetail
    schema = Schema_ConfigAttributeDetail(many=True)

    @classmethod
    def list(cls, set_id, *args, **kwargs):
        try:
            objs = cls.model.find_all_by_attr({"config_attr_set_id": set_id})
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

        try:
            if objs:
                return cls.schema.dump(objs), 200
            raise Exception("No data found")
        except Exception:
            return [], 200
