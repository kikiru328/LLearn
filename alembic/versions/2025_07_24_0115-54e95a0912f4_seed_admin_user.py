"""seed admin user

Revision ID: 54e95a0912f4
Revises: 715448e08026
Create Date: 2025-07-24 01:15:11.660325

"""

from datetime import datetime, timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "54e95a0912f4"
down_revision: Union[str, Sequence[str], None] = "715448e08026"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
            INSERT INTO users (id, email, name, password, role, created_at, updated_at)
            VALUES (
                :id, :email, :name, :password, :role, :now, :now
            )
            """
        ).bindparams(
            id="01K0W16RATW8CQJZCS10GKSQCS",
            email="admin@example.com",
            name="관리자",
            password="$2b$12$/GI0/xBIiMElWzK5gGBXw.0J2JPJRo8WgV69sRjjWa.R6yL3jjOVe",
            role="ADMIN",
            now=datetime.now(timezone.utc),
        )
    )


def downgrade() -> None:
    op.execute(
        sa.text("DELETE FROM users WHERE email = :email").bindparams(
            email="admin@example.com"
        )
    )
