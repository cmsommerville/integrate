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

    @staticmethod
    def identify_parent(parent_id: int):
        bnft_route_part = f"benefit/{parent_id}/provisions"
        prov_route_part = f"provision/{parent_id}/benefits"
        if bnft_route_part in request.path:
            return "BENEFIT"
        elif prov_route_part in request.path:
            return "PROVISION"
        else:
            raise Exception(
                "Cannot determine whether parent_id is a provision_id or benefit_id"
            )

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
        parent_id = kwargs.get("parent_id")
        parent_type = cls.identify_parent(parent_id)
        data = request.get_json()
        if parent_type == "BENEFIT":
            modified_data = [
                {"config_provision_id": val, "config_benefit_id": parent_id}
                for val in data["config_provision_id"]
            ]
        elif parent_type == "PROVISION":
            modified_data = [
                {"config_benefit_id": val, "config_provision_id": parent_id}
                for val in data["config_benefit_id"]
            ]
        else:
            raise Exception("Route must contain either `benefit_id` or `provision_id`")

        objs = cls.schema.load(modified_data)
        cls.model.save_all_to_db(objs)
        return cls.schema.dump(objs)
