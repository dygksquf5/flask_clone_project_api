"""empty message

Revision ID: e0756a5ffbd6
Revises: 0bcb5b31c70a
Create Date: 2021-02-26 10:42:03.338240

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0756a5ffbd6'
down_revision = '0bcb5b31c70a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart', sa.Column('option_id', sa.BigInteger(), nullable=True))
    op.create_foreign_key(None, 'cart', 'option', ['option_id'], ['id'])
    op.add_column('order_data', sa.Column('option_id', sa.BigInteger(), nullable=True))
    op.create_foreign_key(None, 'order_data', 'option', ['option_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order_data', type_='foreignkey')
    op.drop_column('order_data', 'option_id')
    op.drop_constraint(None, 'cart', type_='foreignkey')
    op.drop_column('cart', 'option_id')
    # ### end Alembic commands ###
