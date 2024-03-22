from typing import List
from app.extensions import db
from app.shared import BaseModel
from sqlalchemy import and_
from sqlalchemy.ext.hybrid import hybrid_property
from .Config_PlanDesignDetail import Model_ConfigPlanDesignDetail_PlanDesign
from .Config_Coverage import Model_ConfigCoverage

from ..tables import TBL_NAMES

CONFIG_COVERAGE = TBL_NAMES["CONFIG_COVERAGE"]
CONFIG_PLAN_DESIGN_SET = TBL_NAMES["CONFIG_PLAN_DESIGN_SET"]
CONFIG_PRODUCT = TBL_NAMES["CONFIG_PRODUCT"]


class Model_ConfigPlanDesignSet(BaseModel):
    __tablename__ = CONFIG_PLAN_DESIGN_SET

    config_plan_design_set_id = db.Column(db.Integer, primary_key=True)
    config_parent_id = db.Column(db.Integer, nullable=False)
    config_parent_type_code = db.Column(db.String(50), nullable=False)
    config_plan_design_set_label = db.Column(db.String(100), nullable=False)
    config_plan_design_set_description = db.Column(db.String(1000), nullable=True)

    __mapper_args__ = {
        "polymorphic_on": config_parent_type_code,
        "polymorphic_identity": "base",
    }


class Model_ConfigPlanDesignSet_Coverage(Model_ConfigPlanDesignSet):
    __mapper_args__ = {"polymorphic_identity": "coverage"}

    parent = db.relationship(
        "Model_ConfigCoverage",
        primaryjoin="Model_ConfigCoverage.config_coverage_id == Model_ConfigPlanDesignSet_Coverage.config_parent_id",
        foreign_keys="Model_ConfigPlanDesignSet_Coverage.config_parent_id",
    )
    plan_design_details = db.relationship(
        "Model_ConfigPlanDesignDetail_Benefit",
        primaryjoin="Model_ConfigPlanDesignSet_Coverage.config_plan_design_set_id == Model_ConfigPlanDesignDetail_Benefit.config_plan_design_set_id",
        foreign_keys="Model_ConfigPlanDesignDetail_Benefit.config_plan_design_set_id",
        uselist=True,
        lazy="joined",
    )

    @classmethod
    def get_available_plan_designs(cls, product_id: int):
        """
        Returns all the plan designs available for a given product.
        """
        return (
            cls.query.join(
                Model_ConfigCoverage,
                Model_ConfigCoverage.config_coverage_id == cls.config_parent_id,
            )
            .filter(Model_ConfigCoverage.config_product_id == product_id)
            .all()
        )


class Model_ConfigPlanDesignSet_Product(Model_ConfigPlanDesignSet):
    __mapper_args__ = {"polymorphic_identity": "product"}

    parent = db.relationship(
        "Model_ConfigProduct",
        primaryjoin="Model_ConfigProduct.config_product_id == Model_ConfigPlanDesignSet_Product.config_parent_id",
        foreign_keys="Model_ConfigPlanDesignSet_Product.config_parent_id",
    )
    plan_design_details = db.relationship(
        "Model_ConfigPlanDesignDetail_PlanDesign",
        primaryjoin="Model_ConfigPlanDesignSet_Product.config_plan_design_set_id == Model_ConfigPlanDesignDetail_PlanDesign.config_plan_design_set_id",
        foreign_keys="Model_ConfigPlanDesignDetail_PlanDesign.config_plan_design_set_id",
        uselist=True,
        lazy="joined",
    )

    @hybrid_property
    def coverage_plan_designs(self):
        """
        A product-level plan design set is composed of multiple coverage-level plan designs at the detail level.
        This property returns all the coverage-level plan designs that are part of this product-level plan design set.
        """
        PD = Model_ConfigPlanDesignDetail_PlanDesign
        CVG = Model_ConfigPlanDesignSet_Coverage
        return (
            db.session.query(CVG)
            .join(PD, PD.config_parent_id == CVG.config_plan_design_set_id)
            .filter(PD.config_plan_design_set_id == self.config_plan_design_set_id)
            .all()
        )

    @classmethod
    def find_by_parent(cls, parent_id, limit=1000, offset=0, *args, **kwargs):
        return (
            cls.query.filter(
                cls.config_parent_id == parent_id,
                cls.config_parent_type_code == "product",
            )
            .slice(offset, offset + limit)
            .all()
        )
