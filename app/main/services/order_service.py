from flask import json, jsonify, g, request
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError, DataError

from datetime import datetime, timedelta, date
from app.main.models.order_dao import OrderStatus, ExpectTime
from app.main import output

import uuid
import re


class OrderService:
    def __init__(self, orderdao, app):
        self.app = app
        self.orderdao = orderdao

    def new_order(self, order_info, user_id):
        new_main_order_id = uuid.uuid4()

        # request params checking part, if not -> return params error
        check_list = output.NEW_ORDER_CHECK_LIST_1
        check_list_2 = output.NEW_ORDER_CHECK_LIST_2

        for i in check_list:
            if i not in order_info:
                return jsonify(msg=output.CHECK_PARAMS_ERROR), 400

        total_price = order_info['order_total_price']
        menus = order_info['menus']

        check_list_3 = [i for menu in menus for i in menu]

        for j in check_list_2:
            if j not in check_list_3:
                return jsonify(msg=output.CHECK_PARAMS_ERROR), 400

        check_list_4 = [j for menu in menus for i in menu['option'] for j in i]
        for v in check_list_4:
            if 'option_id' != v:
                return jsonify(msg=output.CHECK_PARAMS_ERROR), 400

        for menu in menus:
            menu_detail = self.orderdao._get_menu(menu_id=menu['menu_id'])
            if menu_detail is DataError:
                return jsonify(msg=output.CHECK_MENU_ID_ERROR), 400
            elif menu_detail is NoResultFound:
                return jsonify(msg=output.NO_RESULT_MENU_ERROR), 404
            elif menu_detail is ValueError:
                return jsonify(msg=output.CHECK_UUID_VALUE_ERROR), 400

            if menu_detail.store_id != uuid.UUID(order_info['store_id']):
                return jsonify(msg=output.INVALID_MENU_WITH_STORE_ERROR), 400
            total_price -= menu_detail.price

            for option in menu['option']:
                option_detail = self.orderdao._get_option(option_id=option['option_id'])
                if option_detail is DataError:
                    return jsonify(msg=output.CHECK_OPTION_ID_ERROR), 400
                elif option_detail is NoResultFound:
                    return jsonify(msg=output.NO_RESULT_OPTION_ERROR), 404
                elif option_detail is ValueError:
                    return jsonify(msg=output.CHECK_UUID_VALUE_ERROR), 400

                if option_detail and option_detail.store_id != uuid.UUID(order_info['store_id']):
                    return jsonify(msg=output.INVALID_OPTION_WITH_STORE_ERROR), 400
                total_price -= option_detail.extra_price

        if total_price != 0:
            return jsonify(msg=output.INVALID_TOTAL_ORDER_PRICE_ERROR), 400

        try:
            ExpectTime(order_info['expect_time'])
        except:
            return jsonify(msg=output.WRONG_ENUM_ERROR), 400

        # main_order db 저장
        self.orderdao.create_new_main_order(order_info=order_info,
                                            user_id=user_id,
                                            main_order_id=new_main_order_id)

        # waiting before order status -> from 'waiting accept' to 'accepted'.
        return jsonify({'msg': output.ORDERED_AND_WAITING,
                        'order_id': new_main_order_id}), 200

    def check_order_status(self, user_id, main_order_id):
        current_status = self.orderdao.order_status(main_order_id=main_order_id)

        if current_status is NoResultFound:
            return jsonify(msg=output.NO_RESULT_ERROR), 404
        elif current_status is Exception:
            return jsonify(msg=output.UNEXPECTED_ERROR), 400
        elif current_status and current_status == OrderStatus(1).name:
            return jsonify(msg=output.ORDERED_AND_WAITING), 200
        else:
            result = self.orderdao.get_current_order_info(main_order_id=main_order_id, user_id=user_id)
            if result is NoResultFound:
                return jsonify(msg=output.NO_RESULT_ERROR), 404
            elif result is Exception:
                return jsonify(msg=output.UNEXPECTED_ERROR), 400
        return result

    def order_detail(self, date_from, date_to, user_id):
        if not date_from:
            date_from = (datetime.now().strftime("%Y") + "-" + datetime.now().strftime("%m"))
            if not date_to:
                date_to = date_from
        elif not date_to:
            date_to = date_from

        check = self._check_date_regex(date_from=date_from, date_to=date_to)
        if not check:
            return jsonify(msg=output.WRONG_DATE_TYPE_ERROR), 400

        result = self.orderdao.user_order_search(user_id=user_id, date_from=date_from, date_to=date_to)
        if result == NoResultFound:
            return jsonify(msg=output.NO_RESULT_ORDER_DETAIL), 404
        elif result == DataError:
            return jsonify(msg=output.CHECK_PARAMS_ERROR), 400
        elif result == Exception:
            return jsonify(msg=output.UNEXPECTED_ERROR), 400
        return result

    def change_status(self, payload):
        if 'order_id' not in payload or 'set_status' not in payload:
            return jsonify(msg=output.NOTHING_PARAMS_ERROR), 404
        main_order_id = payload['order_id']
        set_status = payload['set_status']
        try:
            uuid.UUID(main_order_id)
        except ValueError:
            return jsonify(msg=output.CHECK_UUID_VALUE_ERROR), 400

        try:
            OrderStatus(set_status)
        except:
            return jsonify(msg=output.WRONG_ENUM_ERROR), 400

        compare_time = datetime.now()
        main_order_info = self.orderdao.get_main_order(main_order_id=main_order_id)
        if main_order_info == NoResultFound:
            return jsonify(msg=output.NO_RESULT_ORDER_DETAIL), 404
        elif main_order_info == DataError:
            return jsonify(msg=output.CHECK_ORDER_ID_ERROR), 400
        elif main_order_info == Exception:
            return jsonify(msg=output.UNEXPECTED_ERROR), 400

        # 매장 주문 거부
        if set_status == 6:
            if main_order_info.order_status == OrderStatus(2).name:
                return jsonify(msg=output.STATUS_ERROR_2), 400
            elif main_order_info.order_status == OrderStatus(3).name:
                return jsonify(msg=output.STATUS_ERROR_3), 400
            elif main_order_info.order_status == OrderStatus(5).name:
                return jsonify(msg=output.STATUS_ERROR_5), 400
            elif main_order_info.order_status == OrderStatus(6).name:
                return jsonify(msg=output.STATUS_ERROR_6), 400
            return self.orderdao.change_order_status(status=set_status, main_order_info=main_order_info)

        elif set_status == 4:
            if main_order_info.order_status == OrderStatus(2).name:
                return jsonify(msg=output.STATUS_ERROR_2), 400
            elif main_order_info.order_status == OrderStatus(3).name:
                return jsonify(msg=output.STATUS_ERROR_3), 400
            elif main_order_info.order_status == OrderStatus(5).name:
                return jsonify(msg=output.STATUS_ERROR_5), 400
            elif main_order_info.order_status == OrderStatus(4).name:
                return jsonify(msg=output.STATUS_ERROR_4), 400
            elif main_order_info.order_status == OrderStatus(6).name:
                return jsonify(msg=output.STATUS_ERROR_6), 400

            # 사용자 주문3분 취소 부분
            if compare_time - main_order_info.create_at > timedelta(minutes=3):
                return jsonify(msg=output.TIME_OVER), 400
            else:
                return self.orderdao.change_order_status(status=set_status, main_order_info=main_order_info)
        # 매장에서 주문 수락 했을 때
        elif set_status == 2:
            if main_order_info.order_status == OrderStatus(4).name:
                return jsonify(msg=output.STATUS_ERROR_4), 400
            elif main_order_info.order_status == OrderStatus(5).name:
                return jsonify(msg=output.STATUS_ERROR_5), 400
            elif main_order_info.order_status == OrderStatus(6).name:
                return jsonify(msg=output.STATUS_ERROR_6), 400
            elif main_order_info.order_status == OrderStatus(2).name:
                return jsonify(msg=output.STATUS_ERROR_2), 400

            return self.orderdao.change_order_status(status=set_status, main_order_info=main_order_info)

        elif set_status == 3:
            if main_order_info.order_status == OrderStatus(4).name:
                return jsonify(msg=output.STATUS_ERROR_4), 400
            elif main_order_info.order_status == OrderStatus(5).name:
                return jsonify(msg=output.STATUS_ERROR_5), 400
            elif main_order_info.order_status == OrderStatus(6).name:
                return jsonify(msg=output.STATUS_ERROR_6), 400
            elif main_order_info.order_status == OrderStatus(3).name:
                return jsonify(msg=output.STATUS_ERROR_3), 400
            elif main_order_info.order_status == OrderStatus(1).name:
                return jsonify(msg=output.STATUS_ERROR_1), 400

            return self.orderdao.change_order_status(status=set_status, main_order_info=main_order_info)

        elif set_status == 5:
            if main_order_info.order_status == OrderStatus(2).name:
                return jsonify(msg=output.STATUS_ERROR_2), 400
            elif main_order_info.order_status == OrderStatus(3).name:
                return jsonify(msg=output.STATUS_ERROR_3), 400
            elif main_order_info.order_status == OrderStatus(4).name:
                return jsonify(msg=output.STATUS_ERROR_4), 400
            elif main_order_info.order_status == OrderStatus(5).name:
                return jsonify(msg=output.STATUS_ERROR_5), 400
            return self.orderdao.change_order_status(status=set_status, main_order_info=main_order_info)

        else:
            return jsonify(msg=output.NO_RESULT_ERROR), 404

    def reorder(self, order_id, payload, user_id):
        new_main_order_id = uuid.uuid4()

        order_info = self.orderdao.get_main_order(main_order_id=order_id)

        if user_id != order_info.user_id:
            return jsonify(msg=output.WRONG_USER_WITH_ORDER_ERROR), 401

        result = self.orderdao.create_reorder(order_info=order_info,
                                              user_id=user_id,
                                              new_main_order_id=new_main_order_id,
                                              payload=payload)
        if result == IntegrityError:
            return jsonify(msg=output.DATABASE_ERROR), 400
        elif result == DataError:
            return jsonify(msg=output.CHECK_ORDER_ID_ERROR), 400
        elif result == Exception:
            return jsonify(msg=output.UNEXPECTED_ERROR), 400

        return result

    def _check_date_regex(self, date_from, date_to):
        check = re.compile('^([0-9]{4})+-([0-9]{2})$')
        f = check.match(date_from) is not None
        t = check.match(date_to) is not None

        if f and t:
            return True
        else:
            return False

    def scheduling_order_status(self):
        result = self.orderdao._scheduling_order_search()
        return jsonify(result)
