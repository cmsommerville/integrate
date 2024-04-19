"""views and stored procs

Revision ID: 7d21c8adc125
Revises: 03bcf4f5967b
Create Date: 2024-04-18 16:20:12.109228

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "7d21c8adc125"
down_revision = "03bcf4f5967b"
branch_labels = None
depends_on = None

with open(
    "migrations/views/vw_config_product_default_rating_mapper_sets.sql", "r"
) as f:
    vw_config_product_default_rating_mapper_sets = f.read()

with open("migrations/views/vw_config_rating_cohorts.sql", "r") as f:
    vw_config_rating_cohorts = f.read()

with open("migrations/views/vw_selection_rate_table_factors.sql", "r") as f:
    vw_selection_rate_table_factors = f.read()

with open("migrations/stored_procs/selection_rate_engine.sql", "r") as f:
    selection_rate_engine = f.read()


def upgrade():
    op.execute("DROP VIEW IF EXISTS dbo.vw_config_product_default_rating_mapper_sets")
    op.execute(vw_config_product_default_rating_mapper_sets)

    op.execute("DROP VIEW IF EXISTS dbo.vw_config_rating_cohorts")
    op.execute(vw_config_rating_cohorts)

    op.execute("DROP VIEW IF EXISTS dbo.vw_selection_rate_table_factors")
    op.execute(vw_selection_rate_table_factors)

    op.execute("DROP PROCEDURE IF EXISTS dbo.selection_rate_engine")
    op.execute(selection_rate_engine)


def downgrade():
    op.execute("DROP VIEW dbo.vw_config_product_default_rating_mapper_sets")
    # op.execute(
    #     """CREATE VIEW dbo.vw_config_product_default_rating_mapper_sets AS
    #     SELECT
    #         NULL AS config_product_id,
    #         NULL AS config_rating_mapper_collection_id,
    #         NULL AS selection_rating_mapper_set_type,
    #         NULL AS default_config_rating_mapper_set_id
    #     """
    # )

    op.execute("DROP VIEW dbo.vw_config_rating_cohorts")
    # op.execute(
    #     """CREATE VIEW dbo.vw_config_rating_cohorts AS
    #     SELECT
    #         NULL AS config_product_id,
    #         NULL AS rate_table_age_value,
    #         NULL AS rate_table_attribute_detail_id1,
    #         NULL AS rate_table_attribute_detail_id2,
    #         NULL AS rate_table_attribute_detail_id3,
    #         NULL AS rate_table_attribute_detail_id4,
    #         NULL AS rate_table_attribute_detail_id5,
    #         NULL AS rate_table_attribute_detail_id6,
    #         NULL AS row_hash
    #     """
    # )

    op.execute("DROP VIEW dbo.vw_selection_rate_table_factors")
    # op.execute(
    #     """CREATE VIEW dbo.vw_selection_rate_table_factors AS
    #     SELECT
    #         NULL AS selection_benefit_id,
    #         NULL AS selection_plan_id,
    #         NULL AS config_rate_table_id,
    #         NULL AS factor_value
    #     """
    # )

    op.execute("DROP PROCEDURE dbo.selection_rate_engine")
