"""change answer size

Revision ID: cc9706c7d2a0
Revises: a014f946b916
Create Date: 2022-10-06 16:01:49.686880

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "cc9706c7d2a0"
down_revision = "a014f946b916"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        "alter table answers alter column choice type varchar using choice::varchar;"
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        "alter table answers alter column choice type varchar(1) using choice::varchar(1);"
    )
