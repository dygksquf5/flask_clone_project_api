"""empty message

Revision ID: 6493caf1cac1
Revises: 1f17448710cb
Create Date: 2021-02-25 15:19:39.141859

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6493caf1cac1'
down_revision = '1f17448710cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart', sa.Column('option_uuid', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'cart', 'option', ['option_uuid'], ['uuid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cart', type_='foreignkey')
    op.drop_column('cart', 'option_uuid')
    # ### end Alembic commands ###
