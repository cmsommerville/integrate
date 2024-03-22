from flask import request
from flask_restx import fields
from sqlalchemy import and_
from app.extensions import db, api
from app.shared import (
    BaseCRUDResource,
    BaseCRUDResourceList,
)
from ..models import (
    Model_ConfigProductVariation,
    Model_ConfigProductVariationState,
    Model_ConfigPlanDesignVariationState,
    Model_ConfigPlanDesignSet_Product,
)
from ..schemas import (
    Schema_ConfigProductVariation,
    Schema_ConfigProductVariation_SetPlanDesignVariationStates,
    Schema_ConfigPlanDesignVariationState,
)


class CRUD_ConfigProductVariation(BaseCRUDResource):
    model = Model_ConfigProductVariation
    schema = Schema_ConfigProductVariation()


class CRUD_ConfigProductVariation_List(BaseCRUDResourceList):
    model = Model_ConfigProductVariation
    schema = Schema_ConfigProductVariation(many=True)


model_post = api.model(
    "Resource_ConfigProductVariation_SetPlanDesignVariationStates_POST",
    {
        "config_product_variation_state_id": fields.List(
            fields.Integer,
            description="A list of product variation state IDs that all provided plan design set IDs will be assigned to",
            required=True,
        ),
        "config_plan_design_set_id": fields.List(
            fields.Integer,
            description="A list of plan design IDs that to assign to all provided product variation state IDs",
            required=True,
        ),
    },
)


@api.doc(get=False)
class Resource_ConfigProductVariation_SetPlanDesignVariationStates(
    BaseCRUDResourceList
):
    model = Model_ConfigPlanDesignVariationState
    validation_schema = Schema_ConfigProductVariation_SetPlanDesignVariationStates()
    schema = Schema_ConfigPlanDesignVariationState(many=True)

    @classmethod
    @api.doc(
        model=model_post,
        validate=True,
        description="Assign multiple plan design set IDs to multiple product variation state IDs at once. All product variation state IDs must belong to the product variation ID route parameter (parent_id).\n\nTHIS METHOD IS IDEMPOTENT. If you pass existing combinations of plan designs and states, it will return the existing records and not create new ones.",
    )
    def post(cls, *args, **kwargs):
        return super().post(*args, **kwargs)

    @classmethod
    def list(cls, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    @staticmethod
    def validate_input_ids(input_ids, database_ids):
        if any([i not in database_ids for i in input_ids]):
            raise ValueError("Invalid plan design id(s) provided")

    @classmethod
    def cross_join_plan_design_variation_states(
        cls, product_variation_id, validated_data
    ):
        PVS = Model_ConfigProductVariationState
        PDS = Model_ConfigPlanDesignSet_Product
        PDVS = Model_ConfigPlanDesignVariationState

        qryPVS = (
            db.session.query(PVS.config_product_variation_state_id)
            .filter(
                PVS.config_product_variation_id == product_variation_id,
                PVS.config_product_variation_state_id.in_(
                    validated_data["config_product_variation_state_id"]
                ),
            )
            .subquery()
        )
        qryPDS = (
            db.session.query(PDS.config_plan_design_set_id)
            .filter(
                PDS.config_plan_design_set_id.in_(
                    validated_data["config_plan_design_set_id"]
                )
            )
            .subquery()
        )

        # this query intentionally joins a column to itself to suppress a cross join warning
        # we want a cross join here, so we don't need a warning
        qryCrossJoin = (
            db.session.query(
                qryPVS.c.config_product_variation_state_id,
                qryPDS.c.config_plan_design_set_id,
            )
            .select_from(qryPVS)
            .join(
                qryPDS,
                qryPVS.c.config_product_variation_state_id
                == qryPVS.c.config_product_variation_state_id,  # INTENTIONAL JOIN
            )
            .subquery()
        )
        res = db.session.query(qryCrossJoin).all()

        # validate product variation state ids
        cls.validate_input_ids(
            validated_data["config_product_variation_state_id"], [row[0] for row in res]
        )
        # validate plan design set ids
        cls.validate_input_ids(
            validated_data["config_plan_design_set_id"], [row[1] for row in res]
        )

        # this merges existing plan design variation states' IDs with the new ones
        res = (
            db.session.query(qryCrossJoin, PDVS.config_plan_design_variation_state_id)
            .join(
                PDVS,
                and_(
                    qryCrossJoin.c.config_product_variation_state_id
                    == PDVS.config_product_variation_state_id,
                    qryCrossJoin.c.config_plan_design_set_id
                    == PDVS.config_plan_design_set_id,
                ),
                isouter=True,
            )
            .all()
        )

        return [
            {
                "config_product_variation_state_id": row[0],
                "config_plan_design_set_id": row[1],
                **(
                    {"config_plan_design_variation_state_id": row[2]}
                    if row[2] is not None
                    else {}
                ),
            }
            for row in res
        ]

    @classmethod
    def bulk_create(cls, parent_id: int, *args, **kwargs):
        req = request.get_json()
        validated_input_data = cls.validation_schema.dump(req)
        validated_data = cls.cross_join_plan_design_variation_states(
            parent_id, validated_input_data
        )
        objs = cls.schema.load(validated_data)
        cls.model.save_all_to_db(objs)
        return cls.schema.dump(objs)
