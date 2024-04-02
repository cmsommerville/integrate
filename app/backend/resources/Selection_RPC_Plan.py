import datetime
from marshmallow import Schema, fields
from app.extensions import db
from app.auth import get_user, NotAuthorizedError
from app.shared.errors import PlanInvalidError
from ..models import (
    Model_ConfigPlanDesignDetail_Benefit,
    Model_ConfigBenefitDurationDetail,
    Model_ConfigBenefitDurationSet,
    Model_ConfigBenefitVariationState,
    Model_ConfigFactor,
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
)
from ..schemas import (
    Schema_SelectionPlan,
    Schema_DefaultProductRatingMapperSet_For_Selection,
    Schema_SelectionRatingMapperSet,
)

WITH_GRANT_OPTION = True


class Schema_GrantPlanACL(Schema):
    user_name = fields.String(required=True)
    with_grant_option = fields.Boolean(default=False)


class Schema_RevokePlanACL(Schema):
    user_name = fields.String(required=True)


class SelectionProvisionMixin:
    @staticmethod
    def config_to_selection_factor(
        config_factor: Model_ConfigFactor,
    ):
        return Model_SelectionFactor(
            config_factor_set_id=config_factor.config_factor_set_id,
            config_factor_id=config_factor.config_factor_id,
            selection_rate_table_age_value=config_factor.rate_table_age_value,
            selection_rating_attr_id1=config_factor.rating_attr_id1,
            selection_rating_attr_id2=config_factor.rating_attr_id2,
            selection_rating_attr_id3=config_factor.rating_attr_id3,
            selection_rating_attr_id4=config_factor.rating_attr_id4,
            selection_rating_attr_id5=config_factor.rating_attr_id5,
            selection_rating_attr_id6=config_factor.rating_attr_id6,
            selection_factor_value=config_factor.factor_value,
        )

    @classmethod
    def get_selection_factors(
        cls,
        config_provision: Model_ConfigProvision,
        selection_provision: Model_SelectionProvision,
    ):
        # find first ruleset
        validated_factor_ruleset = next(
            (
                ruleset
                for ruleset in config_provision.factors
                if ruleset.apply_ruleset(selection_provision)
            ),
            None,
        )

        if validated_factor_ruleset is None:
            return []

        return [
            cls.config_to_selection_factor(val)
            for val in validated_factor_ruleset.factor_values
        ]


class SelectionBenefitMixin:
    @classmethod
    def _default_coverage_benefits__plan_design(
        cls, default_product_plan_design, plan: Model_SelectionPlan
    ):
        """
        Create coverages and benefits based on the default product plan design.
        """
        default_coverage_plan_designs = (
            default_product_plan_design.coverage_plan_designs
        )
        selection_coverages = []
        for cpd in default_coverage_plan_designs:
            coverage = Model_SelectionCoverage(
                selection_plan_id=plan.selection_plan_id,
                config_coverage_id=cpd.config_parent_id,
                config_plan_design_set_id=cpd.config_plan_design_set_id,
            )
            coverage.benefits = cls.load_plan_design_to_selection_benefit(
                cpd.config_plan_design_set_id, plan
            )
            selection_coverages.append(coverage)
        return selection_coverages

    @classmethod
    def _default_coverage_benefits__config_benefit(cls, plan: Model_SelectionPlan):
        quotable_benefits = Model_ConfigBenefitVariationState.find_quotable_benefits(
            plan.config_product_variation_state_id,
            plan.situs_state_id,
            plan.selection_plan_effective_date,
        )

        selection_coverages_dict = {}
        for bvs, bnft, cvg in quotable_benefits:
            if cvg.config_coverage_id not in selection_coverages_dict:
                selection_coverages_dict[cvg.config_coverage_id] = (
                    Model_SelectionCoverage(
                        selection_plan_id=plan.selection_plan_id,
                        config_coverage_id=cvg.config_coverage_id,
                    )
                )
            selection_coverages_dict[cvg.config_coverage_id].benefits.append(
                Model_SelectionBenefit(
                    selection_plan_id=plan.selection_plan_id,
                    config_benefit_variation_state_id=bvs.config_benefit_variation_state_id,
                    selection_value=bnft.default_value,
                )
            )
        return selection_coverages_dict.values()

    @classmethod
    def _qry_plan_design_benefits(
        cls,
        config_plan_design_set_id: int,
        product_variation_state_id: int,
        effective_date: datetime.date,
    ):
        PDB = Model_ConfigPlanDesignDetail_Benefit
        BVS = Model_ConfigBenefitVariationState
        BD = Model_ConfigBenefitDurationSet
        BDD = Model_ConfigBenefitDurationDetail
        qry = (
            db.session.query(
                BVS.config_benefit_variation_state_id,
                PDB.default_value,
                BD.config_benefit_duration_set_id,
                BD.default_config_benefit_duration_detail_id,
                BDD.config_benefit_duration_factor,
            )
            .select_from(PDB)
            .join(BVS, BVS.config_benefit_id == PDB.config_parent_id)
            .join(BD, BD.config_benefit_id == BVS.config_benefit_id, isouter=True)
            .join(
                BDD,
                BD.default_config_benefit_duration_detail_id
                == BDD.config_benefit_duration_detail_id,
                isouter=True,
            )
            .filter(
                PDB.config_plan_design_set_id == config_plan_design_set_id,
                BVS.config_product_variation_state_id == product_variation_state_id,
                BVS.config_benefit_variation_state_effective_date <= effective_date,
                BVS.config_benefit_variation_state_expiration_date >= effective_date,
            )
        )
        return qry.all()

    @classmethod
    def load_plan_design_to_selection_benefit(
        cls,
        config_plan_design_set_id: int,
        plan: Model_SelectionPlan,
    ):
        """
        Set a plan's benefits (which are by benefit variation state ID)
        based on a plan design selection (which are by benefit ID).
        """
        rows = cls._qry_plan_design_benefits(
            config_plan_design_set_id,
            plan.config_product_variation_state_id,
            plan.selection_plan_effective_date,
        )
        objs_dict = {}
        for row in rows:
            (
                config_benefit_variation_state_id,
                default_benefit_value,
                config_benefit_duration_set_id,
                default_config_benefit_duration_detail_id,
                config_benefit_duration_factor,
            ) = row
            bnft_key = (
                plan.selection_plan_id,
                config_benefit_variation_state_id,
                float(default_benefit_value),
            )
            if bnft_key not in objs_dict:
                objs_dict[bnft_key] = Model_SelectionBenefit(
                    selection_plan_id=plan.selection_plan_id,
                    config_benefit_variation_state_id=config_benefit_variation_state_id,
                    selection_value=float(default_benefit_value),
                )

            if config_benefit_duration_set_id is not None:
                objs_dict[bnft_key].duration_sets.append(
                    Model_SelectionBenefitDuration(
                        **{
                            "config_benefit_duration_set_id": config_benefit_duration_set_id,
                            "config_benefit_duration_detail_id": default_config_benefit_duration_detail_id,
                            "selection_factor": float(config_benefit_duration_factor),
                        }
                    )
                )
        return list(objs_dict.values())


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
    SelectionProvisionMixin, SelectionBenefitMixin, SelectionPlanMixin
):
    schema = Schema_SelectionPlan()

    @classmethod
    def create_default_coverage_benefits(
        cls, plan: Model_SelectionPlan, *args, **kwargs
    ):
        default_product_plan_design = (
            plan.config_product_variation_state.default_product_plan_design
        )
        if default_product_plan_design is None:
            return cls._default_coverage_benefits__config_benefit(plan)

        return cls._default_coverage_benefits__plan_design(
            default_product_plan_design, plan
        )

    @classmethod
    def create_default_age_bands(cls, plan: Model_SelectionPlan, *args, **kwargs):
        default_age_band_set = plan.config_product_variation_state.age_band_set
        if default_age_band_set is None:
            return [
                Model_SelectionAgeBand(
                    selection_plan_id=plan.selection_plan_id,
                    age_band_lower=0,
                    age_band_upper=999,
                )
            ]

        return [
            Model_SelectionAgeBand(
                selection_plan_id=plan.selection_plan_id,
                age_band_lower=ab.age_band_lower,
                age_band_upper=ab.age_band_upper,
            )
            for ab in default_age_band_set.age_bands
        ]

    @classmethod
    def create_default_rating_mappers(cls, plan: Model_SelectionPlan, *args, **kwargs):
        schema = Schema_DefaultProductRatingMapperSet_For_Selection(many=True)
        selection_schema = Schema_SelectionRatingMapperSet(many=True)
        objs = Model_DefaultProductRatingMapperSet.find_by_parent(
            plan.config_product_id
        )
        data = schema.dump(objs)
        return selection_schema.load(
            [{**row, "selection_plan_id": plan.selection_plan_id} for row in data]
        )

    @classmethod
    def create_default_provisions(cls, plan: Model_SelectionPlan, *args, **kwargs):
        provision_states = Model_ConfigProvisionState.get_provision_states_by_product(
            plan.config_product_id,
            plan.situs_state_id,
            plan.selection_plan_effective_date,
        )
        selection_provisions = [
            Model_SelectionProvision(
                selection_plan_id=plan.selection_plan_id,
                config_provision_state_id=ps.config_provision_state_id,
                selection_value=ps.parent.default_value,
            )
            for ps in provision_states
        ]
        db.session.add_all(selection_provisions)
        db.session.flush()

        for selection_provision in selection_provisions:
            factors = cls.get_selection_factors(
                selection_provision.config_provision, selection_provision
            )
            selection_provision.factors = factors

        return selection_provisions

    @classmethod
    def create_plan(cls, payload):
        is_plan_valid = Model_ConfigProductVariationState.is_plan_valid(
            payload["config_product_variation_state_id"],
            payload["situs_state_id"],
            payload["selection_plan_effective_date"],
        )
        if is_plan_valid:
            user = get_user()
            default_acl = {
                "user_name": user.get("user_name"),
                "with_grant_option": WITH_GRANT_OPTION,
            }
            return cls.schema.load({**payload, "acl": [default_acl]})
        raise PlanInvalidError(
            "Situs state, product variation, and effective date are incompatible"
        )

    @classmethod
    def create_default_plan(cls, payload, *args, **kwargs):
        try:
            plan = cls.create_plan(payload)
            db.session.add(plan)
            db.session.flush()

            selection_rating_mappers = cls.create_default_rating_mappers(plan)
            db.session.add_all(selection_rating_mappers)

            selection_age_bands = cls.create_default_age_bands(plan)
            db.session.add_all(selection_age_bands)

            selection_coverage_benefits = cls.create_default_coverage_benefits(plan)
            db.session.add_all(selection_coverage_benefits)

            selection_provisions = cls.create_default_provisions(plan)
            db.session.add_all(selection_provisions)

            db.session.commit()
            return cls.schema.dump(plan)
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def grant_plan(cls, payload, plan_id, *args, **kwargs):
        try:
            schema = Schema_GrantPlanACL()
            validated_data = schema.load(payload)
            user = get_user()
            plan, with_grant_option = cls.query_plan_acl_with_grant_option(
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
            db.session.commit()
            return cls.schema.dump(plan)
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def revoke_plan(cls, payload, plan_id, *args, **kwargs):
        try:
            schema = Schema_RevokePlanACL()
            validated_data = schema.load(payload)
            user = get_user()
            plan, with_grant_option = cls.query_plan_acl_with_grant_option(
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
            db.session.commit()
            return {"msg": "Successfully revoked permissions"}
        except Exception as e:
            db.session.rollback()
            raise e
