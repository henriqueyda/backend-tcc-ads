"""empty message

Revision ID: e5561ef05c52
Revises: 834560b2f633
Create Date: 2023-03-23 22:45:08.672859

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "e5561ef05c52"
down_revision = "834560b2f633"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("is_admin", sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "is_admin")
    # ### end Alembic commands ###