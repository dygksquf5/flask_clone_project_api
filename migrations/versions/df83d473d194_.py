"""empty message

Revision ID: df83d473d194
Revises: 6b99c6475051
Create Date: 2021-02-25 15:25:21.736809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df83d473d194'
down_revision = '6b99c6475051'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart', sa.Column('option_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'cart', 'option', ['option_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cart', type_='foreignkey')
    op.drop_column('cart', 'option_id')
    # ### end Alembic commands ###
