"""empty message

Revision ID: 763fbee93c87
Revises: 90bf9f3406bb
Create Date: 2021-02-25 15:11:46.547191

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '763fbee93c87'
down_revision = '90bf9f3406bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'option', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'option', type_='unique')
    # ### end Alembic commands ###
