from marshmallow import Schema, fields
from app.extensions import db
from app.shared.utils import system_temporal_hint
from app.shared.errors import RowNotFoundError
from sqlalchemy.sql import and_
from ..models import (
    Model_SelectionPlan,
    Model_SelectionRatingMapperSet,
    Model_SelectionRatingMapperDetail,
    Model_ConfigProduct,
    Model_ConfigRatingMapperSet,
    Model_ConfigRatingMapperDetail,
)


class Schema_UpdateRatingMapper(Schema):
    selection_rating_mapper_set_type = fields.String(required=True)
    config_rating_mapper_set_id = fields.Integer(required=True)
    has_custom_weights = fields.Boolean(default=False)


class Selection_RPC_RatingMapper:
    def __init__(self, payload, plan_id, *args, **kwargs):
        self.payload = payload
        self.validated_data = Schema_UpdateRatingMapper().load(self.payload)
        self.plan_id = plan_id
        self.plan = Model_SelectionPlan.find_one(plan_id)
        if self.plan is None:
            raise RowNotFoundError("Plan not found")
        self.t = self.plan.plan_as_of_dts

    def get_rating_mapper_details(self, payload, plan_id, *args, **kwargs):
        selection_rating_mapper_set_type = payload["selection_rating_mapper_set_type"]

        RMS = Model_ConfigRatingMapperSet
        RMD = Model_ConfigRatingMapperDetail
        PROD = Model_ConfigProduct
        PLAN = Model_SelectionPlan

        PRODUCT_MAPPER = getattr(
            PROD,
            f"rating_mapper_collection_id{selection_rating_mapper_set_type[-1]}",
        )
        qry = (
            db.session.query(RMD)
            .select_from(RMD)
            .join(
                RMS, RMS.config_rating_mapper_set_id == RMD.config_rating_mapper_set_id
            )
            .join(
                PROD,
                PRODUCT_MAPPER == RMS.config_rating_mapper_collection_id,
            )
            .join(PLAN, PLAN.config_product_id == PROD.config_product_id)
            .filter(
                PLAN.selection_plan_id == plan_id,
                RMS.config_rating_mapper_set_id
                == payload["config_rating_mapper_set_id"],
            )
        )
        if self.t is not None:
            hint = system_temporal_hint(self.t)
            qry = qry.with_hint(RMD, hint).with_hint(RMS, hint).with_hint(PROD, hint)

        return qry.all()

    def update_rating_mapper(self, *args, **kwargs):
        config_rating_mapper_details = self.get_rating_mapper_details(
            self.validated_data, self.plan_id
        )
        if not config_rating_mapper_details:
            raise RowNotFoundError("Rating Mapper not found")

        db.session.query(Model_SelectionRatingMapperSet).filter(
            and_(
                Model_SelectionRatingMapperSet.selection_plan_id == self.plan_id,
                Model_SelectionRatingMapperSet.selection_rating_mapper_set_type
                == self.validated_data["selection_rating_mapper_set_type"],
            )
        ).delete()
        selection_rating_mapper_set = Model_SelectionRatingMapperSet(
            **{
                **self.validated_data,
                "selection_plan_id": self.plan_id,
                "config_rating_mapper_set_id": self.validated_data[
                    "config_rating_mapper_set_id"
                ],
                "mapper_details": [
                    Model_SelectionRatingMapperDetail(
                        config_rating_mapper_detail=d.config_rating_mapper_detail_id,
                        rate_table_attribute_detail_id=d.rate_table_attribute_detail_id,
                        output_attribute_detail_id=d.output_attribute_detail_id,
                        default_weight=d.default_weight,
                        weight=d.default_weight,
                    )
                    for d in config_rating_mapper_details
                ],
            }
        )

        db.session.add_all(selection_rating_mapper_set)
        db.session.flush()
