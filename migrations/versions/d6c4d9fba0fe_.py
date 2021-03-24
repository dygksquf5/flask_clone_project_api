"""empty message

Revision ID: d6c4d9fba0fe
Revises: bb5c662e9d1c
Create Date: 2021-02-24 14:20:33.061900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6c4d9fba0fe'
down_revision = 'bb5c662e9d1c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('store_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['store_id'], ['store.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('menus_detail')
    op.add_column('menus', sa.Column('category_id', sa.Integer(), nullable=True))
    op.add_column('menus', sa.Column('price', sa.Integer(), nullable=False))
    op.add_column('menus', sa.Column('profile', sa.String(length=300), nullable=True))
    op.add_column('menus', sa.Column('profile_img', sa.String(), nullable=True))
    op.add_column('menus', sa.Column('sale_status', sa.Boolean(), nullable=True))
    op.create_foreign_key(None, 'menus', 'category', ['category_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'menus', type_='foreignkey')
    op.drop_column('menus', 'sale_status')
    op.drop_column('menus', 'profile_img')
    op.drop_column('menus', 'profile')
    op.drop_column('menus', 'price')
    op.drop_column('menus', 'category_id')
    op.create_table('menus_detail',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('profile_img', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('sale_status', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('menus_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('profile', sa.VARCHAR(length=300), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['menus_id'], ['menus.id'], name='menus_detail_menus_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='menus_detail_pkey')
    )
    op.drop_table('category')
    # ### end Alembic commands ###