import datetime
from sqlalchemy.sql.functions import coalesce
from sqlalchemy.ext.hybrid import hybrid_property
from app.extensions import db
from app.shared import BaseModel

from .Config_ProductVariation import Model_ConfigProductVariation
from .Config_PlanDesignSet import Model_ConfigPlanDesignSet_Product
from .Config_PlanDesignVariationState import Model_ConfigPlanDesignVariationState
from .Ref_States import Model_RefStates

from ..tables import TBL_NAMES

CONFIG_AGE_BAND_SET = TBL_NAMES["CONFIG_AGE_BAND_SET"]
CONFIG_PLAN_DESIGN_SET = TBL_NAMES["CONFIG_PLAN_DESIGN_SET"]
CONFIG_PRODUCT = TBL_NAMES["CONFIG_PRODUCT"]
CONFIG_PRODUCT_VARIATION_STATE = TBL_NAMES["CONFIG_PRODUCT_VARIATION_STATE"]
CONFIG_PRODUCT_VARIATION = TBL_NAMES["CONFIG_PRODUCT_VARIATION"]
REF_MASTER = TBL_NAMES["REF_MASTER"]
REF_STATES = TBL_NAMES["REF_STATES"]


class Model_ConfigProductVariationState(BaseModel):
    __tablename__ = CONFIG_PRODUCT_VARIATION_STATE
    __table_args__ = (
        db.UniqueConstraint(
            "config_product_variation_id",
            "state_id",
            "config_product_variation_state_effective_date",
        ),
        db.CheckConstraint(
            "config_product_variation_state_effective_date <= config_product_variation_state_expiration_date"
        ),
    )

    config_product_variation_state_id = db.Column(db.Integer, primary_key=True)
    config_product_variation_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_PRODUCT_VARIATION}.config_product_variation_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    )
    state_id = db.Column(
        db.ForeignKey(
            f"{REF_STATES}.state_id", ondelete="NO ACTION", onupdate="NO ACTION"
        )
    )

    config_product_variation_state_effective_date = db.Column(db.Date, nullable=False)
    config_product_variation_state_expiration_date = db.Column(db.Date, nullable=False)
    default_config_age_band_set_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_AGE_BAND_SET}.config_age_band_set_id",
            ondelete="SET NULL",
            onupdate="SET NULL",
        ),
        nullable=True,
    )
    default_plan_design_set_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_PLAN_DESIGN_SET}.config_plan_design_set_id",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        nullable=True,
    )

    @hybrid_property
    def default_product_plan_design(self):
        """
        A product-level plan design set is composed of multiple coverage-level plan designs at the detail level.
        This property returns all the coverage-level plan designs that are part of this product-level plan design set.
        """
        PD = Model_ConfigPlanDesignSet_Product
        return (
            db.session.query(PD)
            .select_from(self.__class__)
            .join(PD, PD.config_plan_design_set_id == self.default_plan_design_set_id)
            .one_or_none()
        )

    @hybrid_property
    def selectable_product_plan_designs(self):
        """
        A product-level plan design set is composed of multiple coverage-level plan designs at the detail level.
        This property returns all the coverage-level plan designs that are part of this product-level plan design set.
        """
        PD = Model_ConfigPlanDesignSet_Product
        PDVS = Model_ConfigPlanDesignVariationState
        return (
            db.session.query(PD)
            .select_from(self.__class__)
            .join(
                PDVS,
                PDVS.config_product_variation_state_id
                == self.config_product_variation_state_id,
            )
            .join(PD, PD.config_plan_design_set_id == PDVS.config_plan_design_set_id)
            .all()
        )

    age_band_set = db.relationship("Model_ConfigAgeBandSet")
    state = db.relationship("Model_RefStates")
    parent = db.relationship("Model_ConfigProductVariation")

    @classmethod
    def find_by_product_variation(cls, id):
        return cls.query.filter(cls.config_product_variation_id == id).all()

    @classmethod
    def find_one_for_selection_plan(
        cls,
        config_product_id: int,
        config_product_variation_code: str,
        state_code: str,
        plan_effective_date: datetime.date,
    ):
        PV = Model_ConfigProductVariation
        S = Model_RefStates
        return (
            db.session.query(cls)
            .join(PV, cls.config_product_variation_id == PV.config_product_variation_id)
            .join(S, cls.state_id == S.state_id)
            .filter(
                PV.config_product_variation_code == config_product_variation_code,
                PV.config_product_id == config_product_id,
                S.state_code == state_code,
                cls.config_product_variation_state_effective_date
                <= plan_effective_date,
                plan_effective_date
                <= cls.config_product_variation_state_expiration_date,
            )
            .order_by(cls.config_product_variation_state_effective_date.desc())
            .one()
        )
