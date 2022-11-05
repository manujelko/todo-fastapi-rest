"""add apt num col

Revision ID: bac5f5d96445
Revises: 7374413835f3
Create Date: 2022-11-05 11:57:50.444182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bac5f5d96445"
down_revision = "7374413835f3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("address", sa.Column("apt_num", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("address", "apt_num")
