from flask import jsonify, json
from sqlalchemy import null
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.utils import secure_filename

from app.main import output
from app.main.connection import connect_s3, upload_s3, get_kakao

from datetime import datetime, timedelta
import uuid


class StoreService:
    def __init__(self, storedao, app):
        self.app = app
        self.storedao = storedao

    # 스토어 사진 파일 저장 s3 (AWS)
    def save_store_image(self, picture, filename):
        try:
            # s3 커넥트
            s3 = connect_s3()
            image_url = upload_s3(s3=s3, picture=picture, filename=filename)

            return image_url

        except Exception as err:
            return jsonify({'msg': err}, 400)

    def register_store(self, new_store, profile_img):
        new_store_id = uuid.uuid4()
        # 등록된 주소로 위도경도 찾아서 바로 입력해주기!
        address = new_store['address']

        latitude, longitude = get_kakao(address=address)

        if profile_img:
            filename = secure_filename(profile_img.filename)
            image_url = self.save_store_image(picture=profile_img,
                                              filename=filename)
            if image_url == Exception:
                return jsonify(msg=output.AWS_ERROR), 400

        else:
            image_url = None

        result = self.storedao.create_new_store(store_id=new_store_id, new_store=new_store,
                                                latitude=latitude, longitude=longitude,
                                                profile_img=image_url)

        if result == IntegrityError:
            return jsonify(msg=output.DATABASE_ERROR), 400
        elif result == DataError:
            return jsonify(msg=output.CHECK_DATA_TYPE_ERROR), 400
        elif result == Exception:
            return jsonify(msg=output.UNEXPECTED_ERROR), 400

        return result

    # 가입한지 얼마 안된 스토어들 가져오는 함수
    def new_stores(self, off_set, limit):
        # 오늘자 기준으로 30일 전
        adj_time = datetime.now().date() - timedelta(days=30)
        result = self.storedao.get_new_store(off_set=off_set, limit=limit, adj_time=adj_time)
        if not result:
            return jsonify(msg=output.NO_RESULT_ERROR), 404
        if result == NoResultFound:
            return jsonify(msg=output.NO_RESULT_ERROR), 404
        elif result == TypeError:
            return jsonify(msg=output.CHECK_DATA_TYPE_ERROR), 400
        elif result == Exception:
            return jsonify(msg=output.CHECK_DATA_TYPE_ERROR), 400
        return result

    def near_store(self, latitude, longitude):
        # 근처 5키로 매장으로 하자 !
        meter = 5000
        result = self.storedao.get_near_store(latitude=latitude, longitude=longitude, meter=meter)

        if result == NoResultFound:
            return jsonify(msg=output.NO_RESULT_ERROR), 404
        elif result == DataError:
            return jsonify(msg=output.CHECK_DATA_TYPE_ERROR), 400
        elif result == TypeError:
            return jsonify(msg=output.CHECK_DATA_TYPE_ERROR), 400
        elif result == Exception:
            return jsonify(msg=output.UNEXPECTED_ERROR), 400
        return result

    # 선택한 가게정보 전부 불러오기
    def get_store_info(self, store_id):
        result = self.storedao.get_store_info(store_id=store_id)
        if result == NoResultFound:
            return jsonify(msg=output.NO_RESULT_ERROR), 404
        elif result == DataError:
            return jsonify(msg=output.CHECK_DATA_TYPE_ERROR), 400
        elif result == Exception:
            return jsonify(msg=output.UNEXPECTED_ERROR), 400
        return result

    def create_new_menu(self, payload, store_id):
        if payload['category_id']:
            category_id = payload['category_id']
        else:
            category_id = uuid.uuid4()
            category_name = payload['category_name']
            create_cate = self.storedao.create_category(category_id=category_id,
                                                        category_name=category_name)
            if create_cate == IntegrityError:
                return IntegrityError

        new_menu_id = uuid.uuid4()
        menu = payload['menus']

        check_list = ["name", "price", "profile", "profile_img", "sale_status"]

        for check in check_list:
            if check not in menu:
                return jsonify(msg=output.NOTHING_PARAMS_ERROR), 400

        name = menu['name']
        price = menu['price']
        profile = menu['profile']
        profile_img = menu['profile_img']
        sale_status = menu['sale_status']

        result = self.storedao.create_menu(menu_id=new_menu_id,
                                           name=name,
                                           price=price,
                                           profile=profile,
                                           profile_img=profile_img,
                                           sale_status=sale_status,
                                           category_id=category_id,
                                           store_id=store_id)
        if result == IntegrityError:
            return jsonify(msg=output.DATABASE_ERROR), 400
        elif result == DataError:
            return jsonify(msg=output.CHECK_DATA_TYPE_ERROR), 400
        elif result == Exception:
            return jsonify(msg=output.UNEXPECTED_ERROR), 400
        return result

    def create_new_option(self, payload, store_id):
        new_option_id = uuid.uuid4()
        if 'option_name' not in payload:
            return jsonify(msg=output.NOTHING_PARAMS_ERROR), 400
        elif 'extra_price' not in payload:
            return jsonify(msg=output.NOTHING_PARAMS_ERROR), 400

        option_name = payload['option_name']
        extra_price = payload['extra_price']
        result = self.storedao.create_option(option_id=new_option_id,
                                             store_id=store_id,
                                             option_name=option_name,
                                             extra_price=extra_price)
        if result == IntegrityError:
            return jsonify(msg=output.DATABASE_ERROR), 400
        elif result == DataError:
            return jsonify(msg=output.CHECK_DATA_TYPE_ERROR), 400
        elif result == Exception:
            return jsonify(msg=output.UNEXPECTED_ERROR), 400

        return result

    def get_all_info(self, store_id):
        result = self.storedao.get_all(store_id=store_id)
        if result == NoResultFound:
            return jsonify(msg=output.NO_RESULT_ERROR), 404
        elif result == Exception:
            return jsonify(msg=output.UNEXPECTED_ERROR), 400

        return result

    def all_menus_by_category(self, store_id,category_id, off_set, limit):
        result = self.storedao.get_all_menus(store_id=store_id, category_id=category_id,
                                             off_set=off_set, limit=limit)

        if result == NoResultFound:
            return jsonify(msg=output.NO_RESULT_ERROR), 404
        elif result == DataError:
            return jsonify(msg=output.CHECK_DATA_TYPE_ERROR), 400
        elif result == Exception:
            return jsonify(msg=output.UNEXPECTED_ERROR), 400

        return result

    def all_option(self, store_id):
        result = self.storedao.get_all_option(store_id=store_id)

        if result == NoResultFound:
            return jsonify(msg=output.NO_RESULT_ERROR), 404
        elif result == DataError:
            return jsonify(msg=output.CHECK_DATA_TYPE_ERROR), 400
        elif result == Exception:
            return jsonify(msg=output.UNEXPECTED_ERROR), 400

        return result

    def delete_store_info(self, store_id):
        result = self.storedao.delete_store(store_id=store_id)
        if result is IntegrityError:
            return jsonify(msg=output.DATABASE_ERROR), 400
        elif result is Exception:
            return jsonify(msg=output.UNEXPECTED_ERROR), 400
        return result

    def get_all_store(self, off_set, limit):
        result = self.storedao.all_store(off_set=off_set, limit=limit)
        if result is NoResultFound:
            return jsonify(msg=output.NO_RESULT_ERROR), 404
        elif result is Exception:
            return jsonify(msg=output.UNEXPECTED_ERROR), 400
        return result

    def get_store_by_word(self, words, off_set, limit):
        if not words:
            return jsonify(msg=output.NOTHING_PARAMS_ERROR), 400
        if not off_set:
            off_set = null()
        elif not limit:
            limit = null()

        result = self.storedao.search_store(words=words, off_set=off_set, limit=limit)
        if result is NoResultFound:
            return jsonify(msg=output.NO_RESULT_ERROR), 404
        elif result is Exception:
            return jsonify(msg=Exception), 400
        return result

    def modify_new_menu(self, store_id, menu_id, payload):
        result = self.storedao.modify_menu(store_id=store_id, menu_id=menu_id, payload=payload)
        return result

    def modify_new_option(self, store_id, option_id, payload):
        result = self.storedao.modify_option(store_id=store_id, option_id=option_id, payload=payload)
        return result

