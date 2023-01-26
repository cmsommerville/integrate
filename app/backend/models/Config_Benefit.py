from app.extensions import db
from app.shared import BaseModel, BaseRowLevelSecurityTable
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from ..tables import TBL_NAMES

CONFIG_BENEFIT = TBL_NAMES['CONFIG_BENEFIT']
CONFIG_BENEFIT_AUTH = TBL_NAMES['CONFIG_BENEFIT_AUTH']
CONFIG_BENEFIT_AUTH_ACL = TBL_NAMES['CONFIG_BENEFIT_AUTH_ACL']
CONFIG_COVERAGE = TBL_NAMES['CONFIG_COVERAGE']
CONFIG_RATE_GROUP = TBL_NAMES['CONFIG_RATE_GROUP']
CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
REF_MASTER = TBL_NAMES['REF_MASTER']


class Model_ConfigBenefitAuth_ACL(BaseModel, BaseRowLevelSecurityTable):
    __tablename__ = CONFIG_BENEFIT_AUTH_ACL

    config_benefit_auth_acl_id = db.Column(db.Integer, primary_key=True)
    config_benefit_auth_id = db.Column(db.ForeignKey(
        f"{CONFIG_BENEFIT_AUTH}.config_benefit_auth_id"))
    auth_role_code = db.Column(db.String(30), nullable=False)



class Model_ConfigBenefitAuth(BaseModel):
    __tablename__ = CONFIG_BENEFIT_AUTH
    # __table_args__ = (
    #     db.UniqueConstraint('config_benefit_id', 'priority'), 
    # )

    config_benefit_auth_id = db.Column(db.Integer, primary_key=True)
    config_benefit_id = db.Column(db.ForeignKey(
        f"{CONFIG_BENEFIT}.config_benefit_id"))
    priority = db.Column(db.Integer, nullable=False)
    min_value = db.Column(db.Numeric(12, 2))
    max_value = db.Column(db.Numeric(12, 2))
    step_value = db.Column(db.Numeric(12, 4))
    default_value = db.Column(db.Numeric(12, 4))

    acl = db.relationship("Model_ConfigBenefitAuth_ACL", 
        innerjoin=True, lazy='joined')


class Model_ConfigBenefit(BaseModel):
    __tablename__ = CONFIG_BENEFIT
    __table_args__ = (
        db.UniqueConstraint('config_benefit_version_code', ),
    )

    config_benefit_id = db.Column(db.Integer, primary_key=True)
    config_product_id = db.Column(db.ForeignKey(
        f"{CONFIG_PRODUCT}.config_product_id"), nullable=False)
    ref_benefit_id = db.Column(db.ForeignKey(
        f"{REF_MASTER}.ref_id"), nullable=False)
    config_coverage_id = db.Column(db.ForeignKey(
        f"{CONFIG_COVERAGE}.config_coverage_id"))
    config_rate_group_id = db.Column(db.ForeignKey(
        f"{CONFIG_RATE_GROUP}.config_rate_group_id"))
    config_benefit_version_code = db.Column(db.String(30), nullable=False)
    unit_type_id = db.Column(db.ForeignKey(f"{REF_MASTER}.ref_id"))
    config_benefit_description = db.Column(db.String(1000))

    durations = db.relationship("Model_ConfigBenefitDurationSet")
    ref_benefit = db.relationship("Model_RefBenefit",
        primaryjoin="Model_ConfigBenefit.ref_benefit_id == Model_RefBenefit.ref_id", lazy='joined')
    coverage = db.relationship("Model_ConfigCoverage")
    rate_group = db.relationship("Model_ConfigRateGroup")
    unit_type = db.relationship("Model_RefUnitCode",
        primaryjoin="Model_ConfigBenefit.unit_type_id == Model_RefUnitCode.ref_id", lazy='joined')
    benefit_auth = db.relationship("Model_ConfigBenefitAuth", 
        order_by="desc(Model_ConfigBenefitAuth.priority)", 
        innerjoin=True, lazy='joined')

    @hybrid_property
    def priority(self):
        return next((x.priority for x in self.benefit_auth), None)

    @hybrid_property
    def min_value(self):
        return next((x.min_value for x in self.benefit_auth), None)

    @hybrid_property
    def max_value(self):
        return next((x.max_value for x in self.benefit_auth), None)

    @hybrid_property
    def step_value(self):
        return next((x.step_value for x in self.benefit_auth), None)

    @hybrid_property
    def default_value(self):
        return next((x.default_value for x in self.benefit_auth), None)

    @classmethod
    def find_by_product(cls, id: int):
        return cls.query.filter(cls.config_product_id == id).all()

