"""empty message

Revision ID: 31f911fd03ae
Revises: dccbf7bd5a33
Create Date: 2021-02-24 15:18:37.515459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31f911fd03ae'
down_revision = 'dccbf7bd5a33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('board_like', 'board_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('board_like', 'users_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('board_like', 'users_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('board_like', 'board_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
