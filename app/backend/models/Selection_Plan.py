import os
import datetime
from app.extensions import db
from app.shared import BaseModel, BaseRowLevelSecurityTable
from app.shared.utils import system_temporal_hint
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm import validates
from sqlalchemy.sql import text
from sqlalchemy.dialects.mssql import DATETIME2

from ..tables import TBL_NAMES
from .Selection_Coverage import Model_SelectionCoverage

CONFIG_PLAN_DESIGN_SET = TBL_NAMES["CONFIG_PLAN_DESIGN_SET"]
CONFIG_PRODUCT = TBL_NAMES["CONFIG_PRODUCT"]
CONFIG_PRODUCT_VARIATION_STATE = TBL_NAMES["CONFIG_PRODUCT_VARIATION_STATE"]
REF_MASTER = TBL_NAMES["REF_MASTER"]
REF_STATES = TBL_NAMES["REF_STATES"]
SELECTION_PLAN = TBL_NAMES["SELECTION_PLAN"]
SELECTION_PLAN_ACL = TBL_NAMES["SELECTION_PLAN_ACL"]
SELECTION_RATING_MAPPER_SET = TBL_NAMES["SELECTION_RATING_MAPPER_SET"]


class Model_SelectionPlan_ACL(BaseModel, BaseRowLevelSecurityTable):
    FN_NAME = "fn_rls__selection_plan_acl"

    __tablename__ = SELECTION_PLAN_ACL
    __table_args__ = (
        db.CheckConstraint("NOT (user_name IS NULL AND role_name IS NULL)"),
    )

    selection_plan_acl_id = db.Column(db.Integer, primary_key=True)
    selection_plan_id = db.Column(
        db.ForeignKey(
            f"{SELECTION_PLAN}.selection_plan_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=True,
        index=True,
    )
    user_name = db.Column(db.String(100), nullable=True)
    role_name = db.Column(db.String(100), nullable=True)
    with_grant_option = db.Column(db.Boolean, default=False)

    @classmethod
    def create_standard_policy(cls):
        sql = f"""
            SELECT COUNT(1)
            FROM   sys.objects
            WHERE  object_id = OBJECT_ID(N'{cls.RLS_SCHEMA}.{cls.FN_NAME}')
            AND type IN ( N'FN', N'IF', N'TF', N'FS', N'FT' )
        """

        rls_function_exists = db.session.execute(text(sql)).fetchone()[0]
        if rls_function_exists != 0:
            return

        sql = f"""
            CREATE FUNCTION {cls.RLS_SCHEMA}.{cls.FN_NAME}(@user_name VARCHAR(30))
                RETURNS TABLE
            WITH SCHEMABINDING
            AS
            RETURN SELECT 1 AS {cls.FN_NAME}_output
            WHERE 
                COALESCE(IS_MEMBER('{cls.RLS_RESTRICTED_ROLE}'), 1) = 0 OR (
                    CAST(SESSION_CONTEXT(N'user_name') AS VARCHAR(255)) IN (@user_name, 'superuser')
                )
        """
        db.session.execute(text(sql))
        db.session.commit()

    @classmethod
    def add_rls(cls, model):
        table_schema = model.__table__.schema
        _schema = "dbo" if table_schema is None else f"{table_schema}"
        _tablename = model.__tablename__
        _policy_name = f"policy_rls__{_schema}_{_tablename}"

        cls.create_standard_policy()

        sql = f"""
            SELECT COUNT(1)
            FROM   sys.objects
            WHERE  object_id = OBJECT_ID(N'{cls.RLS_SCHEMA}.{_policy_name}')
        """

        security_policy_exists = db.session.execute(text(sql)).fetchone()[0]
        if security_policy_exists != 0:
            return

        sql = f"""
            CREATE SECURITY POLICY {cls.RLS_SCHEMA}.{_policy_name}
            ADD FILTER PREDICATE {cls.RLS_SCHEMA}.{cls.FN_NAME}(user_name) ON {_schema}.{_tablename}
            WITH (STATE = ON)
        """
        db.session.execute(text(sql))
        db.session.commit()

    @classmethod
    def drop_rls(cls, model):
        table_schema = model.__table__.schema
        _schema = "dbo" if table_schema is None else f"{table_schema}"
        _tablename = model.__tablename__
        _policy_name = f"policy_rls__{_schema}_{_tablename}"

        sql = f"""
            DROP SECURITY POLICY {cls.RLS_SCHEMA}.{_policy_name};
        """
        try:
            db.session.execute(text(sql))
            db.session.commit()
        except Exception:
            pass

        sql = f"""
            DROP FUNCTION {cls.RLS_SCHEMA}.{cls.FN_NAME};
        """
        try:
            db.session.execute(text(sql))
            db.session.commit()
        except Exception:
            pass


class Model_SelectionPlan(BaseModel):
    __tablename__ = SELECTION_PLAN

    selection_plan_id = db.Column(db.Integer, primary_key=True)
    config_product_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT}.config_product_id"))
    selection_plan_effective_date = db.Column(db.Date, nullable=False)
    situs_state_id = db.Column(db.ForeignKey(f"{REF_STATES}.state_id"))
    config_product_variation_state_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_PRODUCT_VARIATION_STATE}.config_product_variation_state_id"
        )
    )
    selection_group_id = db.Column(db.Integer, nullable=True)
    cloned_from_selection_plan_id = db.Column(
        db.ForeignKey(f"{SELECTION_PLAN}.selection_plan_id"), nullable=True
    )
    is_template = db.Column(db.Boolean, default=False)
    plan_status = db.Column(db.ForeignKey(f"{REF_MASTER}.ref_id"))
    plan_as_of_dts = db.Column(
        DATETIME2(7),
        nullable=False,
        comment="All configuration will be pulled as of this datetime. The goal is to set this date to a value immediately before the row_eff_dts of the first system-temporal record. In practice, it will be extremely rare for configuration to be updated concurrently with a plan that uses that configuration. Use the `get_db_current_timestamp` function to get the current timestamp from the database.",
    )

    row_eff_dts = db.Column(DATETIME2(7), nullable=False, server_default=db.func.now())
    row_exp_dts = db.Column(
        DATETIME2(7), nullable=False, server_default="9999-12-31 23:59:59.999999"
    )

    situs_state = db.relationship("Model_RefStates")
    config_product = db.relationship("Model_ConfigProduct")
    config_product_variation_state = db.relationship(
        "Model_ConfigProductVariationState"
    )
    acl = db.relationship("Model_SelectionPlan_ACL", innerjoin=True, lazy="joined")
    rating_mapper_sets = db.relationship("Model_SelectionRatingMapperSet")

    coverages = db.relationship("Model_SelectionCoverage", back_populates="parent")
    provisions = db.relationship("Model_SelectionProvision", back_populates="parent")

    @validates("plan_as_of_dts")
    def validates_plan_as_of_dts(self, key, value):
        if self.plan_as_of_dts:  # Field already exists
            raise ValueError("Plan as of datetime cannot be modified.")
        return value

    @hybrid_method
    def get_acl(self, t=None, *args, **kwargs):
        """
        This method returns the ACL list for the selection plan.
        If `t` is provided, it will return the ACL list as of that time using system-temporal table queries.
        """
        hint = system_temporal_hint(t)
        return (
            db.session.query(Model_SelectionPlan_ACL)
            .with_hint(Model_SelectionPlan_ACL, hint)
            .filter_by(selection_plan_id=self.selection_plan_id)
            .all()
        )

    @hybrid_method
    def get_coverages(self, t=None, *args, **kwargs):
        """
        This method returns the coverage list for the selection plan.
        If `t` is provided, it will return the coverage list as of that time using system-temporal table queries.
        """
        hint = system_temporal_hint(t)
        return (
            db.session.query(Model_SelectionCoverage)
            .with_hint(Model_SelectionCoverage, hint)
            .filter_by(selection_plan_id=self.selection_plan_id)
            .all()
        )
