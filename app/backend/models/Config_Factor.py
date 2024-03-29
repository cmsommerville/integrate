from app.extensions import db
from app.shared import BaseModel, BaseRuleset

from ..tables import TBL_NAMES

CONFIG_FACTOR = TBL_NAMES["CONFIG_FACTOR"]
CONFIG_FACTOR_SET = TBL_NAMES["CONFIG_FACTOR_SET"]
CONFIG_PROVISION = TBL_NAMES["CONFIG_PROVISION"]


class Model_ConfigFactorSet(BaseModel, BaseRuleset):
    __tablename__ = CONFIG_FACTOR_SET

    config_factor_set_id = db.Column(db.Integer, primary_key=True)
    config_provision_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_PROVISION}.config_provision_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    )
    factor_priority = db.Column(db.Integer, nullable=False)
    vary_by_rating_age = db.Column(db.Boolean, default=False)
    vary_by_rating_attr1 = db.Column(db.Boolean, default=False)
    vary_by_rating_attr2 = db.Column(db.Boolean, default=False)
    vary_by_rating_attr3 = db.Column(db.Boolean, default=False)
    vary_by_rating_attr4 = db.Column(db.Boolean, default=False)
    vary_by_rating_attr5 = db.Column(db.Boolean, default=False)
    vary_by_rating_attr6 = db.Column(db.Boolean, default=False)

    factor_rules = db.relationship("Model_ConfigFactorRule", lazy="joined")
    factor_values = db.relationship("Model_ConfigFactor", lazy="joined")

    def apply_ruleset(self, selection_provision: BaseModel):
        return all([rule.apply_rule(selection_provision) for rule in self.factor_rules])


class Model_ConfigFactor(BaseModel, BaseRuleset):
    __tablename__ = CONFIG_FACTOR

    config_factor_id = db.Column(db.Integer, primary_key=True)
    config_factor_set_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_FACTOR_SET}.config_factor_set_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        nullable=True,
    )
    rate_table_age_value = db.Column(db.Integer, default=-1)
    rating_attr_id1 = db.Column(db.Integer, default=-1)
    rating_attr_id2 = db.Column(db.Integer, default=-1)
    rating_attr_id3 = db.Column(db.Integer, default=-1)
    rating_attr_id4 = db.Column(db.Integer, default=-1)
    rating_attr_id5 = db.Column(db.Integer, default=-1)
    rating_attr_id6 = db.Column(db.Integer, default=-1)
    factor_value = db.Column(db.Numeric(8, 5), default=1)
