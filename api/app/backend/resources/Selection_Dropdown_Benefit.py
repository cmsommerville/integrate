from itertools import groupby
from marshmallow import Schema, fields
from sqlalchemy.sql import or_, func, desc
from sqlalchemy.orm import attributes
from app.extensions import db
from app.shared.utils import system_temporal_hint
from ..models import (
    Model_ConfigBenefitDurationDetail,
    Model_ConfigBenefitDurationDetailAuth_ACL,
    Model_ConfigBenefitDurationSet,
    Model_ConfigBenefitVariationState,
    Model_ConfigBenefit,
    Model_ConfigBenefitAuth,
    Model_ConfigBenefitAuth_ACL,
)


class DDSchema_ConfigBenefitWithDuration(Schema):
    config_product_variation_state_id = fields.Integer()
    config_product_variation_id = fields.Integer()
    config_product_variation_code = fields.String()
    config_product_variation_label = fields.String()
    config_product_variation_state_effective_date = fields.Date()
    config_product_variation_state_expiration_date = fields.Date()
    state_code = fields.String()
    state_name = fields.String()
    version_id = fields.String()


class Temporal_ConfigBenefitDuration:
    @staticmethod
    def _qry_benefit_duration_detail(t, parent_subquery=None):
        BDD = Model_ConfigBenefitDurationDetail
        AUTH = Model_ConfigBenefitDurationDetailAuth_ACL

        qry = (
            db.session.query(BDD)
            .join(
                AUTH,
                BDD.config_benefit_duration_detail_id
                == AUTH.config_benefit_duration_detail_id,
                isouter=True,
            )
            .with_hint(BDD, system_temporal_hint(t))
            .with_hint(AUTH, system_temporal_hint(t))
            .filter(
                or_(
                    BDD.is_restricted == False,
                    AUTH.config_benefit_duration_detail_auth_acl_id == None,
                )
            )
        )
        if parent_subquery is not None:
            qry = qry.join(
                parent_subquery,
                BDD.config_benefit_duration_set_id
                == parent_subquery.c.config_benefit_duration_set_id,
            )
        return qry.order_by(BDD.config_benefit_duration_set_id)

    @staticmethod
    def _qry_benefit_duration_set(t, parent_subquery=None):
        BDS = Model_ConfigBenefitDurationSet

        qry = db.session.query(BDS).with_hint(BDS, system_temporal_hint(t))

        if parent_subquery is not None:
            qry = qry.join(
                parent_subquery,
                BDS.config_benefit_id == parent_subquery.c.config_benefit_id,
            )
        return qry.order_by(BDS.config_benefit_id)

    @classmethod
    def query(cls, t, parent_subquery=None):
        BDS = cls._qry_benefit_duration_set(t, parent_subquery)
        BDD = cls._qry_benefit_duration_detail(t, BDS.subquery())

        children = dict(
            (k, list(v))
            for k, v in groupby(
                BDD,
                lambda x: x.config_benefit_duration_set_id,
            )
        )
        BDS = BDS.all()
        for row in BDS:
            attributes.set_committed_value(
                row,
                "_duration_items",
                children.get(row.config_benefit_duration_set_id, ()),
            )

        return BDS


class Temporal_ConfigBenefitVariationState:
    @staticmethod
    def _qry_benefit_auth_temporal(t, parent_subquery=None):
        """
        Get min/max/step values for benefits as of the time `t`
        """
        AUTH = Model_ConfigBenefitAuth
        ACL = Model_ConfigBenefitAuth_ACL

        row_number_column = (
            func.row_number()
            .over(
                partition_by=AUTH.config_benefit_id,
                order_by=desc(AUTH.priority),
            )
            .label("rn")
        )
        return (
            db.session.query(
                AUTH.config_benefit_id,
                AUTH.min_value,
                AUTH.max_value,
                AUTH.step_value,
                row_number_column,
            )
            .join(ACL, AUTH.config_benefit_auth_id == ACL.config_benefit_auth_id)
            .with_hint(AUTH, system_temporal_hint(t))
            .with_hint(ACL, system_temporal_hint(t))
            .subquery()
        )

    @classmethod
    def _qry_benefit_variation_state_temporal(cls, t, parent_subquery=None):
        BVS = Model_ConfigBenefitVariationState
        BNFT = Model_ConfigBenefit
        qry_bnft = (
            db.session.query(BVS, BNFT)
            .join(BVS, BNFT.config_benefit_id == BVS.config_benefit_id)
            .with_hint(BNFT, system_temporal_hint(t))
            .with_hint(BVS, system_temporal_hint(t))
        )
        if parent_subquery is not None:
            qry_bnft = qry_bnft.join(
                parent_subquery,
                BVS.config_benefit_variation_state_id
                == parent_subquery.c.config_benefit_variation_state_id,
            )

        AUTH = cls._qry_benefit_auth_temporal(t, qry_bnft.subquery())
        qry_bnft = (
            qry_bnft.join(AUTH, AUTH.c.config_benefit_id == BNFT.config_benefit_id)
            .add_columns(AUTH.c.min_value, AUTH.c.max_value, AUTH.c.step_value)
            .filter(AUTH.c.rn == 1)
        )
        return qry_bnft

    @classmethod
    def query(cls, t, parent_subquery=None):
        BVS = cls._qry_benefit_variation_state_temporal(t, parent_subquery)
        BDS = Temporal_ConfigBenefitDuration.query(t, BVS.subquery())

        children = dict(
            (k, list(v))
            for k, v in groupby(
                BDS,
                lambda x: x.config_benefit_id,
            )
        )
        BVS = BVS.all()
        output = []
        for bvs, bnft, minval, maxval, stepval in BVS:
            output.append(
                [
                    bvs,
                    bnft,
                    minval,
                    maxval,
                    stepval,
                    children.get(bnft.config_benefit_id, ()),
                ]
            )

        return output
