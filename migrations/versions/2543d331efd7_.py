"""empty message

Revision ID: 2543d331efd7
Revises: 0be99e93696f
Create Date: 2021-02-28 11:33:40.356227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2543d331efd7'
down_revision = '0be99e93696f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('main_order', sa.Column('quantity', sa.Integer(), nullable=True))
    op.add_column('main_order', sa.Column('user_ide', sa.Integer(), nullable=True))
    op.drop_constraint('main_order_user_id_fkey', 'main_order', type_='foreignkey')
    op.create_foreign_key(None, 'main_order', 'users', ['user_ide'], ['id'], ondelete='CASCADE')
    op.drop_column('main_order', 'user_id')
    op.drop_column('order_detail', 'quantity')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_detail', sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('main_order', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'main_order', type_='foreignkey')
    op.create_foreign_key('main_order_user_id_fkey', 'main_order', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_column('main_order', 'user_ide')
    op.drop_column('main_order', 'quantity')
    # ### end Alembic commands ###
