"""change question type

Revision ID: 37eada297bdd
Revises: cc9706c7d2a0
Create Date: 2022-10-06 16:05:46.961952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "37eada297bdd"
down_revision = "cc9706c7d2a0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        "alter table questions alter column type type varchar using type::varchar;"
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        "alter table questions alter column type type boolean using type::boolean;"
    )
