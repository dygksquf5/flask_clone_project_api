from sqlalchemy.dialects.postgresql import UUID
from app.main.extensions import db


# 큰 종류 나뉘는곳, 커피, 베이컬, 티종류 등등
class Category(db.Model):
    __tablename__ = 'category'

    uuid = db.Column(UUID(as_uuid=True), unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)

    menus = db.relationship('Menus', passive_deletes=True, backref=db.backref('category_set'))


class Menus(db.Model):
    __tablename__ = 'menus'

    uuid = db.Column(UUID(as_uuid=True), unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    profile = db.Column(db.String, nullable=True)
    profile_img = db.Column(db.String, nullable=True)
    sale_status = db.Column(db.Boolean, default=True)

    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('category.uuid', ondelete='CASCADE'))

    store_id = db.Column(UUID(as_uuid=True), db.ForeignKey('store.uuid', ondelete='CASCADE'))


class Option(db.Model):
    __tablename__ = 'option'

    uuid = db.Column(UUID(as_uuid=True), unique=True, primary_key=True)
    store_id = db.Column(UUID(as_uuid=True), db.ForeignKey('store.uuid', ondelete='CASCADE'))
    option_name = db.Column(db.String)
    extra_price = db.Column(db.Integer)


class MenuDao:
    def __init__(self, db, board_dao, store_dao, user_dao,order_dao):
        self.db = db
        self.board_dao = board_dao
        self.store_dao = store_dao
        self.user_dao = user_dao
        self.order_dao = order_dao
    pass

