from typing import Dict, List
from app.extensions import db
from app.shared.utils import system_temporal_hint
from ..models import (
    Model_ConfigFactor,
    Model_SelectionFactor,
    Model_ConfigFactorSet,
    Model_ConfigProvisionState,
    Model_SelectionProvision,
)


class FactorRulesetApplicator:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def config_to_selection_factor(
        config_factor: Model_ConfigFactor, selection_provision_id: int
    ):
        return Model_SelectionFactor(
            selection_provision_id=selection_provision_id,
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
    def get_config_factors(cls, selection_provision: Model_SelectionProvision, t=None):
        FCTR = Model_ConfigFactorSet
        PS = Model_ConfigProvisionState
        SP = Model_SelectionProvision

        qry = (
            db.session.query(FCTR)
            .join(PS, PS.config_provision_id == FCTR.config_provision_id)
            .join(SP, SP.config_provision_state_id == PS.config_provision_state_id)
            .filter(
                SP.selection_provision_id == selection_provision.selection_provision_id
            )
        )
        if t is not None:
            qry = qry.with_hint(FCTR, system_temporal_hint(t)).with_hint(
                PS, system_temporal_hint(t)
            )

        return qry.all()

    @classmethod
    def get_first_valid_ruleset(
        cls,
        config_factor_sets: List[Model_ConfigFactorSet],
        selection_provision: Model_SelectionProvision,
        t=None,
    ):
        # find first ruleset
        validated_factor_ruleset = next(
            (
                ruleset
                for ruleset in config_factor_sets
                if ruleset.apply_ruleset(selection_provision, t=t)
            ),
            None,
        )

        if validated_factor_ruleset is None:
            return []

        return [
            cls.config_to_selection_factor(
                val, selection_provision.selection_provision_id
            )
            for val in validated_factor_ruleset.get_factor_values(t=t)
        ]
