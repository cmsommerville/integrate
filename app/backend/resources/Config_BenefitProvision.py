from flask import request
from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigBenefitProvision
from ..schemas import Schema_ConfigBenefitProvision


class CRUD_ConfigBenefitProvision(BaseCRUDResource):
    model = Model_ConfigBenefitProvision
    schema = Schema_ConfigBenefitProvision()


class CRUD_ConfigBenefitProvision_List(BaseCRUDResourceList):
    model = Model_ConfigBenefitProvision
    schema = Schema_ConfigBenefitProvision(many=True)

    @classmethod
    def bulk_create(cls, *args, **kwargs):
        """
        Handles requests of two forms:
        ```
        {
            "config_provision_id": [1, 2, 3, ...]
        }
        ```
        ...or...
        ```
        {
            "config_benefit_id": [1, 2, 3, ...],
        }
        ```
        """
        config_benefit_id = kwargs.get("benefit_id", None)
        config_provision_id = kwargs.get("provision_id", None)
        data = request.get_json()
        if config_benefit_id is not None:
            modified_data = [
                {"config_provision_id": val, "config_benefit_id": config_benefit_id}
                for val in data["config_provision_id"]
            ]
        elif config_provision_id is not None:
            modified_data = [
                {"config_benefit_id": val, "config_provision_id": config_provision_id}
                for val in data["config_benefit_id"]
            ]
        else:
            raise Exception("Route must contain either `benefit_id` or `provision_id`")

        objs = cls.schema.load(modified_data)
        cls.model.save_all_to_db(objs)
        return cls.schema.dump(objs)
