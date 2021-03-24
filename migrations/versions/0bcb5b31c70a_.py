"""empty message

Revision ID: 0bcb5b31c70a
Revises: 00939fb12edb
Create Date: 2021-02-26 10:34:35.040466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0bcb5b31c70a'
down_revision = '00939fb12edb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('option', sa.Column('extra_price', sa.Integer(), nullable=True))
    op.add_column('option', sa.Column('menu_id', sa.Integer(), nullable=True))
    op.add_column('option', sa.Column('option_name', sa.String(), nullable=True))
    op.create_foreign_key(None, 'option', 'menus', ['menu_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'option', type_='foreignkey')
    op.drop_column('option', 'option_name')
    op.drop_column('option', 'menu_id')
    op.drop_column('option', 'extra_price')
    # ### end Alembic commands ###
