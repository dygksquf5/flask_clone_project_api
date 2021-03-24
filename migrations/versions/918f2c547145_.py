"""empty message

Revision ID: 918f2c547145
Revises: 5d9a1545c897
Create Date: 2021-03-04 16:19:17.870821

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '918f2c547145'
down_revision = '5d9a1545c897'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_detail')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order_detail',
    sa.Column('uuid', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('main_order_id', postgresql.UUID(), autoincrement=False, nullable=True),
    sa.Column('menu_id', postgresql.UUID(), autoincrement=False, nullable=True),
    sa.Column('option_id', postgresql.UUID(), autoincrement=False, nullable=True),
    sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['main_order_id'], ['main_order.uuid'], name='order_detail_main_order_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['menu_id'], ['menus.uuid'], name='order_detail_menu_id_fkey'),
    sa.ForeignKeyConstraint(['option_id'], ['option.uuid'], name='order_detail_option_id_fkey'),
    sa.PrimaryKeyConstraint('uuid', name='order_detail_pkey'),
    sa.UniqueConstraint('uuid', name='order_detail_uuid_key')
    )
    # ### end Alembic commands ###
