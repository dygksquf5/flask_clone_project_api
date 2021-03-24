from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import current_user
from app.main.extensions import db
from flask import jsonify, json
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.main import output
import pandas as pd

import datetime


class Users(db.Model):
    __tablename__ = 'users'

    uuid = db.Column(UUID(as_uuid=True), unique=True, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    # 결제 패스워드
    pay_password = db.Column(db.String, nullable=True)
    profile_img = db.Column(db.String, nullable=True)
    create_at = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.now)

    board = db.relationship('Board', passive_deletes=True, backref=db.backref('user_board_set'))
    comment = db.relationship('Comment', passive_deletes=True, backref=db.backref('user_set'))
    order = db.relationship('MainOrder', passive_deletes=True, backref=db.backref('user_set'))


class Terms(db.Model):
    __tablename__ = 'terms'

    id = db.Column(db.Integer, primary_key=True)
    terms_detail = db.Column(db.String)


class UserDao:
    def __init__(self, db, board_dao, store_dao, menu_dao, order_dao):
        self.db = db
        self.menu_dao = menu_dao
        self.store_dao = store_dao
        self.board_dao = board_dao
        self.order_dao = order_dao

    def create_user(self, new_user, password,new_user_id, image_url):
        try:
            new_user_info = Users(uuid=new_user_id, name=new_user.get('name'), email=new_user.get('email'),
                                  password=password, profile_img=image_url)

            self.db.session.add(new_user_info)
            self.db.session.commit()
        except IntegrityError:
            self.db.session.rollback()
            return IntegrityError
        except Exception:
            return Exception

        return jsonify({'msg': output.SUCCESS ,
                        'user_id': new_user_id}), 200

    def get_all_terms(self):
        try:
            term = self.db.session.query(Terms).first()
            return term
        except NoResultFound:
            return NoResultFound
        except Exception:
            return Exception

    def get_user_info_by_email(self, email):
        try:
            user = self.db.session.query(Users).filter(Users.email == email).one()
            return user
        except NoResultFound:
            return NoResultFound
        except Exception:
            return Exception

    def get_user_info_by_id(self, user_id):
        try:
            user = self.db.session.query(Users).filter(Users.uuid == user_id)
            df = pd.read_sql(user.statement, db.session.bind)
            result = json.loads(df.to_json(orient='records', default_handler=str))
            return result
        except NoResultFound:
            return NoResultFound
        except DataError:
            return DataError
        except Exception:
            return Exception


    def save_user_profile_img(self, image_url):
        try:
            current_user.profile_img = image_url
            self.db.session.commit()
            return jsonify(msg=output.SUCCESS), 200
        except IntegrityError:
            db.session.rollaback()
            return IntegrityError

    def set_new_pay_password(self, pay_password):
        try:
            current_user.pay_password = pay_password
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return IntegrityError

    def set_new_password(self, user, new_password):
        try:
            user.password = new_password
            db.session.commit()
            return jsonify(msg=output.SUCCESS), 200
        except IntegrityError:
            db.session.rollback()
            return IntegrityError
        except DataError:
            db.session.rollback()
            return DataError

    def set_new_name(self, user, new_name):
        try:
            user.name = new_name
            db.session.commit()
            return jsonify(msg=output.SUCCESS), 200
        except IntegrityError:
            db.session.rollback()
            return IntegrityError
        except DataError:
            db.session.rollback()
            return DataError

    def set_new_email(self, user, new_email):
        try:
            user.email = new_email
            db.session.commit()
            return jsonify(msg=output.SUCCESS), 200
        except IntegrityError:
            db.session.rollback()
            return IntegrityError
        except DataError:
            return DataError


    def delete_user_info(self, user):
        try:
            user = Users.query.filter(Users.uuid == user.uuid).delete()
            db.session.commit()
            return jsonify(msg=output.SUCCESS), 200
        except IntegrityError:
            db.session.rollbakc()
            return IntegrityError
        except Exception:
            return Exception



