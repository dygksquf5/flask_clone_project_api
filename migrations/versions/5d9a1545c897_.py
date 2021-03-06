"""empty message

Revision ID: 5d9a1545c897
Revises: 8ce431e1a7e3
Create Date: 2021-03-04 16:17:34.990037

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5d9a1545c897'
down_revision = '8ce431e1a7e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('category_store_id_fkey', 'category', type_='foreignkey')
    op.drop_column('category', 'store_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category', sa.Column('store_id', postgresql.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key('category_store_id_fkey', 'category', 'store', ['store_id'], ['uuid'], ondelete='CASCADE')
    # ### end Alembic commands ###
