"""create quiz model

Revision ID: 889527573ef0
Revises: dbf1a8f72108
Create Date: 2022-10-06 12:20:22.050032

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "889527573ef0"
down_revision = "dbf1a8f72108"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "quizzes",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("published", sa.Boolean(), nullable=True),
        sa.Column("user_id", postgresql.UUID(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("quizzes")
    # ### end Alembic commands ###
