from app.extensions import db
from app.shared import BaseModel, BaseRowLevelSecurityTable
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from .Selection_Benefit import Model_SelectionBenefit
from .Selection_Provision import Model_SelectionProvision

from ..tables import TBL_NAMES

CONFIG_ENTITY_COVARIANCE_SET = TBL_NAMES["CONFIG_ENTITY_COVARIANCE_SET"]
CONFIG_ENTITY_COVARIANCE_SET_ACL = TBL_NAMES["CONFIG_ENTITY_COVARIANCE_SET_ACL"]
CONFIG_BENEFIT_VARIATION_STATE = TBL_NAMES["CONFIG_BENEFIT_VARIATION_STATE"]
CONFIG_PROVISION_STATE = TBL_NAMES["CONFIG_PROVISION_STATE"]
CONFIG_PRODUCT = TBL_NAMES["CONFIG_PRODUCT"]
REF_MASTER = TBL_NAMES["REF_MASTER"]


class Model_ConfigEntityCovarianceSet_ACL(BaseModel, BaseRowLevelSecurityTable):
    __tablename__ = CONFIG_ENTITY_COVARIANCE_SET_ACL

    config_entity_covariance_set_acl_id = db.Column(db.Integer, primary_key=True)
    config_entity_covariance_set_id = db.Column(
        db.ForeignKey(f"{CONFIG_ENTITY_COVARIANCE_SET}.config_entity_covariance_set_id")
    )
    auth_role_code = db.Column(db.String(30), nullable=False)


class Model_ConfigEntityCovarianceSet(BaseModel):
    __tablename__ = CONFIG_ENTITY_COVARIANCE_SET

    config_entity_covariance_set_id = db.Column(db.Integer, primary_key=True)
    config_entity_id = db.Column(db.Integer, nullable=False)
    config_entity_type_code = db.Column(db.String(50), nullable=False)

    selector_attr_name = db.Column(db.String(1000), nullable=True)
    selector_attr_operator_id = db.Column(
        db.ForeignKey(f"{REF_MASTER}.ref_id"),
        nullable=True,
        comment="Pythonic comparison operators, such as __eq__, __gt__, etc.",
    )
    selector_attr_value = db.Column(db.String(100), nullable=True)
    selector_attr_data_type_id = db.Column(
        db.ForeignKey(f"{REF_MASTER}.ref_id"),
        nullable=True,
        comment="Javascript data types, such as string, number, and boolean",
    )

    ref_optionality_id = db.Column(
        db.ForeignKey(f"{REF_MASTER}.ref_id"), nullable=False
    )

    acl = db.relationship(
        "Model_ConfigEntityCovarianceSet_ACL", innerjoin=True, lazy="joined"
    )
    optionality = db.relationship(
        "Model_RefOptionality",
        primaryjoin="Model_ConfigEntityCovarianceSet.comparison_operator_id == Model_RefOptionality.ref_id",
        lazy="joined",
    )
    selector_operator = db.relationship(
        "Model_RefComparisonOperator",
        primaryjoin="Model_ConfigEntityCovarianceSet.comparison_operator_id == Model_RefComparisonOperator.ref_id",
        lazy="joined",
    )
    selector_data_type = db.relationship(
        "Model_RefDataTypes",
        primaryjoin="Model_ConfigEntityCovarianceSet.comparison_attr_data_type_id == Model_RefDataTypes.ref_id",
        lazy="joined",
    )

    covariance_rules = db.relationship(
        "Model_ConfigEntityCovarianceRule", lazy="joined"
    )

    __mapper_args__ = {
        "polymorphic_on": config_entity_type_code,
        "polymorphic_identity": "base",
    }

    @classmethod
    def is_applicable(cls, covariance_set, selection_instance):
        """
        Validate if a covariance set is applicable, given a selection instance
        """
        if (
            covariance_set.selector_attr_name is None
            or covariance_set.selector_attr_operator_id is None
            or covariance_set.selector_attr_value is None
        ):
            return True

        data_type_obj = getattr(covariance_set, "selector_data_type", None)
        data_type = getattr(data_type_obj, "ref_attr_code", None)

        # get the operator code -- i.e. __eq__, __lt__, etc.
        operator = covariance_set.selector_operator.ref_attr_code

        # get the attribute being compared
        # this item might be of the wrong type
        actual_value__improper_type = covariance_set.nested_getattr(
            selection_instance, covariance_set.comparison_attr_name
        )
        # convert to the correct type
        actual_value = covariance_set.convert_data_type(
            actual_value__improper_type, data_type
        )

        # create a comparison function using the operator code
        comparison_function = getattr(actual_value, operator)
        return comparison_function(covariance_set.rule_value)

    @classmethod
    def handle_selection_benefit(cls, selection_instance: Model_SelectionBenefit):
        covariance_sets = cls.query.filter_by(
            config_entity_id=selection_instance.config_benefit_variation_state_id,
            config_entity_type_code="benefit_variation_state",
        ).all()
        return [s for s in covariance_sets if cls.is_applicable(s, selection_instance)]

    @classmethod
    def handle_selection_provision(cls, selection_instance: Model_SelectionProvision):
        covariance_sets = cls.query.filter_by(
            config_entity_id=selection_instance.config_provision_id,
            config_entity_type_code="provision_state",
        ).all()
        return [s for s in covariance_sets if cls.is_applicable(s, selection_instance)]

    @classmethod
    def get_applicable_covariance_sets(cls, selection_instance: BaseModel):
        """
        If the selector is null, then we don't need to refine
        """
        if isinstance(selection_instance, Model_SelectionBenefit):
            cls.handle_selection_benefit(selection_instance)
        elif isinstance(selection_instance, Model_SelectionProvision):
            cls.handle_selection_provision(selection_instance)
        else:
            return []

    def apply_ruleset(self, selection_instance: BaseModel):
        return all([rule.apply_rule(selection_instance) for rule in self.factor_rules])


class Model_ConfigEntityCovarianceSet_BenefitVariationState(
    Model_ConfigEntityCovarianceSet
):
    __mapper_args__ = {"polymorphic_identity": "benefit_variation_state"}
    entity = db.relationship(
        f"{CONFIG_BENEFIT_VARIATION_STATE}.config_benefit_variation_state_id",
        primaryjoin="Model_ConfigBenefitVariationState.config_benefit_variation_state_id == Model_ConfigEntityCovarianceSet_BenefitVariationState.config_entity_id",
    )

    @classmethod
    def find_by_benefit_variation_state(cls, id: int):
        return cls.query.filter_by(
            config_entity_id=id, config_entity_type_code="benefit_variation_state"
        ).all()


class Model_ConfigEntityCovarianceSet_ProvisionState(Model_ConfigEntityCovarianceSet):
    __mapper_args__ = {"polymorphic_identity": "provision_state"}
    entity = db.relationship(
        f"{CONFIG_PROVISION_STATE}.config_provision_state_id",
        primaryjoin="Model_ConfigProvisionState.config_provision_state_id == Model_ConfigEntityCovarianceSet_ProvisionState.config_entity_id",
    )

    @classmethod
    def find_by_provision_state(cls, id: int):
        return cls.query.filter_by(
            config_entity_id=id, config_entity_type_code="provision_state"
        ).all()
