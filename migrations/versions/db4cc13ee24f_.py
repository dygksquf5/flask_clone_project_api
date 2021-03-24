"""empty message

Revision ID: db4cc13ee24f
Revises: 90503410a402
Create Date: 2021-02-26 15:11:08.583009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db4cc13ee24f'
down_revision = '90503410a402'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_data')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order_data',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('main_order_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('menu_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('option_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['main_order_id'], ['main_order.id'], name='order_data_main_order_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['menu_id'], ['menus.id'], name='order_data_menu_id_fkey'),
    sa.ForeignKeyConstraint(['option_id'], ['option.id'], name='order_data_option_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='order_data_pkey')
    )
    # ### end Alembic commands ###