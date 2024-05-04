"""superuser

Revision ID: 046a67ebb50f
Revises: 7d21c8adc125
Create Date: 2024-04-25 08:01:50.887535

"""

import os
from alembic import op
import sqlalchemy as sa
from migrations.data.auth import (
    register_superuser_roles_permissions,
    register_sys_admin,
)


# revision identifiers, used by Alembic.
revision = "046a67ebb50f"
down_revision = "7d21c8adc125"
branch_labels = None
depends_on = None


def upgrade():
    pwd = os.getenv("SYS_SUPERUSER_PWD")
    if pwd is None:
        raise ValueError("SYS_SUPERUSER_PWD environment variable is not set")

    register_superuser_roles_permissions()
    register_sys_admin(pwd)


def downgrade():
    pass
