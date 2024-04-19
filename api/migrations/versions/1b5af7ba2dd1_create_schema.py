"""create_schema

Revision ID: 1b5af7ba2dd1
Create Date: 2024-04-19 16:27:30.291280

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1b5af7ba2dd1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE SCHEMA auth")
    op.execute("CREATE SCHEMA rls")


def downgrade():
    op.execute("DROP SCHEMA auth")
    op.execute("DROP SCHEMA rls")