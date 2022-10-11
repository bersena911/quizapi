"""add time fields

Revision ID: 66c56ce8d341
Revises: b42165ae945b
Create Date: 2022-10-11 17:36:15.630484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "66c56ce8d341"
down_revision = "b42165ae945b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "game_questions",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )
    op.add_column(
        "game_questions",
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "games",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )
    op.add_column(
        "games", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "quizzes",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )
    op.add_column(
        "quizzes", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "users",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "created_at")
    op.drop_column("quizzes", "updated_at")
    op.drop_column("quizzes", "created_at")
    op.drop_column("games", "updated_at")
    op.drop_column("games", "created_at")
    op.drop_column("game_questions", "updated_at")
    op.drop_column("game_questions", "created_at")
    # ### end Alembic commands ###