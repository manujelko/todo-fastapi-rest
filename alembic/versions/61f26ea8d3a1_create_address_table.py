"""Create address table

Revision ID: 61f26ea8d3a1
Revises: 3d789313d15a
Create Date: 2022-11-05 11:20:37.545813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "61f26ea8d3a1"
down_revision = "3d789313d15a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "address",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("address1", sa.String(), nullable=False),
        sa.Column("address2", sa.String(), nullable=False),
        sa.Column("city", sa.String(), nullable=False),
        sa.Column("state", sa.String(), nullable=False),
        sa.Column("country", sa.String(), nullable=False),
        sa.Column("postal_code", sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("address")
