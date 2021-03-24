from app.main.extensions import db
from sqlalchemy.dialects.postgresql import UUID

from datetime import datetime

board_like_table = db.Table(
    'board_like',
    db.Column('users_id', UUID(as_uuid=True), db.ForeignKey('users.uuid', ondelete='CASCADE')),
    db.Column('board_id', UUID(as_uuid=True), db.ForeignKey('board.uuid', ondelete='CASCADE'))
)


class Board(db.Model):
    __tablename__ = 'board'

    uuid = db.Column(UUID(as_uuid=True), unique=True, primary_key=True)
    store_id = db.Column(UUID(as_uuid=True), db.ForeignKey('store.uuid', ondelete='CASCADE'))
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.uuid', ondelete='CASCADE'))

    content = db.Column(db.String, nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    image = db.Column(db.String, nullable=True)

    like = db.relationship('Users', secondary=board_like_table, backref=db.backref('board_like_set'))
    comment = db.relationship('Comment', backref=db.backref('board_set'))


class Comment(db.Model):
    __tablename__ = 'comment'

    uuid = db.Column(UUID(as_uuid=True), unique=True, primary_key=True)
    content = db.Column(db.String, nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.uuid', ondelete='CASCADE'))
    board_id = db.Column(UUID(as_uuid=True), db.ForeignKey('board.uuid', ondelete='CASCADE'))


class BoardDao:
    def __init__(self, db, store_dao, user_dao, menu_dao, order_dao):
        self.db = db
        self.menu_dao = menu_dao
        self.store_dao = store_dao
        self.user_dao = user_dao
        self.order_dao = order_dao
    pass