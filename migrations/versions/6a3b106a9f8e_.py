"""empty message

Revision ID: 6a3b106a9f8e
Revises: b6abf80344de
Create Date: 2021-02-19 18:21:42.675659

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a3b106a9f8e'
down_revision = 'b6abf80344de'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'content')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('content', sa.TEXT(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###