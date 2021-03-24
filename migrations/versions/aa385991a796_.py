"""empty message

Revision ID: aa385991a796
Revises: 17b734f6d403
Create Date: 2021-02-26 10:23:55.277238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa385991a796'
down_revision = '17b734f6d403'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('option_id_key', 'option', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('option_id_key', 'option', ['id'])
    # ### end Alembic commands ###
