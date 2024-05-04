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


with open("migrations/functions/fn_rls__user_name.sql", "r") as f:
    fn_rls__user_name = f.read()

with open("migrations/functions/fn_rls__user_role.sql", "r") as f:
    fn_rls__user_role = f.read()


def upgrade():
    op.execute("CREATE SCHEMA auth")
    op.execute("CREATE SCHEMA rls")
    op.execute(fn_rls__user_name)
    op.execute(fn_rls__user_role)


def downgrade():
    op.execute("DROP SCHEMA auth")
    op.execute("DROP SCHEMA rls")
    op.execute("DROP FUNCTION rls.fn_rls__user_name")
    op.execute("DROP FUNCTION rls.fn_rls__user_role")
