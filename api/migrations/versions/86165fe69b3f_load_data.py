"""load data

Revision ID: 86165fe69b3f
Revises: 046a67ebb50f
Create Date: 2024-05-08 16:13:48.142777

"""

from alembic import op
import sqlalchemy as sa
from migrations.data.refdata import load_refdata, downgrade_refdata


# revision identifiers, used by Alembic.
revision = "86165fe69b3f"
down_revision = "046a67ebb50f"
branch_labels = None
depends_on = None


def upgrade():
    load_refdata()


def downgrade():
    downgrade_refdata()
