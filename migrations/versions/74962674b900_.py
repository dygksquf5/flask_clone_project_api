"""empty message

Revision ID: 74962674b900
Revises: db06eec0c8aa
Create Date: 2021-03-03 17:12:05.653409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74962674b900'
down_revision = 'db06eec0c8aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('store', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('store', sa.Column('longitude', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('store', 'longitude')
    op.drop_column('store', 'latitude')
    # ### end Alembic commands ###
