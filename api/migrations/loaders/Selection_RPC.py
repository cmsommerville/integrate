import requests
from typing import List, Tuple
import datetime
from marshmallow import ValidationError
from sqlalchemy.sql import desc, and_
from sqlalchemy.exc import NoResultFound
from app.extensions import db
from app.shared.utils import get_db_current_timestamp
from app.shared.errors import AppValidationError, RowNotFoundError
from app.backend.models import (
    Model_ConfigProductVariation,
    Model_ConfigProductVariationState,
    Model_ConfigProduct,
    Model_ConfigBenefit,
    Model_ConfigBenefitAuth,
    Model_ConfigBenefitAuth_ACL,
    Model_ConfigBenefitVariationState,
    Model_ConfigBenefitDurationSet,
    Model_ConfigBenefitDurationDetail,
    Model_ConfigProvision,
    Model_ConfigProvisionState,
    Model_DefaultProductRatingMapperSet,
    Model_ConfigRatingMapperDetail,
    Model_ConfigRatingMapperSet,
    Model_ConfigRatingMapperCollection,
    Model_ConfigDropdownDetail,
    Model_ConfigDropdownSet,
    Model_RefDataTypes,
    Model_SelectionPlan,
    Model_SelectionBenefit,
    Model_SelectionBenefitDuration,
    Model_SelectionProvision,
    Model_SelectionRatingMapperSet,
)

from app.backend.resources.Selection_RPC_Plan import Selection_RPC_Plan
from app.backend.resources.Selection_RPC_AgeBands import Selection_RPC_AgeBands
from app.backend.resources.Selection_RPC_Benefit import Selection_RPC_Benefit
from app.backend.resources.Selection_RPC_BenefitDuration import (
    Selection_RPC_BenefitDuration,
)
from app.backend.resources.Selection_RPC_ProductVariation import (
    Selection_RPC_ProductVariation,
)
from app.backend.resources.Selection_RPC_Provision import Selection_RPC_Provision
from app.backend.resources.Selection_RPC_RatingMapper import Selection_RPC_RatingMapper


class TestSelectionRPC_CreateDefaultPlan:
    def __init__(self, *args, **kwargs):
        pass

    def test_create_default_plan(self):
        t = get_db_current_timestamp()
        PRODUCT_VARIATION_CODE = "base"
        SITUS_STATE = "AL"
        EFFECTIVE_DATE = datetime.date(2024, 4, 1)
        self.product = Model_ConfigProduct.find_one_by_attr(
            {"config_product_code": "AC70000"}
        )
        variation_state = Model_ConfigProductVariationState.find_one_for_selection_plan(
            self.product.config_product_id,
            PRODUCT_VARIATION_CODE,
            SITUS_STATE,
            EFFECTIVE_DATE,
        )
        payload = {
            "config_product_variation_state_id": variation_state.config_product_variation_state_id,
            "situs_state_id": variation_state.state_id,
            "selection_plan_effective_date": str(EFFECTIVE_DATE),
        }
        instance = Selection_RPC_Plan(payload, t=t)
        response = instance.create_default_plan()

        self.plan_data = response
        self.plan = (
            db.session.query(Model_SelectionPlan)
            .filter_by(selection_plan_id=response.get("selection_plan_id"))
            .one()
        )

        assert response is not None
        assert response.get("selection_plan_id") is not None
        assert (
            response.get("config_product_variation_state_id")
            == variation_state.config_product_variation_state_id
        )
        assert response.get("situs_state_id") == variation_state.state_id
        assert self.plan.plan_as_of_dts < self.plan.row_eff_dts

    def execute(self):
        self.test_create_default_plan()

    @classmethod
    def rollback(cls):
        db.session.rollback()


class TestSelectionRPC_Benefit(TestSelectionRPC_CreateDefaultPlan):
    def test_update_benefit_amount(self):
        BENEFIT_CODE = "bnft100"
        BNFT = Model_ConfigBenefit
        BVS = Model_ConfigBenefitVariationState
        SB = Model_SelectionBenefit

        config_benefit_variation_state_id, config_benefit = (
            db.session.query(BVS.config_benefit_variation_state_id, BNFT)
            .join(BNFT, BVS.config_benefit_id == BNFT.config_benefit_id)
            .join(
                SB,
                SB.config_benefit_variation_state_id
                == BVS.config_benefit_variation_state_id,
            )
            .filter(
                SB.selection_plan_id == self.plan.selection_plan_id,
                BNFT.config_benefit_code == BENEFIT_CODE,
                BNFT.config_product_id == self.product.config_product_id,
                BVS.state_id == self.plan.situs_state_id,
                BVS.config_benefit_variation_state_effective_date
                <= self.plan.selection_plan_effective_date,
                BVS.config_benefit_variation_state_expiration_date
                >= self.plan.selection_plan_effective_date,
            )
            .one()
        )

        selection_benefit = Model_SelectionBenefit.find_one_by_attr(
            {
                "config_benefit_variation_state_id": config_benefit_variation_state_id,
                "selection_plan_id": self.plan.selection_plan_id,
            }
        )

        new_benefit_amount = (
            0.5
            * (float(config_benefit.max_value) + float(config_benefit.min_value))
            // float(config_benefit.step_value)
        ) * float(config_benefit.step_value)
        payload = {
            "selection_benefit_id": selection_benefit.selection_benefit_id,
            "selection_value": new_benefit_amount,
            "version_id": selection_benefit.version_id,
        }
        response = Selection_RPC_Benefit(
            payload, plan_id=self.plan.selection_plan_id
        ).upsert_benefit()
        assert response is not None
        assert response.get("selection_value") == new_benefit_amount

    def test_delete_selected_benefit(self):
        BENEFIT_CODE = "bnft200"
        BNFT = Model_ConfigBenefit
        BVS = Model_ConfigBenefitVariationState
        SB = Model_SelectionBenefit

        qry = (
            db.session.query(SB)
            .join(
                BVS,
                BVS.config_benefit_variation_state_id
                == SB.config_benefit_variation_state_id,
            )
            .join(BNFT, BNFT.config_benefit_id == BVS.config_benefit_id)
            .filter(
                SB.selection_plan_id == self.plan.selection_plan_id,
                BNFT.config_benefit_code == BENEFIT_CODE,
            )
        )
        selection_benefit = qry.one()
        payload = {
            "selection_benefit_id": selection_benefit.selection_benefit_id,
            "version_id": selection_benefit.version_id,
        }
        instance = Selection_RPC_Benefit(payload, plan_id=self.plan.selection_plan_id)
        response = instance.remove_benefit()

        assert response is None
        check_selection_benefit = qry.one_or_none()
        assert check_selection_benefit is None

    def test_update_benefit_amount__fail_temporal_query(self):
        BENEFIT_CODE = "bnft252"
        NEW_BENEFIT_AMOUNT = 9999900

        new_auth = self._add_config_benefit_auth_post_hoc(
            BENEFIT_CODE, NEW_BENEFIT_AMOUNT, NEW_BENEFIT_AMOUNT + 100
        )

        BNFT = Model_ConfigBenefit
        BVS = Model_ConfigBenefitVariationState
        SB = Model_SelectionBenefit

        config_benefit_variation_state_id, config_benefit = (
            db.session.query(BVS.config_benefit_variation_state_id, BNFT)
            .join(BNFT, BVS.config_benefit_id == BNFT.config_benefit_id)
            .join(
                SB,
                SB.config_benefit_variation_state_id
                == BVS.config_benefit_variation_state_id,
            )
            .filter(
                SB.selection_plan_id == self.plan.selection_plan_id,
                BNFT.config_benefit_code == BENEFIT_CODE,
                BNFT.config_product_id == self.product.config_product_id,
                BVS.state_id == self.plan.situs_state_id,
                BVS.config_benefit_variation_state_effective_date
                <= self.plan.selection_plan_effective_date,
                BVS.config_benefit_variation_state_expiration_date
                >= self.plan.selection_plan_effective_date,
            )
            .one()
        )

        selection_benefit = Model_SelectionBenefit.find_one_by_attr(
            {
                "config_benefit_variation_state_id": config_benefit_variation_state_id,
                "selection_plan_id": self.plan.selection_plan_id,
            }
        )

        try:
            payload = {
                "selection_benefit_id": selection_benefit.selection_benefit_id,
                "selection_value": NEW_BENEFIT_AMOUNT,
                "version_id": selection_benefit.version_id,
            }
            instance = Selection_RPC_Benefit(
                payload, plan_id=self.plan.selection_plan_id
            )
            response = instance.upsert_benefit()
        except AppValidationError:
            pass
        except Exception:
            raise
        else:
            raise AssertionError("You should not be here!")

    def test_insert_benefit__fail_selection_value_validation(self):
        BENEFIT_CODE = "bnft200"
        BNFT = Model_ConfigBenefit
        BVS = Model_ConfigBenefitVariationState

        config_benefit_variation_state, config_benefit = (
            db.session.query(BVS, BNFT)
            .join(BNFT, BVS.config_benefit_id == BNFT.config_benefit_id)
            .filter(
                BNFT.config_benefit_code == BENEFIT_CODE,
                BNFT.config_product_id == self.product.config_product_id,
                BVS.state_id == self.plan.situs_state_id,
                BVS.config_product_variation_state_id
                == self.plan.config_product_variation_state_id,
                BVS.config_benefit_variation_state_effective_date
                <= self.plan.selection_plan_effective_date,
                BVS.config_benefit_variation_state_expiration_date
                >= self.plan.selection_plan_effective_date,
            )
            .one()
        )

        # fail min_value validation
        new_benefit_amount = float(config_benefit.min_value) - 1
        payload = {
            "config_benefit_variation_state_id": config_benefit_variation_state.config_benefit_variation_state_id,
            "selection_value": new_benefit_amount,
        }
        try:
            instance = Selection_RPC_Benefit(
                payload, plan_id=self.plan.selection_plan_id
            )
            _ = instance.upsert_benefit()
        except AppValidationError as e:
            assert str(e) == "Selection must be greater than minimum permissible value"
        else:
            raise AssertionError("Expected AppValidationError")

        # fail step_value validation
        new_benefit_amount = (
            0.5
            * (float(config_benefit.max_value) + float(config_benefit.min_value))
            // float(config_benefit.step_value)
        ) * float(config_benefit.step_value) - 0.01

        payload = {
            "config_benefit_variation_state_id": config_benefit_variation_state.config_benefit_variation_state_id,
            "selection_value": new_benefit_amount,
        }
        try:
            instance = Selection_RPC_Benefit(
                payload, plan_id=self.plan.selection_plan_id
            )
            _ = instance.upsert_benefit()
        except AppValidationError as e:
            assert (
                str(e) == "Selection must be a multiple of the permissible step value"
            )
        else:
            raise AssertionError("Expected AppValidationError")

        # fail max_value validation
        new_benefit_amount = float(config_benefit.max_value) + 1
        payload = {
            "config_benefit_variation_state_id": config_benefit_variation_state.config_benefit_variation_state_id,
            "selection_value": new_benefit_amount,
        }
        try:
            instance = Selection_RPC_Benefit(
                payload, plan_id=self.plan.selection_plan_id
            )
            _ = instance.upsert_benefit()
        except AppValidationError as e:
            assert str(e) == "Selection must be less than maximum permissible value"
        else:
            raise AssertionError("Expected AppValidationError")

    def test_insert_benefit__pass_selection_value_validation(self):
        BENEFIT_CODE = "bnft200"
        self._add_config_benefit_durations_post_hoc(BENEFIT_CODE)

        BNFT = Model_ConfigBenefit
        BVS = Model_ConfigBenefitVariationState

        config_benefit_variation_state, config_benefit = (
            db.session.query(BVS, BNFT)
            .join(BNFT, BVS.config_benefit_id == BNFT.config_benefit_id)
            .filter(
                BNFT.config_benefit_code == BENEFIT_CODE,
                BNFT.config_product_id == self.product.config_product_id,
                BVS.state_id == self.plan.situs_state_id,
                BVS.config_product_variation_state_id
                == self.plan.config_product_variation_state_id,
                BVS.config_benefit_variation_state_effective_date
                <= self.plan.selection_plan_effective_date,
                BVS.config_benefit_variation_state_expiration_date
                >= self.plan.selection_plan_effective_date,
            )
            .one()
        )

        new_benefit_amount = (
            0.5
            * (float(config_benefit.max_value) + float(config_benefit.min_value))
            // float(config_benefit.step_value)
        ) * float(config_benefit.step_value)

        payload = {
            "config_benefit_variation_state_id": config_benefit_variation_state.config_benefit_variation_state_id,
            "selection_value": new_benefit_amount,
        }
        instance = Selection_RPC_Benefit(payload, plan_id=self.plan.selection_plan_id)
        response = instance.upsert_benefit()
        assert response is not None
        assert response.get("selection_value") == new_benefit_amount
        assert len(response.get("duration_sets")) == 0

    def _add_config_benefit_auth_post_hoc(self, benefit_code, min_value, max_value):
        """
        Add benefit auth with highest priority to benefit after plan creation.
        The plan should not pick up this up, if the temporal queries are working correctly.
        """
        config_benefit = Model_ConfigBenefit.find_one_by_attr(
            {"config_benefit_code": benefit_code}
        )

        new_auth = Model_ConfigBenefitAuth(
            config_benefit_id=config_benefit.config_benefit_id,
            priority=10000,
            min_value=min_value,
            max_value=max_value,
            step_value=1,
            default_value=min_value,
            acl=[
                Model_ConfigBenefitAuth_ACL(auth_role_code="uw800"),
                Model_ConfigBenefitAuth_ACL(auth_role_code="uw900"),
                Model_ConfigBenefitAuth_ACL(auth_role_code="uw1000"),
            ],
        )

        db.session.add(new_auth)
        db.session.flush()
        return new_auth

    def _add_config_benefit_durations_post_hoc(self, benefit_code):
        """
        Add benefit durations to benefit 200 after plan creation.
        The plan should not pick up these benefit durations as a requirement,
        if the temporal queries are working correctly.
        """
        config_benefit = Model_ConfigBenefit.find_one_by_attr(
            {"config_benefit_code": benefit_code}
        )
        duration_details = [
            Model_ConfigBenefitDurationDetail(
                config_benefit_duration_detail_code=f"temporal_test_{benefit_code}_{i}",
                config_benefit_duration_detail_label=f"Temporal Test {benefit_code} - {i}",
                config_benefit_duration_factor=0.8 + 0.1 * i,
                is_restricted=False,
            )
            for i in range(0, 4)
        ]
        duration_set = Model_ConfigBenefitDurationSet(
            config_benefit_id=config_benefit.config_benefit_id,
            config_benefit_duration_set_code=f"temporal_test_{benefit_code}",
            config_benefit_duration_set_label=f"Temporal Test {benefit_code}",
        )
        duration_set.duration_items.extend(duration_details)
        db.session.add(duration_set)
        db.session.flush()
        return duration_set

    def execute(self):
        self.test_create_default_plan()
        self.test_update_benefit_amount()
        self.test_delete_selected_benefit()
        self.test_update_benefit_amount__fail_temporal_query()
        self.test_insert_benefit__fail_selection_value_validation()
        self.test_insert_benefit__pass_selection_value_validation()


class TestSelectionRPC_BenefitDuration(TestSelectionRPC_CreateDefaultPlan):
    def _add_config_benefit_duration_details_post_hoc(
        self, benefit_duration_set: Model_ConfigBenefitDurationSet
    ):
        """
        Add benefit duration detail options after plan creation.
        The plan should not pick up these benefit durations as a requirement,
        if the temporal queries are working correctly.
        """
        _id = benefit_duration_set.config_benefit_duration_set_id
        duration_details = [
            Model_ConfigBenefitDurationDetail(
                config_benefit_duration_set_id=benefit_duration_set.config_benefit_duration_set_id,
                config_benefit_duration_detail_code=f"tt_{benefit_duration_set.config_benefit_duration_set_code}_{i}",
                config_benefit_duration_detail_label=f"Temporal Test {benefit_duration_set.config_benefit_duration_set_code} - {i}",
                config_benefit_duration_factor=0.8 + 0.1 * i,
                is_restricted=False,
            )
            for i in range(0, 4)
        ]
        db.session.add_all(duration_details)
        db.session.flush()
        db.session.refresh(benefit_duration_set)
        return benefit_duration_set

    def test_update_benefit_duration(self, *args, **kwargs):
        """
        Choose a new benefit duration detail for the first benefit duration in the plan.
        """
        CBD = Model_ConfigBenefitDurationDetail
        SBD = Model_SelectionBenefitDuration
        SB = Model_SelectionBenefit
        first_selection_benefit_duration = (
            db.session.query(SBD)
            .join(SB, SB.selection_benefit_id == SBD.selection_benefit_id)
            .filter(SB.selection_plan_id == self.plan.selection_plan_id)
            .first()
        )

        new_config_benefit_duration_detail = (
            db.session.query(CBD)
            .filter(
                CBD.config_benefit_duration_set_id
                == first_selection_benefit_duration.config_benefit_duration_set_id,
                CBD.config_benefit_duration_detail_id
                != first_selection_benefit_duration.config_benefit_duration_detail_id,
            )
            .order_by(desc(CBD.config_benefit_duration_detail_id))
            .first()
        )

        payload = {
            "selection_benefit_duration_id": first_selection_benefit_duration.selection_benefit_duration_id,
            "config_benefit_duration_detail_id": new_config_benefit_duration_detail.config_benefit_duration_detail_id,
            "version_id": first_selection_benefit_duration.version_id,
        }
        instance = Selection_RPC_BenefitDuration(
            payload, plan_id=self.plan.selection_plan_id
        )
        response = instance.update_benefit_duration()
        assert response is not None
        assert (
            response.get("config_benefit_duration_detail_id")
            == new_config_benefit_duration_detail.config_benefit_duration_detail_id
        )

    def test_update_benefit_duration__fail_temporal_query(self, *args, **kwargs):
        """
        Add new duration details to an existing benefit duration set post-hoc.
        The plan should not be able to select these new duration details.
        This test should throw a NoResultFound error.
        """
        SBD = Model_SelectionBenefitDuration
        SB = Model_SelectionBenefit
        BDS = Model_ConfigBenefitDurationSet

        # get a benefit code for something that exists in the selected benefit durations
        selection_benefit_duration, benefit_duration_set = (
            db.session.query(SBD, BDS)
            .select_from(SBD)
            .join(SB, SBD.selection_benefit_id == SB.selection_benefit_id)
            .join(
                BDS,
                SBD.config_benefit_duration_set_id
                == BDS.config_benefit_duration_set_id,
            )
            .filter(SB.selection_plan_id == self.plan.selection_plan_id)
            .order_by(desc(SBD.selection_benefit_duration_id))
            .first()
        )

        # update the benefit durations post-hoc
        new_duration_set = self._add_config_benefit_duration_details_post_hoc(
            benefit_duration_set
        )
        new_duration_detail = next(
            (
                dd
                for dd in new_duration_set.duration_items
                if dd.config_benefit_duration_detail_code.startswith("tt_")
            ),
            None,
        )

        payload = {
            "selection_benefit_duration_id": selection_benefit_duration.selection_benefit_duration_id,
            "config_benefit_duration_detail_id": new_duration_detail.config_benefit_duration_detail_id,
            "version_id": selection_benefit_duration.version_id,
        }
        try:
            instance = Selection_RPC_BenefitDuration(
                payload, plan_id=self.plan.selection_plan_id
            )
            _ = instance.update_benefit_duration()
        except NoResultFound:
            # this is where we expect the error to be raised
            # the update_benefit_duration method shouldn't be able to find the new duration detail record
            # it uses a .one() fetch method, which will error with this error type and message
            pass
        except Exception as e:
            raise e

    def execute(self):
        self.test_create_default_plan()
        self.test_update_benefit_duration()
        self.test_update_benefit_duration__fail_temporal_query()


class TestSelectionRPC_Provision(TestSelectionRPC_CreateDefaultPlan):
    def _get_selection_provision_by_data_type(self, data_type_code: str):
        PRV = Model_ConfigProvision
        PS = Model_ConfigProvisionState
        SP = Model_SelectionProvision
        DT = Model_RefDataTypes

        return (
            db.session.query(SP)
            .select_from(SP)
            .join(PS, PS.config_provision_state_id == SP.config_provision_state_id)
            .join(PRV, PRV.config_provision_id == PS.config_provision_id)
            .join(DT, DT.ref_id == PRV.config_provision_data_type_id)
            .filter(
                SP.selection_plan_id == self.plan.selection_plan_id,
                DT.ref_attr_code == data_type_code,
            )
            .order_by(desc(SP.selection_provision_id))
            .first()
        )

    def _add_config_dropdown_options_post_hoc(self, config_provision_state_id: int):
        DDS = Model_ConfigDropdownSet
        PROV = Model_ConfigProvision
        PS = Model_ConfigProvisionState

        dropdown_set = (
            db.session.query(DDS)
            .select_from(DDS)
            .join(PROV, PROV.config_dropdown_set_id == DDS.config_dropdown_set_id)
            .join(PS, PS.config_provision_id == PROV.config_provision_id)
            .filter(PS.config_provision_state_id == config_provision_state_id)
            .one()
        )

        new_dropdown_detail = Model_ConfigDropdownDetail(
            config_dropdown_set_id=dropdown_set.config_dropdown_set_id,
            config_dropdown_detail_code="tt_001",
            config_dropdown_detail_label="Temporal Test 001",
            is_restricted=False,
        )
        db.session.add(new_dropdown_detail)
        db.session.flush()
        return new_dropdown_detail

    def test_update_provision(self):
        """
        Test happy path updating a selection provision numeric selection.
        """

        selection_provision = self._get_selection_provision_by_data_type("number")

        NEW_SELECTION_VALUE = (
            str(2 * float(selection_provision.selection_value))
            if selection_provision.selection_value is not None
            else "4000"
        )
        payload = {
            "selection_provision_id": selection_provision.selection_provision_id,
            "selection_value": NEW_SELECTION_VALUE,
            "version_id": selection_provision.version_id,
        }
        response = Selection_RPC_Provision(
            payload, plan_id=self.plan.selection_plan_id
        ).update_provision()
        assert response is not None
        assert response.get("selection_value") == NEW_SELECTION_VALUE

    def test_update_provision__fail_arbitrary_selection(self):
        """
        Validate that the user cannot pass arbitrary string selections.
        The user is required to select from dropdown options for string data types.
        """
        selection_provision = self._get_selection_provision_by_data_type("string")

        payload = {
            "selection_provision_id": selection_provision.selection_provision_id,
            "version_id": selection_provision.version_id,
            "selection_value": "lkjasdfo8h",
        }
        try:
            instance = Selection_RPC_Provision(
                payload, plan_id=self.plan.selection_plan_id
            )
            _ = instance.update_provision()
        except NoResultFound:
            pass
        except Exception as e:
            raise e

    def test_update_provision__fail_temporal_query(self):
        """
        Validate that the temporal query is working correctly.
        This should prohibit adding a new dropdown option after plan creation, then selecting it.
        """
        selection_provision = self._get_selection_provision_by_data_type("string")

        # add new dropdown options post-hoc
        new_dropdown_detail = self._add_config_dropdown_options_post_hoc(
            selection_provision.config_provision_state_id
        )
        payload = {
            "selection_provision_id": selection_provision.selection_provision_id,
            "version_id": selection_provision.version_id,
            "selection_value": new_dropdown_detail.config_dropdown_detail_code,
        }
        try:
            instance = Selection_RPC_Provision(
                payload, plan_id=self.plan.selection_plan_id
            )
            _ = instance.update_provision()
        except NoResultFound:
            pass
        except Exception as e:
            raise e

    def execute(self):
        self.test_create_default_plan()
        self.test_update_provision()
        self.test_update_provision__fail_temporal_query()
        self.test_update_provision__fail_arbitrary_selection()


class TestSelectionRPC_RatingMapper(TestSelectionRPC_CreateDefaultPlan):
    def _get_first_unselected_rating_mapper_set(cls, plan_id):
        """
        Fetch one rating mapper set that has not been selected for the plan.
        """
        RMS = Model_ConfigRatingMapperSet
        DRMS = Model_DefaultProductRatingMapperSet
        PLAN = Model_SelectionPlan
        SRMS = Model_SelectionRatingMapperSet

        res = (
            db.session.query(RMS)
            .select_from(RMS)
            .join(
                DRMS,
                DRMS.config_rating_mapper_collection_id
                == RMS.config_rating_mapper_collection_id,
            )
            .join(PLAN, PLAN.config_product_id == DRMS.config_product_id)
            .join(
                SRMS,
                and_(
                    SRMS.config_rating_mapper_set_id == RMS.config_rating_mapper_set_id,
                    PLAN.selection_plan_id == SRMS.selection_plan_id,
                ),
                isouter=True,
            )
            .filter(
                PLAN.selection_plan_id == plan_id,
                SRMS.selection_rating_mapper_set_id == None,
            )
            .first()
        )
        return res

    @classmethod
    def _create_arbitrary_mapper_detail(cls, attributes):
        if len(attributes) <= 1:
            raise ValueError(
                "There must be more than one attribute in the rating mapper set"
            )

        splitter_index = len(attributes) // 2
        return [
            Model_ConfigRatingMapperDetail(
                rate_table_attribute_detail_id=attr.config_attr_detail_id,
                output_attribute_detail_id=attributes[
                    splitter_index
                ].config_attr_detail_id,
                weight=1,
            )
            for attr in attributes[:splitter_index]
        ]

    def _add_config_rating_mapper_post_hoc(self, plan: Model_SelectionPlan):
        """
        Add rating mapper set post-hoc.
        Use to validate that pre-existing plans cannot pick up these additions
        """

        RMC = Model_ConfigRatingMapperCollection
        DRMS = Model_DefaultProductRatingMapperSet
        PLAN = Model_SelectionPlan

        selection_rating_mapper_set_type, first_rating_mapper_collection = (
            db.session.query(DRMS.selection_rating_mapper_set_type, RMC)
            .select_from(RMC)
            .join(
                DRMS,
                DRMS.config_rating_mapper_collection_id
                == RMC.config_rating_mapper_collection_id,
            )
            .join(PLAN, PLAN.config_product_id == DRMS.config_product_id)
            .filter(
                PLAN.selection_plan_id == plan.selection_plan_id,
            )
            .order_by(DRMS.config_rating_mapper_collection_id)
        ).first()

        attributes = first_rating_mapper_collection.attribute_set.attributes

        new_rating_mapper_set = Model_ConfigRatingMapperSet(
            config_rating_mapper_set_label="tt_001",
            config_rating_mapper_collection_id=first_rating_mapper_collection.config_rating_mapper_collection_id,
            is_composite=False,
            is_employer_paid=False,
            mapper_details=self._create_arbitrary_mapper_detail(attributes),
        )
        db.session.add(new_rating_mapper_set)
        db.session.flush()
        return selection_rating_mapper_set_type, new_rating_mapper_set

    def test_update_rating_mapper(self):
        selection_rating_mappers = self.plan.rating_mapper_sets
        new_rating_mapper_set = self._get_first_unselected_rating_mapper_set(
            self.plan.selection_plan_id
        )
        if new_rating_mapper_set is None:
            # if in here, that means that there are no other rating mappers to select from
            # test passes automatically
            return

        update_rating_mapper_set = next(
            (
                rms
                for rms in selection_rating_mappers
                if rms.config_rating_mapper_set_id
                == new_rating_mapper_set.config_rating_mapper_set_id
            ),
            None,
        )
        if update_rating_mapper_set is None:
            raise RowNotFoundError("Cannot find rating mapper set to update.")

        payload = {
            "selection_rating_mapper_set_type": update_rating_mapper_set.selection_rating_mapper_set_type,
            "config_rating_mapper_set_id": new_rating_mapper_set.config_rating_mapper_set_id,
            "has_custom_weights": False,
        }
        instance = Selection_RPC_RatingMapper(
            payload=payload, plan_id=self.plan.selection_plan_id
        )
        response = instance.update_rating_mapper()

        assert response is not None
        assert (
            response.get("config_rating_mapper_set_id")
            == new_rating_mapper_set.config_rating_mapper_set_id
        )

    def test_update_rating_mapper__fail_temporal_query(self):
        """
        This test adds a new rating mapper set and tries to apply it to an existing plan.
        This should fail because the plan should not be able to see the new rating mapper set.
        """
        selection_rating_mapper_set_type, new_rating_mapper_set = (
            self._add_config_rating_mapper_post_hoc(self.plan)
        )

        payload = {
            "selection_rating_mapper_set_type": selection_rating_mapper_set_type,
            "config_rating_mapper_set_id": new_rating_mapper_set.config_rating_mapper_set_id,
            "has_custom_weights": False,
        }
        try:
            instance = Selection_RPC_RatingMapper(
                payload=payload, plan_id=self.plan.selection_plan_id
            )
            _ = instance.update_rating_mapper()
        except (RowNotFoundError, NoResultFound):
            pass
        except Exception:
            raise

    def execute(self):
        self.test_create_default_plan()
        self.test_update_rating_mapper()
        self.test_update_rating_mapper__fail_temporal_query()


class TestSelectionRPC_AgeBands(TestSelectionRPC_CreateDefaultPlan):
    @staticmethod
    def _create_age_band_details(arr: List[Tuple[int, int]]):
        return [
            dict(
                age_band_lower=lower,
                age_band_upper=upper,
            )
            for lower, upper in arr
        ]

    def test_update_age_band__pass_validation(self):
        payload = self._create_age_band_details(
            [
                (0, 17),
                (18, 34),
                (35, 49),
                (50, 64),
                (65, 100),
            ]
        )

        instance = Selection_RPC_AgeBands(payload, plan_id=self.plan.selection_plan_id)
        response = instance.update_age_bands()
        assert len(response) == 5
        assert all([ab["selection_age_band_id"] is not None for ab in response])

    def test_update_age_band__fail_validation(self, age_bands: List[Tuple[int, int]]):
        payload = self._create_age_band_details(age_bands)
        try:
            instance = Selection_RPC_AgeBands(
                payload, plan_id=self.plan.selection_plan_id
            )
            instance.update_age_bands()
        except ValidationError:
            pass
        except Exception as e:
            raise e

    def execute(self):
        self.test_create_default_plan()
        self.test_update_age_band__pass_validation()
        self.test_update_age_band__fail_validation([(0, 34), (35, 49), (42, 99)])
        self.test_update_age_band__fail_validation([])
        self.test_update_age_band__fail_validation([(-1, 17), (18, 34), (35, 99)])
        self.test_update_age_band__fail_validation([(0, -1)])


class TestSelectionRPC_ProductVariation(TestSelectionRPC_CreateDefaultPlan):
    @classmethod
    def _get_available_product_variations(cls, plan: Model_SelectionPlan):
        """
        List all the other product variations that can be selected for this plan.
        """
        return (
            db.session.query(Model_ConfigProductVariationState)
            .join(
                Model_ConfigProductVariation,
                Model_ConfigProductVariationState.config_product_variation_id
                == Model_ConfigProductVariation.config_product_variation_id,
            )
            .join(
                Model_SelectionPlan,
                and_(
                    Model_ConfigProductVariation.config_product_id
                    == Model_SelectionPlan.config_product_id,
                    Model_ConfigProductVariationState.state_id
                    == Model_SelectionPlan.situs_state_id,
                ),
            )
            .filter(
                Model_SelectionPlan.selection_plan_id == plan.selection_plan_id,
                Model_SelectionPlan.config_product_variation_state_id
                != Model_ConfigProductVariationState.config_product_variation_state_id,
            )
            .all()
        )

    @classmethod
    def _get_single_invalid_product_variation(cls, plan: Model_SelectionPlan):
        """
        Get another product variation from a different product.
        """
        return (
            db.session.query(Model_ConfigProductVariation)
            .filter(
                Model_ConfigProductVariation.config_product_id
                != plan.config_product_id,
            )
            .first()
        )

    def test_update_product_variation(self):
        variations = self._get_available_product_variations(self.plan)
        if not variations:
            return
        payload = {
            "config_product_variation_id": variations[0].config_product_variation_id,
        }
        instance = Selection_RPC_ProductVariation(payload, self.plan.selection_plan_id)
        response = instance.update_product_variation()
        assert response is not None
        assert (
            response["config_product_variation_state_id"]
            == variations[0].config_product_variation_state_id
        )

    def test_update_product_variation__fail_temporal_query(self):
        """
        The plan should not be able to see new product variations added post-hoc.
        """
        variation = Model_ConfigProductVariation(
            config_product_id=self.plan.config_product_id,
            config_product_variation_code="test_variation",
            config_product_variation_label="Test Variation",
        )
        variation_state = Model_ConfigProductVariationState(
            state_id=self.plan.situs_state_id,
            config_product_variation_state_effective_date=datetime.date(2000, 1, 1),
            config_product_variation_state_expiration_date=datetime.date(9999, 12, 31),
            parent=variation,
        )

        db.session.add(variation_state)
        db.session.flush()

        payload = {
            "config_product_variation_id": variation.config_product_variation_id,
        }

        try:
            instance = Selection_RPC_ProductVariation(
                payload, self.plan.selection_plan_id
            )
            _ = instance.update_product_variation()
        except (NoResultFound, RowNotFoundError):
            pass
        except Exception as e:
            raise e

    def test_update_product_variation__fail_invalid_variation(self):
        """
        The plan should not be able to add a product variation belonging to a different product
        """
        variation = self._get_single_invalid_product_variation(self.plan)
        if variation is None:
            return
        payload = {
            "config_product_variation_id": variation.config_product_variation_id,
        }
        try:
            instance = Selection_RPC_ProductVariation(
                payload, self.plan.selection_plan_id
            )
            _ = instance.update_product_variation()
        except (NoResultFound, RowNotFoundError):
            pass
        except Exception:
            raise

    def test_update_product_variation__fail_nonexistent_variation(self):
        """
        The plan should not be able to add a product variation that doesn't exist.
        """
        payload = {
            "config_product_variation_id": -32,
        }
        try:
            instance = Selection_RPC_ProductVariation(
                payload, self.plan.selection_plan_id
            )
            _ = instance.update_product_variation()
        except (NoResultFound, RowNotFoundError):
            pass
        except Exception:
            raise

    def execute(self):
        self.test_create_default_plan()
        self.test_update_product_variation()
        self.test_update_product_variation__fail_nonexistent_variation()
        self.test_update_product_variation__fail_invalid_variation()
        self.test_update_product_variation__fail_temporal_query()


class TestSelectionRPC_Plan(TestSelectionRPC_CreateDefaultPlan):
    SUPERUSER = {"user_name": "superuser", "password": "hello_world"}
    USER1 = {
        "user_name": "csommerville",
        "password": "hello_world",
    }

    def test_grant_plan(self, user_name, with_grant_option=False):
        payload = {"user_name": user_name, "with_grant_option": with_grant_option}
        instance = Selection_RPC_Plan(payload)
        response = instance.grant_plan(plan_id=self.plan.selection_plan_id)
        assert response is not None

    def test_revoke_plan(self, user_name):
        payload = {"user_name": user_name}
        instance = Selection_RPC_Plan(payload)
        response = instance.revoke_plan(plan_id=self.plan.selection_plan_id)
        assert response is not None
        assert "Successfully revoked permissions" in response.get("msg")

    def execute(self):
        self.test_create_default_plan()
        self.test_grant_plan(self.USER1["user_name"], with_grant_option=True)
        self.test_revoke_plan(self.USER1["user_name"])


class TestSelectionRPC_PlanDesign(TestSelectionRPC_CreateDefaultPlan):
    def test_update_product_plan_design(self):
        pass

    def test_upsert_coverage_plan_design(self):
        pass

    def test_remove_coverage_plan_design(self):
        pass

    def execute(self):
        self.test_create_default_plan()
        self.test_update_product_plan_design()
        self.test_upsert_coverage_plan_design()
        self.test_remove_coverage_plan_design()
