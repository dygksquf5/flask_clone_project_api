"""empty message

Revision ID: c2694928df9c
Revises: 1bf533875cd8
Create Date: 2021-02-26 11:19:21.468010

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2694928df9c'
down_revision = '1bf533875cd8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart', sa.Column('option_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'cart', 'option', ['option_id'], ['id'])
    op.add_column('order_data', sa.Column('option_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'order_data', 'option', ['option_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order_data', type_='foreignkey')
    op.drop_column('order_data', 'option_id')
    op.drop_constraint(None, 'cart', type_='foreignkey')
    op.drop_column('cart', 'option_id')
    # ### end Alembic commands ###
