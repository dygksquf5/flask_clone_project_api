"""empty message

Revision ID: 0be99e93696f
Revises: b3638c5d7c1f
Create Date: 2021-02-26 18:01:34.881138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0be99e93696f'
down_revision = 'b3638c5d7c1f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cart')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cart',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('store_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('menu_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('option_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('quantity', sa.INTEGER(), server_default=sa.text('1'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['menu_id'], ['menus.id'], name='cart_menu_id_fkey'),
    sa.ForeignKeyConstraint(['option_id'], ['option.id'], name='cart_option_id_fkey'),
    sa.ForeignKeyConstraint(['store_id'], ['store.id'], name='cart_store_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='cart_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='cart_pkey')
    )
    # ### end Alembic commands ###