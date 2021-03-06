"""empty message

Revision ID: 0356ef42673e
Revises: 02330da97870
Create Date: 2021-03-02 09:55:55.374532

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0356ef42673e'
down_revision = '02330da97870'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('main_order', sa.Column('order_status', sa.String(), nullable=True))
    op.drop_column('main_order', 'order_statu')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('main_order', sa.Column('order_statu', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('main_order', 'order_status')
    # ### end Alembic commands ###
