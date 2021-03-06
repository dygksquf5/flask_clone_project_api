"""empty message

Revision ID: 02330da97870
Revises: f34457040caf
Create Date: 2021-03-02 09:55:44.686242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02330da97870'
down_revision = 'f34457040caf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('main_order', sa.Column('order_statu', sa.String(), nullable=True))
    op.drop_column('main_order', 'order_status')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('main_order', sa.Column('order_status', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('main_order', 'order_statu')
    # ### end Alembic commands ###
