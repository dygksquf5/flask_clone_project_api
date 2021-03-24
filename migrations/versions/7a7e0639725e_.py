"""empty message

Revision ID: 7a7e0639725e
Revises: ea725a9ab449
Create Date: 2021-02-26 10:45:53.027768

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a7e0639725e'
down_revision = 'ea725a9ab449'
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