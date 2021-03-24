from flask import jsonify, json
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm.exc import NoResultFound

from app.main.extensions import db
from app.main import output
import enum, uuid
import datetime
import pandas as pd
from collections import defaultdict


class ExpectTime(enum.Enum):
    now = 0
    five_min = 5
    ten_min = 10
    twenty_min = 20
    thirty_min = 30
    forty_min = 40
    fifty_min = 50
    more_one_hour = 1


class OrderStatus(enum.Enum):
    ordered = 0
    waiting_accept = 1
    accepted = 2
    taken = 3
    canceled = 4
    auto_canceled = 5
    refuse = 6


class MainOrder(db.Model):
    __tablename__ = 'main_order'

    uuid = db.Column(UUID(as_uuid=True), unique=True, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.uuid', ondelete='CASCADE'))
    store_id = db.Column(UUID(as_uuid=True), db.ForeignKey('store.uuid', ondelete='CASCADE'))

    order_total_price = db.Column(db.Integer, nullable=True)
    create_at = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now)
    way_of_payment = db.Column(db.String, nullable=True)
    order_status = db.Column(db.String, default=OrderStatus(1).name)
    expect_time = db.Column(db.String, default=ExpectTime(0).name)  # default 는 지금
    extra_require = db.Column(db.String, nullable=True)

    js_order_data = db.Column(JSONB, nullable=True)


class OrderDao:
    def __init__(self, db, board_dao, store_dao, user_dao, menu_dao):
        self.db = db
        self.menu_dao = menu_dao
        self.board_dao = board_dao
        self.store_dao = store_dao
        self.user_dao = user_dao

    def _get_menu(self, menu_id):
        try:
            try:
                uuid.UUID(menu_id)
            except ValueError:
                return ValueError
            Menus = self.menu_dao.Menus
            _uuid = '{}'.format(menu_id)
            menu_info = Menus.query.filter(Menus.uuid == _uuid).one()
            return menu_info
        except DataError:
            return DataError
        except NoResultFound:
            return NoResultFound

    def _get_option(self, option_id):
        try:
            try:
                uuid.UUID(option_id)
            except ValueError:
                return ValueError
            Option = self.menu_dao.Option
            _uuid = '{}'.format(option_id)
            option_info = Option.query.filter(Option.uuid == _uuid).one()
            return option_info
        except DataError:
            return DataError
        except NoResultFound:
            return NoResultFound

    def create_new_main_order(self, order_info, user_id, main_order_id):

        store_id = order_info['store_id']
        order_total_price = order_info['order_total_price']
        way_of_payment = order_info['way_of_payment']
        expect_time = order_info['expect_time']
        extra_require = order_info['extra_require']
        menus = order_info['menus']
        json_data = [{
            "menu_id": menu['menu_id'],
            "menu_name": self._get_menu(menu['menu_id']).name,
            "menu_price": self._get_menu(menu['menu_id']).price,
            "quantity": menu['quantity'],
            "option": [{
                "option_id": option['option_id'],
                "option_name": self._get_option(option['option_id']).option_name,
                "extra_price": self._get_option(option['option_id']).extra_price
            } for option in menu['option']]
        } for menu in menus]

        try:
            # 메인오더 생성
            new_order = MainOrder(
                uuid=main_order_id,
                user_id=user_id,
                store_id=store_id,
                order_total_price=order_total_price,
                way_of_payment=way_of_payment,
                expect_time=ExpectTime(expect_time).name,
                extra_require=extra_require,
                js_order_data=json_data
            )

            self.db.session.add(new_order)

            self.db.session.commit()

        except IntegrityError:
            self.db.session.rollback()

            return jsonify({'msg': output.INVALID_ACCESS}), 400

    def create_reorder(self, order_info, user_id ,new_main_order_id ,payload):
        way_of_payment = order_info.way_of_payment
        expect_time = order_info.expect_time
        extra_require = order_info.extra_require

        if 'way_of_payment' in payload:
            way_of_payment = payload['way_of_payment']

        if 'expect_time' in payload:
            try:
                expect_time = ExpectTime(payload['expect_time']).name
            except:
                return jsonify(msg=output.WRONG_ENUM_ERROR), 400

        if 'extra_require' in payload:
            extra_require = payload['extra_require']

        new_order = MainOrder(
            uuid=new_main_order_id,
            user_id=user_id,
            store_id=order_info.store_id,
            order_total_price=order_info.order_total_price,
            way_of_payment=way_of_payment,
            expect_time=expect_time,
            extra_require=extra_require,
            js_order_data=order_info.js_order_data
        )

        try:
            db.session.add(new_order)
            db.session.commit()
        except IntegrityError:
            return IntegrityError
        except DataError:
            return DataError
        except Exception:
            return Exception

        return jsonify({"msg" : output.REORDER_CREATE_SUCCESS,
                        "reorder_id" : new_main_order_id})

    def get_current_order_info(self, main_order_id, user_id):
        try:
            try:
                json_order_data = self.db.session.query(MainOrder).filter((
                        MainOrder.uuid == main_order_id), (MainOrder.user_id == user_id)).one().js_order_data
            except NoResultFound:
                return NoResultFound

            main_order_query = '''
                            SELECT main_order.uuid as main_order_id, main_order.order_total_price, main_order.order_status,\
                             main_order.expect_time, main_order.create_at,
                                    users.name as user_name, users.uuid as user_id,
                                    store.name as store_name, store.uuid as store_id
                            FROM (
                                SELECT * FROM main_order WHERE main_order.uuid = '{}'
                            ) main_order
                            JOIN users
                            ON users.uuid = main_order.user_id
                            JOIN store
                            ON main_order.store_id = store.uuid
                            ORDER BY main_order.create_at, user_name DESC;
                            '''.format(str(main_order_id))

            main_df = pd.read_sql(main_order_query, self.db.session.bind)
            main_order_result = json.loads(main_df.to_json(orient='records', default_handler=str))

            for menu in json_order_data:
                for i in main_order_result:
                    i["menus"] = menu

            return jsonify(main_order_result)

        except Exception:
            return Exception

    def user_order_search(self, user_id, date_from, date_to):
        main_order_query = '''        
                    SELECT main_order.uuid as main_order_id, main_order.order_total_price, main_order.order_status,
                             main_order.expect_time, main_order.create_at, main_order.js_order_data,
                            store.name as store_name
                        FROM ( SELECT * FROM main_order 
                                WHERE to_char(create_at ,'YYYY-MM') BETWEEN '{0}' AND '{1}' 
                                and main_order.user_id = '{2}' 
                            )  main_order
                        JOIN users
                        ON users.uuid = '{2}'
                        JOIN store
                        ON main_order.store_id = store.uuid
                        ORDER BY main_order.create_at DESC;
                        '''.format(str(date_from), str(date_to), user_id)
        try:
            main_df = pd.read_sql(main_order_query, self.db.session.bind)
            main_order_result = json.loads(main_df.to_json(orient='records', default_handler=str))
            if not main_order_result:
                return NoResultFound
            return jsonify(main_order_result)
        except DataError:
            return DataError
        except Exception:
            return Exception

    def order_status(self, main_order_id):
        try:
            order_info = self.db.session.query(MainOrder).filter(MainOrder.uuid == main_order_id).one()
            status = order_info.order_status
            return status
        except NoResultFound:
            return NoResultFound
        except Exception:
            return Exception

    def auto_cancel_status(self, main_order_id):
        try:
            status = self.db.session.query(MainOrder).filter(MainOrder.uuid == main_order_id).one()
            status.order_status = OrderStatus(5).name  # auto canceled
            self.db.session.commit()
            return jsonify({'msg': output.ORDERED_AUTO_CANCELED}), 200
        except IntegrityError:
            self.db.session.rollback()
            return jsonify({'msg': output.INVALID_ACCESS}), 400

    def get_main_order(self, main_order_id):
        try:
            main_order = self.db.session.query(MainOrder).filter(MainOrder.uuid == main_order_id).one()
        except NoResultFound:
            return NoResultFound
        except DataError:
            return DataError
        except Exception:
            return Exception
        return main_order

    def change_order_status(self, status, main_order_info):
        try:
            main_order_info.order_status = OrderStatus(status).name
            self.db.session.commit()
            return jsonify({'msg': output.SUCCESS})
        except IntegrityError:
            self.db.session.rollback()
            return jsonify({'msg': output.INVALID_ACCESS}), 400

    def _scheduling_order_search(self):
        row_query = '''
                        SELECT main_order.uuid
                            FROM main_order
                            WHERE (now() - create_at) < '10 minute'
                             and '3 minute' < (now() - create_at)
                             and main_order.order_status = 'waiting_accept'
                            '''
        df = pd.read_sql(row_query, self.db.session.bind)
        result = json.loads(df.to_json(orient='records', default_handler=str))
        return result
