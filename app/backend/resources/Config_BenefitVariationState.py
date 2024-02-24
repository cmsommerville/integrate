from typing import List
from flask import request
from flask_restx import Resource
from app.auth import authorization_required
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from app.extensions import db
from sqlalchemy import and_, or_
from ..models import Model_ConfigBenefitVariationState
from ..schemas import (
    Schema_ConfigBenefitVariationState,
    Schema_ConfigBenefitVariationStateRatesetUpdate,
)


class CRUD_ConfigBenefitVariationState(BaseCRUDResource):
    model = Model_ConfigBenefitVariationState
    schema = Schema_ConfigBenefitVariationState()


class CRUD_ConfigBenefitVariationState_List(BaseCRUDResourceList):
    model = Model_ConfigBenefitVariationState
    schema = Schema_ConfigBenefitVariationState(many=True)


class ConfigBenefitVariationStateRateset(Resource):
    permissions: dict = {
        "patch": ["*"],
    }
    schema = Schema_ConfigBenefitVariationStateRatesetUpdate()

    @staticmethod
    def bulk_update_compound_filter(
        model: Model_ConfigBenefitVariationState, list_: List
    ):
        return [
            and_(
                model.config_benefit_variation_state_id
                == row["config_benefit_variation_state_id"],
                model.version_id == row["version_id"],
            )
            for row in list_
        ]

    @authorization_required
    def patch(cls, **kwargs):
        return cls.bulk_update(**kwargs)

    def bulk_update(cls, **kwargs):
        """
        Bulk update the `config_rate_table_set_id` on multiple
        benefit variation state records at once.

        Expects payload of the form:
        ```
        {
            "config_rate_table_set_id": 1,
            "benefit_variation_states": [
                {
                    "config_benefit_variation_state_id": 1,
                    "version_id": "01HPWW4NSFR03EYCBKPZ22J0NZ"
                },
                ...
            ]
        }
        ```
        """
        try:
            raw_data = request.get_json()
            data = cls.schema.load(raw_data)
            model = Model_ConfigBenefitVariationState
            FILTER = cls.bulk_update_compound_filter(
                model, data["benefit_variation_states"]
            )
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

        try:
            db.session.query(model).filter(or_(*FILTER)).update(
                {"config_rate_table_set_id": data["config_rate_table_set_id"]}
            )

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "msg": str(e)}, 400

        return {"msg": "Success"}, 201
