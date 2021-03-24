"""empty message

Revision ID: 13384145bc0b
Revises: b0c272df5915
Create Date: 2021-02-21 20:58:34.717951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13384145bc0b'
down_revision = 'b0c272df5915'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('pay_password', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'pay_password')
    # ### end Alembic commands ###
