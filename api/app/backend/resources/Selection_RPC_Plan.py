import datetime
from typing import List
from marshmallow import Schema, fields
from sqlalchemy.sql import func, desc, and_, text
from sqlalchemy.sql.functions import coalesce
from sqlalchemy.sql.expression import literal_column
from app.extensions import db
from app.auth import get_user, NotAuthorizedError
from app.shared.utils import system_temporal_hint
from app.shared.errors import PlanInvalidError
from ..classes import FactorRulesetApplicator
from ..models import (
    Model_ConfigAgeBandDetail,
    Model_ConfigBenefitDurationDetailAuth_ACL,
    Model_ConfigBenefit,
    Model_ConfigBenefitAuth,
    Model_ConfigBenefitAuth_ACL,
    Model_ConfigBenefitDurationDetail,
    Model_ConfigBenefitDurationSet,
    Model_ConfigBenefitVariationState,
    Model_ConfigFactorSet,
    Model_ConfigFactor,
    Model_ConfigPlanDesignSet_Product,
    Model_ConfigPlanDesignSet_Coverage,
    Model_ConfigPlanDesignDetail_Benefit,
    Model_ConfigPlanDesignDetail_PlanDesign,
    Model_ConfigProductVariation,
    Model_ConfigProductVariationState,
    Model_ConfigProvision,
    Model_ConfigProvisionState,
    Model_DefaultProductRatingMapperSet,
    Model_SelectionAgeBand,
    Model_SelectionPlan,
    Model_SelectionPlan_ACL,
    Model_SelectionCoverage,
    Model_SelectionFactor,
    Model_SelectionBenefit,
    Model_SelectionBenefitDuration,
    Model_SelectionProvision,
    Model_SelectionRatingMapperSet,
)
from ..schemas import (
    Schema_SelectionPlan,
)

WITH_GRANT_OPTION = True


class Schema_CreatePlanDefault(Schema):
    config_product_variation_state_id = fields.Integer(required=True)
    situs_state_id = fields.Integer(required=True)
    selection_plan_effective_date = fields.Date(required=True)


class Schema_GrantPlanACL(Schema):
    user_name = fields.String(required=True)
    with_grant_option = fields.Boolean(default=False)


class Schema_RevokePlanACL(Schema):
    user_name = fields.String(required=True)


class SelectionProvisionMixin:
    @classmethod
    def _qry_insert_selection_provision(cls, plan: Model_SelectionPlan, t=None):
        tbl_SP = Model_SelectionProvision.__table__
        tbl_PS = Model_ConfigProvisionState.__table__
        tbl_P = Model_ConfigProvision.__table__

        hint = system_temporal_hint(t)
        return (
            tbl_SP.insert()
            .from_select(
                [
                    "selection_plan_id",
                    "config_provision_state_id",
                    "selection_value",
                    "version_id",
                    "created_dts",
                    "updated_dts",
                    "updated_by",
                ],
                db.session.query(
                    literal_column(f"{plan.selection_plan_id}").label(
                        "selection_plan_id"
                    ),
                    tbl_PS.c.config_provision_state_id,
                    tbl_P.c.default_value,
                    *cls.watermark_fields(),
                )
                .select_from(tbl_PS)
                .join(
                    tbl_P, tbl_P.c.config_provision_id == tbl_PS.c.config_provision_id
                )
                .with_hint(tbl_PS, hint)
                .with_hint(tbl_P, hint)
                .filter(
                    tbl_PS.c.state_id == plan.situs_state_id,
                    tbl_P.c.config_product_id == plan.config_product_id,
                    tbl_PS.c.config_provision_state_effective_date
                    <= plan.selection_plan_effective_date,
                    tbl_PS.c.config_provision_state_expiration_date
                    >= plan.selection_plan_effective_date,
                ),
            )
            .returning(
                tbl_SP.c.selection_provision_id,
                tbl_SP.c.selection_plan_id,
                tbl_SP.c.config_provision_state_id,
                tbl_SP.c.selection_value,
                tbl_SP.c.version_id,
                tbl_SP.c.created_dts,
                tbl_SP.c.updated_dts,
                tbl_SP.c.updated_by,
            )
        )


class SelectionBenefitMixin:
    @classmethod
    def _qry_get_default_benefit_amounts(cls, plan: Model_SelectionPlan, t=None):
        tbl_BVS = Model_ConfigBenefitVariationState.__table__
        tbl_BNFT = Model_ConfigBenefit.__table__
        tbl_BA = Model_ConfigBenefitAuth.__table__
        tbl_BACL = Model_ConfigBenefitAuth_ACL.__table__

        hint = system_temporal_hint(t)
        row_number_column = (
            func.row_number()
            .over(
                partition_by=tbl_BVS.c.config_benefit_variation_state_id,
                order_by=desc(tbl_BA.c.priority),
            )
            .label("rn")
        )

        qry = (
            db.session.query(
                tbl_BVS.c.config_benefit_variation_state_id,
                tbl_BNFT.c.config_coverage_id,
                tbl_BA.c.priority,
                tbl_BA.c.default_value,
            )
            .select_from(tbl_BVS)
            .join(tbl_BNFT, tbl_BNFT.c.config_benefit_id == tbl_BVS.c.config_benefit_id)
            .join(tbl_BA, tbl_BA.c.config_benefit_id == tbl_BNFT.c.config_benefit_id)
            .join(
                tbl_BACL,
                tbl_BACL.c.config_benefit_auth_id == tbl_BA.c.config_benefit_auth_id,
            )
            .with_hint(tbl_BVS, hint)
            .with_hint(tbl_BNFT, hint)
            .with_hint(tbl_BA, hint)
            .with_hint(tbl_BACL, hint)
            .filter(
                tbl_BVS.c.config_product_variation_state_id
                == plan.config_product_variation_state_id,
                tbl_BVS.c.config_benefit_variation_state_effective_date
                <= plan.selection_plan_effective_date,
                tbl_BVS.c.config_benefit_variation_state_expiration_date
                >= plan.selection_plan_effective_date,
            )
            .add_column(row_number_column)
            .subquery()
        )

        return db.session.query(qry).filter(qry.c.rn == 1).subquery()

    @classmethod
    def _qry_insert_selection_coverage__no_plan_design(
        cls, plan: Model_SelectionPlan, t=None
    ):
        tbl_SC = Model_SelectionCoverage.__table__

        benefit_amount_qry = cls._qry_get_default_benefit_amounts(plan, t)
        distinct_coverage_qry = (
            db.session.query(benefit_amount_qry.c.config_coverage_id)
            .distinct()
            .subquery()
        )

        return tbl_SC.insert().from_select(
            [
                "selection_plan_id",
                "config_coverage_id",
                "version_id",
                "created_dts",
                "updated_dts",
                "updated_by",
            ],
            db.session.query(
                literal_column(f"{plan.selection_plan_id}").label("selection_plan_id"),
                distinct_coverage_qry.c.config_coverage_id,
                *cls.watermark_fields(),
            ),
        )

    @classmethod
    def _qry_insert_selection_benefit__no_plan_design(
        cls, plan: Model_SelectionPlan, t=None
    ):
        tbl_SB = Model_SelectionBenefit.__table__
        tbl_SC = Model_SelectionCoverage.__table__

        benefit_amount_qry = cls._qry_get_default_benefit_amounts(plan, t)

        return tbl_SB.insert().from_select(
            [
                "selection_plan_id",
                "selection_coverage_id",
                "config_benefit_variation_state_id",
                "selection_value",
                "version_id",
                "created_dts",
                "updated_dts",
                "updated_by",
            ],
            db.session.query(
                literal_column(f"{plan.selection_plan_id}").label("selection_plan_id"),
                tbl_SC.c.selection_coverage_id,
                benefit_amount_qry.c.config_benefit_variation_state_id,
                benefit_amount_qry.c.default_value,
                *cls.watermark_fields(),
            )
            .select_from(benefit_amount_qry)
            .join(
                tbl_SC,
                tbl_SC.c.config_coverage_id == benefit_amount_qry.c.config_coverage_id,
            )
            .filter(tbl_SC.c.selection_plan_id == plan.selection_plan_id),
        )

    @classmethod
    def _qry_insert_selection_coverage__plan_design(
        cls, plan: Model_SelectionPlan, t=None
    ):
        """
        Returns an insert query for the default coverages of a new plan based on the default product plan design
        """

        tbl_PVS = Model_ConfigProductVariationState.__table__
        tbl_PPDS = Model_ConfigPlanDesignSet_Product.__table__
        tbl_PPDD = Model_ConfigPlanDesignDetail_PlanDesign.__table__
        tbl_CPDS = Model_ConfigPlanDesignSet_Coverage.__table__
        tbl_SC = Model_SelectionCoverage.__table__

        hint = system_temporal_hint(t)
        return tbl_SC.insert().from_select(
            [
                "selection_plan_id",
                "config_coverage_id",
                "config_plan_design_set_id",
                "version_id",
                "created_dts",
                "updated_dts",
                "updated_by",
            ],
            db.session.query(
                literal_column(f"{plan.selection_plan_id}").label("selection_plan_id"),
                tbl_CPDS.c.config_parent_id,
                tbl_CPDS.c.config_plan_design_set_id,
                *cls.watermark_fields(),
            )
            .select_from(tbl_PVS)
            .join(
                tbl_PPDS,
                tbl_PPDS.c.config_plan_design_set_id
                == tbl_PVS.c.default_plan_design_set_id,
            )
            .join(
                tbl_PPDD,
                tbl_PPDS.c.config_plan_design_set_id
                == tbl_PPDD.c.config_plan_design_set_id,
            )
            .join(
                tbl_CPDS,
                tbl_CPDS.c.config_plan_design_set_id == tbl_PPDD.c.config_parent_id,
            )
            .with_hint(tbl_PVS, hint)
            .with_hint(tbl_PPDS, hint)
            .with_hint(tbl_PPDD, hint)
            .with_hint(tbl_CPDS, hint)
            .filter(
                tbl_PVS.c.config_product_variation_state_id
                == plan.config_product_variation_state_id,
                tbl_PPDS.c.config_parent_type_code == "product",
                tbl_PPDD.c.config_parent_type_code == "plan_design",
                tbl_CPDS.c.config_parent_type_code == "coverage",
            ),
        )

    @classmethod
    def _qry_insert_selection_benefit__plan_design(
        cls, plan: Model_SelectionPlan, t=None
    ):
        """
        Returns an insert query for the default coverages of a new plan based on the default product plan design
        """

        tbl_BVS = Model_ConfigBenefitVariationState.__table__
        tbl_CPDD = Model_ConfigPlanDesignDetail_Benefit.__table__
        tbl_SB = Model_SelectionBenefit.__table__
        tbl_SC = Model_SelectionCoverage.__table__
        hint = system_temporal_hint(t)

        return tbl_SB.insert().from_select(
            [
                "selection_plan_id",
                "selection_coverage_id",
                "config_benefit_variation_state_id",
                "selection_value",
                "version_id",
                "created_dts",
                "updated_dts",
                "updated_by",
            ],
            db.session.query(
                literal_column(f"{plan.selection_plan_id}").label("selection_plan_id"),
                tbl_SC.c.selection_coverage_id,
                tbl_BVS.c.config_benefit_variation_state_id,
                tbl_CPDD.c.default_value,
                *cls.watermark_fields(),
            )
            .select_from(tbl_SC)
            .join(
                tbl_CPDD,
                tbl_CPDD.c.config_plan_design_set_id
                == tbl_SC.c.config_plan_design_set_id,
            )
            .join(
                tbl_BVS,
                and_(
                    tbl_BVS.c.config_benefit_id == tbl_CPDD.c.config_parent_id,
                    tbl_BVS.c.config_product_variation_state_id
                    == plan.config_product_variation_state_id,
                    tbl_BVS.c.config_benefit_variation_state_effective_date
                    <= plan.selection_plan_effective_date,
                    tbl_BVS.c.config_benefit_variation_state_expiration_date
                    >= plan.selection_plan_effective_date,
                ),
            )
            .with_hint(tbl_CPDD, hint)
            .with_hint(tbl_BVS, hint)
            .filter(
                tbl_SC.c.selection_plan_id == plan.selection_plan_id,
                tbl_CPDD.c.config_parent_type_code == "benefit",
            ),
        )

    @classmethod
    def _qry_get_first_benefit_duration_detail(cls, plan: Model_SelectionPlan, t=None):
        hint = system_temporal_hint(t)
        tbl_BDD = Model_ConfigBenefitDurationDetail.__table__
        tbl_BDS = Model_ConfigBenefitDurationSet.__table__
        tbl_BVS = Model_ConfigBenefitVariationState.__table__
        tbl_BDACL = Model_ConfigBenefitDurationDetailAuth_ACL.__table__

        tbl_BDD2 = (
            db.session.query(Model_ConfigBenefitDurationDetail.__table__)
            .with_hint(Model_ConfigBenefitDurationDetail.__table__, hint)
            .subquery()
        )

        qry = (
            db.session.query(
                tbl_BDD.c.config_benefit_duration_set_id,
                func.min(tbl_BDD.c.config_benefit_duration_detail_id).label(
                    "config_benefit_duration_detail_id"
                ),
            )
            .select_from(tbl_BDD)
            .join(
                tbl_BDACL,
                tbl_BDACL.c.config_benefit_duration_detail_id
                == tbl_BDD.c.config_benefit_duration_detail_id,
            )
            .join(
                tbl_BDS,
                tbl_BDS.c.config_benefit_duration_set_id
                == tbl_BDD.c.config_benefit_duration_set_id,
            )
            .join(
                tbl_BVS,
                tbl_BVS.c.config_benefit_id == tbl_BDS.c.config_benefit_id,
            )
            .with_hint(tbl_BDD, hint)
            .with_hint(tbl_BDACL, hint)
            .with_hint(tbl_BDS, hint)
            .with_hint(tbl_BVS, hint)
            .filter(
                tbl_BVS.c.config_product_variation_state_id
                == plan.config_product_variation_state_id,
            )
            .group_by(tbl_BDD.c.config_benefit_duration_set_id)
            .subquery()
        )

        qry = (
            db.session.query(
                qry.c.config_benefit_duration_set_id,
                qry.c.config_benefit_duration_detail_id,
                tbl_BDD2.c.config_benefit_duration_factor,
            )
            .select_from(qry)
            .join(
                tbl_BDD2,
                tbl_BDD2.c.config_benefit_duration_detail_id
                == qry.c.config_benefit_duration_detail_id,
            )
            .subquery()
        )
        return qry

    @classmethod
    def _qry_insert_selection_benefit_duration(cls, plan: Model_SelectionPlan, t=None):
        """
        Returns an insert query for the default coverages of a new plan based on the default product plan design
        """

        tbl_BVS = Model_ConfigBenefitVariationState.__table__
        tbl_BDS = Model_ConfigBenefitDurationSet.__table__
        tbl_BDD = Model_ConfigBenefitDurationDetail.__table__
        tbl_SB = Model_SelectionBenefit.__table__
        tbl_SBD = Model_SelectionBenefitDuration.__table__
        hint = system_temporal_hint(t)
        qry_min_benefit_duration_detail = cls._qry_get_first_benefit_duration_detail(
            plan, t
        )

        return tbl_SBD.insert().from_select(
            [
                "selection_benefit_id",
                "config_benefit_duration_set_id",
                "config_benefit_duration_detail_id",
                "selection_factor",
                "version_id",
                "created_dts",
                "updated_dts",
                "updated_by",
            ],
            db.session.query(
                tbl_SB.c.selection_benefit_id,
                tbl_BDS.c.config_benefit_duration_set_id,
                coalesce(
                    tbl_BDS.c.default_config_benefit_duration_detail_id,
                    qry_min_benefit_duration_detail.c.config_benefit_duration_detail_id,
                ),
                coalesce(
                    tbl_BDD.c.config_benefit_duration_factor,
                    qry_min_benefit_duration_detail.c.config_benefit_duration_factor,
                ),
                *cls.watermark_fields(),
            )
            .select_from(tbl_SB)
            .join(
                tbl_BVS,
                tbl_BVS.c.config_benefit_variation_state_id
                == tbl_SB.c.config_benefit_variation_state_id,
            )
            .join(
                tbl_BDS,
                tbl_BDS.c.config_benefit_id == tbl_BVS.c.config_benefit_id,
            )
            .join(
                tbl_BDD,
                tbl_BDD.c.config_benefit_duration_detail_id
                == tbl_BDS.c.default_config_benefit_duration_detail_id,
                isouter=True,
            )
            .join(
                qry_min_benefit_duration_detail,
                qry_min_benefit_duration_detail.c.config_benefit_duration_set_id
                == tbl_BDS.c.config_benefit_duration_set_id,
                isouter=True,
            )
            .with_hint(tbl_BVS, hint)
            .with_hint(tbl_BDS, hint)
            .with_hint(tbl_BDD, hint)
            .filter(
                tbl_SB.c.selection_plan_id == plan.selection_plan_id,
            ),
        )


class SelectionPlanMixin:
    @classmethod
    def query_plan_acl_with_grant_option(cls, plan_id, user_name, *args, **kwargs):
        PLAN = Model_SelectionPlan
        ACL = Model_SelectionPlan_ACL
        return (
            db.session.query(PLAN, ACL.with_grant_option)
            .join(ACL, ACL.selection_plan_id == PLAN.selection_plan_id)
            .filter(PLAN.selection_plan_id == plan_id, ACL.user_name == user_name)
            .first()
        )


class Selection_RPC_Plan(
    FactorRulesetApplicator,
    SelectionProvisionMixin,
    SelectionBenefitMixin,
    SelectionPlanMixin,
):
    schema = Schema_SelectionPlan(exclude=("coverages",))

    def __init__(self, payload, *args, **kwargs):
        self.payload = payload
        self.t = kwargs.get("t")
        self.hint = system_temporal_hint(self.t)

    @classmethod
    def watermark_fields(cls):
        """
        Standard watermark fields for all tables
        """
        user = get_user()
        user_name = user.get("user_name")
        return [
            literal_column("dbo.ulidstr()").label("version_id"),
            literal_column("CURRENT_TIMESTAMP").label("created_dts"),
            literal_column("CURRENT_TIMESTAMP").label("updated_dts"),
            literal_column(f"'{user_name}'").label("updated_by"),
        ]

    def _create_plan(self, payload):
        """
        Create the plan object from the payload
        """
        is_plan_valid = Model_ConfigProductVariationState.is_plan_valid(
            payload["config_product_variation_state_id"],
            payload["situs_state_id"],
            payload["selection_plan_effective_date"],
        )
        if is_plan_valid:
            variation = (
                db.session.query(Model_ConfigProductVariation)
                .join(
                    Model_ConfigProductVariationState,
                    Model_ConfigProductVariationState.config_product_variation_id
                    == Model_ConfigProductVariation.config_product_variation_id,
                )
                .with_hint(Model_ConfigProductVariation, self.hint)
                .with_hint(Model_ConfigProductVariationState, self.hint)
                .filter(
                    Model_ConfigProductVariationState.config_product_variation_state_id
                    == payload["config_product_variation_state_id"]
                )
                .one()
            )
            user = get_user()
            default_acl = {
                "user_name": user.get("user_name"),
                "with_grant_option": WITH_GRANT_OPTION,
            }
            return self.schema.load(
                {
                    **payload,
                    "plan_as_of_dts": self.t.strftime("%Y-%m-%d %H:%M:%S.%f"),
                    "config_product_id": variation.config_product_id,
                    "acl": [default_acl],
                }
            )
        raise PlanInvalidError(
            "Situs state, product variation, and effective date are incompatible"
        )

    def _create_rating_mappers(self, plan: Model_SelectionPlan, *args, **kwargs):
        """
        Create the selection rating mappers. This is an insert query of data already in the database.
        This is an INSERT from SELECT query
        """
        tbl_DRMS = Model_DefaultProductRatingMapperSet.__table__
        tbl_RMS = Model_SelectionRatingMapperSet.__table__
        qry = tbl_RMS.insert().from_select(
            [
                "selection_plan_id",
                "selection_rating_mapper_set_type",
                "config_rating_mapper_set_id",
                "has_custom_weights",
                "version_id",
                "created_dts",
                "updated_dts",
                "updated_by",
            ],
            db.session.query(
                literal_column(f"{plan.selection_plan_id}").label("selection_plan_id"),
                tbl_DRMS.c.selection_rating_mapper_set_type,
                tbl_DRMS.c.default_config_rating_mapper_set_id,
                literal_column(str(int(False))).label("has_custom_weights"),
                *self.watermark_fields(),
            ).filter(tbl_DRMS.c.config_product_id == plan.config_product_id),
        )

        db.session.execute(qry)

    def _create_age_bands(self, plan: Model_SelectionPlan, *args, **kwargs):
        """
        Create the selection age bands. This is an insert query of data already in the database.
        This is an INSERT from SELECT query.

        If there are no default age bands, then a generic 0-999 single record age band is created.
        """
        config_product_variation_state = plan.config_product_variation_state
        tbl_CABD = Model_ConfigAgeBandDetail.__table__
        tbl_SAB = Model_SelectionAgeBand.__table__

        if config_product_variation_state.default_config_age_band_set_id is None:
            age_band = Model_SelectionAgeBand(
                selection_plan_id=plan.selection_plan_id,
                age_band_lower=0,
                age_band_upper=999,
            )
            db.session.add(age_band)
        else:
            qry = tbl_SAB.insert().from_select(
                [
                    "selection_plan_id",
                    "age_band_lower",
                    "age_band_upper",
                    "version_id",
                    "created_dts",
                    "updated_dts",
                    "updated_by",
                ],
                db.session.query(
                    literal_column(f"{plan.selection_plan_id}").label(
                        "selection_plan_id"
                    ),
                    tbl_CABD.c.age_band_lower,
                    tbl_CABD.c.age_band_upper,
                    *self.watermark_fields(),
                )
                .with_hint(tbl_CABD, self.hint)
                .filter(
                    tbl_CABD.c.config_age_band_set_id
                    == config_product_variation_state.default_config_age_band_set_id
                ),
            )

            db.session.execute(qry)

    def _create_coverage_benefits(self, plan: Model_SelectionPlan, *args, **kwargs):
        """
        Create the selection coverages, benefits, and benefit durations.
        This is an insert query of data already in the database.

        This is an INSERT from SELECT query
        """
        STATS = {}
        config_product_variation_state = plan.config_product_variation_state

        if config_product_variation_state.default_plan_design_set_id is None:
            # create coverages based on benefit-defined defaults
            qry = self._qry_insert_selection_coverage__no_plan_design(plan, t=self.t)
            res = db.session.execute(qry)
            STATS["coverages"] = res.rowcount

            # create benefits based on benefit-defined defaults
            qry = self._qry_insert_selection_benefit__no_plan_design(plan, t=self.t)
            res = db.session.execute(qry)
            STATS["benefits"] = res.rowcount
        else:
            # create coverages from default plan design
            qry = self._qry_insert_selection_coverage__plan_design(plan, t=self.t)
            res = db.session.execute(qry)
            STATS["coverages"] = res.rowcount

            # create benefits from default plan design
            qry = self._qry_insert_selection_benefit__plan_design(plan, t=self.t)
            res = db.session.execute(qry)
            STATS["benefits"] = res.rowcount

        # create benefit durations
        # this doesn't depend on plan design selection
        qry = self._qry_insert_selection_benefit_duration(plan, t=self.t)
        res = db.session.execute(qry)
        STATS["benefit_durations"] = res.rowcount

    def _create_provisions(self, plan: Model_SelectionPlan, *args, **kwargs):
        """
        Create the selection provisions and factors. This is an insert query of data already in the database.
        This is an INSERT from SELECT query
        """
        qry = self._qry_insert_selection_provision(plan, t=self.t)
        res = db.session.execute(qry)
        STATS = {"provisions": res.rowcount}
        columns = list(res.keys())
        selection_provisions = [
            Model_SelectionProvision(**dict(zip(columns, row)))
            for row in res.fetchall()
        ]

        for selection_provision in selection_provisions:
            config_factor_sets = self.get_config_factors(selection_provision, t=self.t)
            factors = self.get_first_valid_ruleset(
                config_factor_sets, selection_provision, t=self.t
            )
            selection_provision.factors = factors

        return selection_provisions

    def create_default_plan(self, *args, **kwargs):
        """
        Main method for creating a default plan.
        This creates the plan, coverages, benefits, benefit durations, provisions, and factors.

        All data is created without commit.
        """
        plan = self._create_plan(self.payload)
        db.session.add(plan)
        db.session.flush()

        self._create_rating_mappers(plan)
        self._create_age_bands(plan)
        self._create_coverage_benefits(plan)
        self._create_provisions(plan)
        return self.schema.dump(plan)

    def grant_plan(self, plan_id, *args, **kwargs):
        schema = Schema_GrantPlanACL()
        validated_data = schema.load(self.payload)
        user = get_user()
        plan, with_grant_option = self.query_plan_acl_with_grant_option(
            plan_id, user.get("user_name", None)
        )
        if not plan:
            raise ValueError("Cannot find plan")
        if with_grant_option is False:
            raise NotAuthorizedError(
                "User does not have permissions to grant permissions to other users"
            )
        plan_acl = Model_SelectionPlan_ACL(
            selection_plan_id=plan.selection_plan_id,
            user_name=validated_data["user_name"],
            with_grant_option=validated_data.get("with_grant_option", False),
        )
        db.session.add(plan_acl)
        db.session.flush()
        return self.schema.dump(plan)

    def revoke_plan(self, plan_id, *args, **kwargs):
        schema = Schema_RevokePlanACL()
        validated_data = schema.load(self.payload)
        user = get_user()
        plan, with_grant_option = self.query_plan_acl_with_grant_option(
            plan_id, user.get("user_name", None)
        )
        if not plan:
            raise ValueError("Cannot find plan")
        if with_grant_option is False:
            raise NotAuthorizedError(
                "User does not have permissions to revoke other users' permissions"
            )
        db.session.query(Model_SelectionPlan_ACL).filter(
            Model_SelectionPlan_ACL.selection_plan_id == plan.selection_plan_id,
            Model_SelectionPlan_ACL.user_name == validated_data["user_name"],
        ).delete()
        db.session.flush()
        return {"msg": "Successfully revoked permissions"}
