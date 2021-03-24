import uuid

from flask import jsonify, json
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm.exc import NoResultFound

from app.main.extensions import db
from app.main import output

import pandas as pd

from datetime import datetime


class Store(db.Model):
    __tablemane__ = 'store'

    uuid = db.Column(UUID(as_uuid=True), unique=True, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_num = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    profile_img = db.Column(db.String, nullable=True)
    profile_detail = db.Column(db.String, nullable=True)
    working_time = db.Column(db.String, nullable=False)
    break_day = db.Column(db.String, nullable=True)
    open_or_not = db.Column(db.Boolean, default=False, nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now())
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    menus = db.relationship('Menus', passive_deletes=True, backref=db.backref('store_set'))
    option = db.relationship('Option', passive_deletes=True, backref=db.backref('store_set'))
    order = db.relationship('MainOrder', backref=db.backref('store_set'))
    board = db.relationship('Board', passive_deletes=True, backref=db.backref('store_set'))


class StoreDao:
    def __init__(self, db, board_dao, user_dao, menu_dao, order_dao):
        self.db = db
        self.menu_dao = menu_dao
        self.board_dao = board_dao
        self.user_dao = user_dao
        self.order_dao = order_dao

    def create_new_store(self, store_id, new_store, latitude, longitude, profile_img):
        try:
            new_store_info = Store(uuid=store_id, name=new_store['name'], phone_num=new_store['phone_num'],
                                   address=new_store['address'],
                                   profile_img=profile_img, profile_detail=new_store['profile_detail'],
                                   working_time=new_store['working_time'], break_day=new_store['break_day'],
                                   latitude=latitude, longitude=longitude)

            self.db.session.add(new_store_info)
            self.db.session.commit()
        except IntegrityError:
            self.db.session.rollback()
            return IntegrityError
        except DataError:
            self.db.session.rollback()
            return DataError
        except Exception:
            self.db.session.rollback()
            return Exception

        return jsonify({'msg': output.SUCCESS,
                        'store_id': store_id}), 200

    def get_new_store(self, off_set, limit, adj_time):
        try:
            new_stores = Store.query.filter(Store.create_at >= adj_time) \
                .order_by(Store.create_at.desc()).offset(off_set).limit(limit)

            df = pd.read_sql(new_stores.statement, new_stores.session.bind)
            results = json.loads(
                df.to_json(orient='records', default_handler=str))  # default-> str 으로줘서 encoding 문제 해결하기!

            return jsonify(results), 200

        except NoResultFound:
            return NoResultFound
        except TypeError:
            return TypeError
        except Exception:
            return Exception

    def get_near_store(self, latitude, longitude, meter):
        try:
            # 제일 가까운 순서대로!
            stores = '''
                        SELECT *
                            FROM (
                                SELECT * , earth_distance(ll_to_earth({0}, {1}),
                                ll_to_earth(store.latitude, store.longitude)) as distance
                                FROM store
                            ) store
                            WHERE store.distance < {2}
                            ORDER BY store.distance ASC;
                        '''.format(latitude, longitude, meter)

            df = pd.read_sql(stores, self.db.session.bind)
            result = json.loads(df.to_json(orient='records', default_handler=str))
            if not result:
                return NoResultFound
        except NoResultFound:
            return NoResultFound
        except DataError:
            return DataError
        except TypeError:
            return TypeError
        except Exception:
            return Exception
        return jsonify(result)

    def get_store_info(self, store_id):
        try:
            store = self.db.session.query(Store).filter(Store.uuid == store_id)
            df = pd.read_sql(store.statement, store.session.bind)
            result = json.loads(df.to_json(orient='records', default_handler=str))
            if not result:
                return NoResultFound
            return jsonify(result), 200
        except NoResultFound:
            return NoResultFound
        except DataError:
            return DataError
        except Exception:
            return Exception

    def create_category(self, category_id, category_name):
        try:
            up_category = self.menu_dao.Category(uuid=category_id,
                                                 name=category_name)

            self.db.session.add(up_category)
            self.db.session.commit()
        except IntegrityError:
            self.db.session.rollback()
            return IntegrityError

    def create_menu(self, menu_id, name, price, profile, profile_img, sale_status, category_id, store_id):
        try:
            new_menu = self.menu_dao.Menus(uuid=menu_id,
                                           name=name,
                                           price=price,
                                           profile=profile,
                                           profile_img=profile_img,
                                           sale_status=sale_status,
                                           category_id=category_id,
                                           store_id=store_id)

            self.db.session.add(new_menu)
            self.db.session.commit()

        except IntegrityError:
            self.db.session.rollback()
            return IntegrityError
        except DataError:
            self.db.session.rollback()
            return DataError
        except Exception:
            self.db.session.rollback()
            return Exception
        return jsonify({'msg': output.SUCCESS,
                        'category_id': category_id,
                        'menu_id' : menu_id})

    def create_option(self, option_id, store_id, option_name, extra_price):
        option = self.menu_dao.Option
        try:
            new_option = option(uuid=option_id,
                                store_id=store_id,
                                option_name=option_name,
                                extra_price=extra_price)
            self.db.session.add(new_option)
            self.db.session.commit()
        except IntegrityError:
            self.db.session.rollback()
            return IntegrityError
        except DataError:
            self.db.session.rollback()
            return DataError
        except Exception:
            self.db.session.rollback()
            return Exception

        return jsonify({'msg': output.SUCCESS,
                        'option_id': option_id}), 200

    def _get_category(self, category_id):
        Category = self.menu_dao.Category
        result = Category.query.filter(Category.uuid == category_id).one()
        return result

    def get_all(self, store_id):
        try:
            store = Store.query.filter(Store.uuid == store_id).one()
        except NoResultFound:
            return NoResultFound
        category_id = set([i.category_id for i in store.menus])
        try:
            result = [{
                "store_id": store.uuid,
                "store_name": store.name,
                "phone_num": store.phone_num,
                "address": store.address,
                "profile_img": store.profile_img,
                "profile_detail": store.profile_detail,
                "working_time": store.working_time,
                "break_day": store.break_day,
                "status": store.open_or_not,
                "category": [{
                    "category_id": ca,
                    "name": self._get_category(ca).name,
                    "menus": [{
                        "menu_id": menu.uuid,
                        "name": menu.name,
                        "price": menu.price,
                        "profile": menu.profile,
                        "profile_img": menu.profile_img,
                        "sale_status": menu.sale_status
                    } for menu in self._get_category(ca).menus]
                } for ca in category_id],
                "option": [{
                    "option_id": option.uuid,
                    "name": option.option_name,
                    "extra_price": option.extra_price
                } for option in store.option]
            }]
        except NoResultFound:
            return NoResultFound
        except Exception:
            return Exception

        return jsonify(result)

    def get_all_menus(self, store_id, category_id, off_set, limit):
        menus = self.menu_dao.Menus
        try:
            all_menus = self.db.session.query(menus).filter((menus.category_id == category_id),
                                                            (menus.store_id == store_id)).offset(off_set).limit(limit)
            df = pd.read_sql(all_menus.statement, all_menus.session.bind)
            result = json.loads(df.to_json(orient='records', default_handler=str))
            if not result:
                return NoResultFound
        except NoResultFound:
            return NoResultFound
        except DataError:
            return DataError
        except Exception:
            return Exception

        return jsonify(result)

    def get_all_option(self, store_id):
        option = self.menu_dao.Option
        try:
            all_options = self.db.session.query(option).filter(option.store_id == store_id)
            df = pd.read_sql(all_options.statement, all_options.session.bind)
            result = json.loads(df.to_json(orient='records', default_handler=str))
            if not result:
                return NoResultFound
        except NoResultFound:
            return NoResultFound
        except DataError:
            return DataError
        except Exception:
            return Exception

        return jsonify(result)

    def delete_store(self, store_id):
        try:
            delete = Store.query.filter(Store.uuid == store_id).delete()
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return IntegrityError
        except Exception:
            db.session.rollback()
            return Exception
        return jsonify(msg=output.SUCCESS)

    def all_store(self, off_set, limit):
        try:
            stores = Store.query.offset(off_set).limit(limit)
            df = pd.read_sql(stores.statement, self.db.session.bind)
            result = json.loads(df.to_json(orient='records', default_handler=str))
        except NoResultFound:
            return NoResultFound
        except Exception:
            return Exception
        return jsonify(result)

    def search_store(self, words, off_set, limit):
        row_query = '''
                SELECT *
                    FROM store
                    WHERE store.name like '%%{0}%%'
                    OFFSET {1}
                    LIMIT {2};
                '''.format(words, off_set, limit)
        try:
            df = pd.read_sql(row_query, self.db.session.bind)

            result = json.loads(df.to_json(orient='records', default_handler=str))

        except NoResultFound:
            return NoResultFound
        except Exception:
            return Exception

        return jsonify(result)

    def modify_menu(self, store_id, menu_id, payload):
        Menus = self.menu_dao.Menus
        menu = Menus.query.filter((Menus.store_id == store_id),
                                  (Menus.uuid == menu_id)).one()

        add_list = []

        if 'name' in payload:
            add_list.append('name')
        if 'price' in payload:
            add_list.append('price')
        if 'profile' in payload:
            add_list.append('profile')
        if 'sale_status' in payload:
            add_list.append('sale_status')

        for i in add_list:
            if i == 'name':
                menu.name = payload['name']
            elif i == 'price':
                menu.price = payload['price']
            elif i == 'profile':
                menu.profile = payload['profile']
            elif i == 'sale_status':
                menu.sale_status = payload['sale_status']

        try:
            self.db.session.commit()
        except DataError:
            self.db.session.rollback()
            return jsonify(msg=output.CHECK_DATA_TYPE_ERROR), 400
        except IntegrityError:
            self.db.session.rollback()
            return jsonify(msg=output.DATABASE_ERROR), 400
        return jsonify(msg=output.SUCCESS)


    def modify_option(self, store_id, option_id, payload):
        Option = self.menu_dao.Option
        try:
            option = Option.query.filter((Option.store_id == store_id),
                                     (Option.uuid == option_id)).one()
        except NoResultFound:
            self.db.session.rollback()
            return jsonify(msg=output.NO_RESULT_ERROR)

        add_list = []
        if 'option_name' in payload:
            add_list.append('option_name')
        elif 'extra_price' in payload:
            add_list.append('extra_price')

        for i in add_list:
            if i == 'option_name':
                option.option_name = payload['option_name']
            elif i == 'extra_price':
                option.extra_price = payload['extra_price']

        try:
            db.session.commit()
        except DataError:
            self.db.session.rollback()
            return jsonify(msg=output.CHECK_DATA_TYPE_ERROR), 400
        except IntegrityError:
            self.db.session.rollback()
            return jsonify(msg=output.DATABASE_ERROR), 400
        return jsonify(msg=output.SUCCESS)






