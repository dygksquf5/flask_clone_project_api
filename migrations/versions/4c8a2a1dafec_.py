"""empty message

Revision ID: 4c8a2a1dafec
Revises: aed0da0473c1
Create Date: 2021-02-26 17:01:07.642872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c8a2a1dafec'
down_revision = 'aed0da0473c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_detail', sa.Column('option_id_1', sa.Integer(), nullable=True))
    op.add_column('order_detail', sa.Column('option_id_2', sa.Integer(), nullable=True))
    op.drop_constraint('order_detail_option_id_fkey', 'order_detail', type_='foreignkey')
    op.create_foreign_key(None, 'order_detail', 'option', ['option_id_2'], ['id'])
    op.create_foreign_key(None, 'order_detail', 'option', ['option_id_1'], ['id'])
    op.drop_column('order_detail', 'option_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_detail', sa.Column('option_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'order_detail', type_='foreignkey')
    op.drop_constraint(None, 'order_detail', type_='foreignkey')
    op.create_foreign_key('order_detail_option_id_fkey', 'order_detail', 'option', ['option_id'], ['id'])
    op.drop_column('order_detail', 'option_id_2')
    op.drop_column('order_detail', 'option_id_1')
    # ### end Alembic commands ###
