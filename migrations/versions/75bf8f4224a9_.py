"""empty message

Revision ID: 75bf8f4224a9
Revises: df3d75f7c1d3
Create Date: 2021-03-02 10:45:37.876930

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '75bf8f4224a9'
down_revision = 'df3d75f7c1d3'
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
    op.create_table('store',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('phone_num', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('profile_img', sa.String(), nullable=True),
    sa.Column('profile_detail', sa.String(), nullable=True),
    sa.Column('working_time', sa.String(), nullable=False),
    sa.Column('break_day', sa.String(), nullable=True),
    sa.Column('open_or_not', sa.Boolean(), nullable=False),
    sa.Column('create_at', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('users',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('pay_password', sa.String(), nullable=True),
    sa.Column('profile_img', sa.String(), nullable=True),
    sa.Column('create_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('board',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('create_at', sa.DateTime(), nullable=False),
    sa.Column('image', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['store_id'], ['store.uuid'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.uuid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('category',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['store_id'], ['store.uuid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('main_order',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('order_total_price', sa.Integer(), nullable=True),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.Column('way_of_payment', sa.String(), nullable=True),
    sa.Column('order_status', sa.String(), nullable=True),
    sa.Column('expect_time', sa.String(), nullable=True),
    sa.Column('extra_require', sa.String(), nullable=True),
    sa.Column('total_quantity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['store_id'], ['store.uuid'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.uuid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('option',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('option_name', sa.String(), nullable=True),
    sa.Column('extra_price', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['store_id'], ['store.uuid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('board_like',
    sa.Column('users_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('board_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['board_id'], ['board.uuid'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['users_id'], ['users.uuid'], ondelete='CASCADE')
    )
    op.create_table('comment',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('create_at', sa.DateTime(), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('board_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['board_id'], ['board.uuid'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.uuid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('menus',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('profile', sa.String(), nullable=True),
    sa.Column('profile_img', sa.String(), nullable=True),
    sa.Column('sale_status', sa.Boolean(), nullable=True),
    sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.uuid'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['store_id'], ['store.uuid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('menu_option_table',
    sa.Column('menu_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('option_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['menu_id'], ['menus.uuid'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['option_id'], ['option.uuid'], ondelete='CASCADE')
    )
    op.create_table('order_detail',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('main_order_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('menu_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('option_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['main_order_id'], ['main_order.uuid'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['menu_id'], ['menus.uuid'], ),
    sa.ForeignKeyConstraint(['option_id'], ['option.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_detail')
    op.drop_table('menu_option_table')
    op.drop_table('menus')
    op.drop_table('comment')
    op.drop_table('board_like')
    op.drop_table('option')
    op.drop_table('main_order')
    op.drop_table('category')
    op.drop_table('board')
    op.drop_table('users')
    op.drop_table('store')
    op.drop_table('refresh')
    # ### end Alembic commands ###
