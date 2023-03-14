"""empty message

Revision ID: 834560b2f633
Revises: a8445019b447
Create Date: 2023-03-12 22:30:47.666646

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "834560b2f633"
down_revision = "a8445019b447"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "order", sa.Column("delivery_address", sa.String(length=255), nullable=True)
    )
    op.add_column(
        "order", sa.Column("delivery_city", sa.String(length=255), nullable=True)
    )
    op.add_column(
        "order", sa.Column("delivery_state", sa.String(length=255), nullable=True)
    )
    op.add_column(
        "order", sa.Column("delivery_zip", sa.String(length=255), nullable=True)
    )
    op.add_column(
        "order", sa.Column("delivery_reference", sa.String(length=255), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("order", "delivery_reference")
    op.drop_column("order", "delivery_zip")
    op.drop_column("order", "delivery_state")
    op.drop_column("order", "delivery_city")
    op.drop_column("order", "delivery_address")
    # ### end Alembic commands ###