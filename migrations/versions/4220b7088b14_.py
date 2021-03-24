"""empty message

Revision ID: 4220b7088b14
Revises: e9a421074946
Create Date: 2021-03-01 11:57:10.507275

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4220b7088b14'
down_revision = 'e9a421074946'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('refresh',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('refresh_token', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('refresh')
    # ### end Alembic commands ###