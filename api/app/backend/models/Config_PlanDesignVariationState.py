from typing import List
from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES
from .Config_PlanDesignSet import (
    Model_ConfigPlanDesignSet_Product,
    Model_ConfigPlanDesignSet_Coverage,
)

CONFIG_PLAN_DESIGN_SET = TBL_NAMES["CONFIG_PLAN_DESIGN_SET"]
CONFIG_PLAN_DESIGN_VARIATION_STATE = TBL_NAMES["CONFIG_PLAN_DESIGN_VARIATION_STATE"]
CONFIG_PRODUCT_VARIATION_STATE = TBL_NAMES["CONFIG_PRODUCT_VARIATION_STATE"]


class Model_ConfigPlanDesignVariationState(BaseModel):
    __tablename__ = CONFIG_PLAN_DESIGN_VARIATION_STATE
    __table_args__ = (
        db.UniqueConstraint(
            "config_product_variation_state_id", "config_plan_design_set_id"
        ),
    )

    config_plan_design_variation_state_id = db.Column(db.Integer, primary_key=True)
    config_product_variation_state_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_PRODUCT_VARIATION_STATE}.config_product_variation_state_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
    )
    config_plan_design_set_id = db.Column(
        db.ForeignKey(f"{CONFIG_PLAN_DESIGN_SET}.config_plan_design_set_id"),
        nullable=False,
    )

    plan_design_sets = db.relationship(
        "Model_ConfigPlanDesignSet", cascade="all, delete"
    )

    @classmethod
    def find_product_plan_designs(
        cls, product_variation_state_id: int
    ) -> List[Model_ConfigPlanDesignSet_Product]:
        """
        Find all product plan designs for a given product variation state.
        This returns product level plan designs, but does not give the benefit level details.
        """
        return (
            db.session.query(Model_ConfigPlanDesignSet_Product)
            .join(
                Model_ConfigPlanDesignSet_Product,
                Model_ConfigPlanDesignSet_Product.config_plan_design_set_id
                == cls.config_plan_design_set_id,
            )
            .filter_by(config_product_variation_state_id=product_variation_state_id)
            .all()
        )

    @classmethod
    def find_coverage_plan_designs(
        cls, product_variation_state_id: int
    ) -> List[Model_ConfigPlanDesignSet_Coverage]:
        return (
            db.session.query(Model_ConfigPlanDesignSet_Coverage)
            .join(
                Model_ConfigPlanDesignSet_Coverage,
                Model_ConfigPlanDesignSet_Coverage.config_plan_design_set_id
                == cls.config_plan_design_set_id,
            )
            .filter_by(config_product_variation_state_id=product_variation_state_id)
            .all()
        )
