"""add order_id sequence

Revision ID: f26d7ff85201
Revises: 37eada297bdd
Create Date: 2022-10-06 16:21:36.935683

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "f26d7ff85201"
down_revision = "37eada297bdd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        """
        create sequence questions_order_id_seq as integer;
        alter table questions alter column order_id set not null;
        alter table questions alter column order_id set default nextval('public.questions_order_id_seq'::regclass);
        alter sequence questions_order_id_seq owned by questions.order_id;
        """
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        """
        drop sequence questions_order_id_seq;
        """
    )
