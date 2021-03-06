"""empty message

Revision ID: d2d3f590fb20
Revises: 918f2c547145
Create Date: 2021-03-05 10:27:16.440682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2d3f590fb20'
down_revision = '918f2c547145'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('main_order', 'total_quantity')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('main_order', sa.Column('total_quantity', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
