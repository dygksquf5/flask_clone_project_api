"""empty message

Revision ID: 2afc126ec68b
Revises: cc2501b978e9
Create Date: 2021-03-10 09:53:19.436604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2afc126ec68b'
down_revision = 'cc2501b978e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'store', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'store', type_='unique')
    # ### end Alembic commands ###