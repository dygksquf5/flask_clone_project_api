"""empty message

Revision ID: acd633aa8398
Revises: 7a7e0639725e
Create Date: 2021-02-26 10:56:05.869612

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'acd633aa8398'
down_revision = '7a7e0639725e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_data', sa.Column('option_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'order_data', 'option', ['option_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order_data', type_='foreignkey')
    op.drop_column('order_data', 'option_id')
    # ### end Alembic commands ###