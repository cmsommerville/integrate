from marshmallow import Schema, fields, ValidationError
from sqlalchemy.orm import joinedload
from app.extensions import db
from ..models import (
    Model_SelectionPlan,
    Model_SelectionRatingMapperSet,
    Model_SelectionRatingMapperDetail,
    Model_ConfigProduct,
    Model_ConfigRatingMapperSet,
)
from ..schemas import Schema_SelectionAgeBand


class RowNotFoundError(Exception):
    pass


class Schema_UpdateRatingMapper(Schema):
    selection_rating_mapper_set_type = fields.String(required=True)
    config_rating_mapper_set_id = fields.Integer(required=True)
    has_custom_weights = fields.Boolean(default=False)


class Selection_RPC_RatingMapper:
    schema = Schema_SelectionAgeBand(many=True)

    @classmethod
    def get_rating_mapper_set(cls, payload, plan_id, *args, **kwargs):
        selection_rating_mapper_set_type = payload["selection_rating_mapper_set_type"]

        RMS = Model_ConfigRatingMapperSet
        PROD = Model_ConfigProduct
        PLAN = Model_SelectionPlan

        PRODUCT_MAPPER = getattr(
            PROD,
            f"rating_mapper_collection_id{selection_rating_mapper_set_type[-1]}",
        )
        return (
            db.session.query(RMS)
            .select_from(RMS)
            .join(
                PROD,
                PRODUCT_MAPPER == RMS.config_rating_mapper_collection_id,
            )
            .join(PLAN, PLAN.config_product_id == PROD.config_product_id)
            .options(joinedload(RMS.mapper_details))
            .filter(
                PLAN.selection_plan_id == plan_id,
                RMS.config_rating_mapper_set_id
                == payload["config_rating_mapper_set_id"],
            )
            .one()
        )

    @classmethod
    def update_rating_mapper(cls, payload, plan_id, *args, **kwargs):
        validated_data = Schema_UpdateRatingMapper().load(payload)
        config_rating_mapper_set = cls.get_rating_mapper_set(validated_data, plan_id)

        db.session.query(Model_SelectionRatingMapperSet).filter(
            Model_SelectionRatingMapperSet.selection_plan_id == plan_id
        ).delete()
        selection_rating_mapper_set = Model_SelectionRatingMapperSet(
            **{
                **validated_data,
                "selection_plan_id": plan_id,
                "config_rating_mapper_set_id": config_rating_mapper_set.config_rating_mapper_set_id,
                "mapper_details": [
                    Model_SelectionRatingMapperDetail(
                        config_rating_mapper_detail=d.config_rating_mapper_detail_id,
                        rate_table_attribute_detail_id=d.rate_table_attribute_detail_id,
                        output_attribute_detail_id=d.output_attribute_detail_id,
                        default_weight=d.default_weight,
                        weight=d.default_weight,
                    )
                    for d in config_rating_mapper_set.mapper_details
                ],
            }
        )

        db.session.add_all(selection_rating_mapper_set)
        db.session.flush()
