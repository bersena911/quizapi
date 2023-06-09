"""add answer_score to game question

Revision ID: 8fd9eccf9bc7
Revises: 68fad4848e6d
Create Date: 2022-10-07 22:57:21.014142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8fd9eccf9bc7"
down_revision = "68fad4848e6d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "game_questions", sa.Column("answer_score", sa.Integer(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("game_questions", "answer_score")
    # ### end Alembic commands ###
