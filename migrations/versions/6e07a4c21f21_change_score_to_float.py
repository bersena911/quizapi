"""change score to float

Revision ID: 6e07a4c21f21
Revises: 8fd9eccf9bc7
Create Date: 2022-10-07 23:06:38.145594

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "6e07a4c21f21"
down_revision = "8fd9eccf9bc7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        """alter table games alter column score type float using score::float;"""
    )
    conn.execute(
        """alter table game_questions alter column answer_score type float using answer_score::float;"""
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        """alter table games alter column score type integer using score::integer;"""
    )
    conn.execute(
        """alter table game_questions alter column answer_score type integer using answer_score::integer;"""
    )
