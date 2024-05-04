from app.extensions import db
from app.shared import BaseModel
from sqlalchemy.ext.hybrid import hybrid_property

from ..tables import TBL_NAMES

CONFIG_FACTOR_RULE = TBL_NAMES["CONFIG_FACTOR_RULE"]
CONFIG_FACTOR_SET = TBL_NAMES["CONFIG_FACTOR_SET"]
REF_MASTER = TBL_NAMES["REF_MASTER"]


class Model_ConfigFactorRule(BaseModel):
    __tablename__ = CONFIG_FACTOR_RULE

    config_factor_rule_id = db.Column(db.Integer, primary_key=True)
    config_factor_set_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_FACTOR_SET}.config_factor_set_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    )
    comparison_attr_name = db.Column(
        db.String(1000),
        nullable=False,
        comment="Column name of the column that is being compared",
    )
    comparison_operator_id = db.Column(
        db.ForeignKey(f"{REF_MASTER}.ref_id"),
        nullable=False,
        comment="Pythonic comparison operators, such as __eq__, __gt__, etc.",
    )
    comparison_attr_value = db.Column(db.String(100), nullable=False)
    comparison_attr_data_type_id = db.Column(
        db.ForeignKey(f"{REF_MASTER}.ref_id"),
        nullable=False,
        comment="Javascript data types, such as string, number, and boolean",
    )

    comparison_operator = db.relationship(
        "Model_RefComparisonOperator",
        primaryjoin="Model_ConfigFactorRule.comparison_operator_id == Model_RefComparisonOperator.ref_id",
    )
    data_type = db.relationship(
        "Model_RefDataTypes",
        primaryjoin="Model_ConfigFactorRule.comparison_attr_data_type_id == Model_RefDataTypes.ref_id",
    )

    @classmethod
    def convert_data_type(cls, value, data_type):
        if data_type in ["number", "int", "float"]:
            return float(value)
        if data_type in ["bool", "boolean"]:
            return str(value).upper() == "TRUE"
        return value

    @hybrid_property
    def rule_value(self):
        data_type_obj = getattr(self, "data_type", None)
        data_type = getattr(data_type_obj, "ref_attr_code", None)
        return self.convert_data_type(self.comparison_attr_value, data_type)

    def apply_rule(self, selection_provision: BaseModel):
        """
        Applies the rule
        """
        data_type_obj = getattr(self, "data_type", None)
        data_type = getattr(data_type_obj, "ref_attr_code", None)

        # get the operator code -- i.e. __eq__, __lt__, etc.
        operator = self.comparison_operator.ref_attr_code

        # get the attribute being compared
        # this item might be of the wrong type
        actual_value__improper_type = self.nested_getattr(
            selection_provision, self.comparison_attr_name
        )
        if actual_value__improper_type is None:
            return False
        # convert to the correct type
        actual_value = self.convert_data_type(actual_value__improper_type, data_type)

        # create a comparison function using the operator code
        comparison_function = getattr(actual_value, operator)
        return comparison_function(self.rule_value)
