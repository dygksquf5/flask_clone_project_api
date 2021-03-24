from flask import Blueprint, request, jsonify, g, json
from werkzeug.utils import secure_filename

from app.main import output

store_bp = Blueprint('store_bp', __name__, url_prefix='/store')


def store_endpoint(store_service):
    @store_bp.route('/new', methods=['POST'])
    def register_store():
        try:
            if 'profile_img' not in request.files:
                profile_img = None
            else:
                profile_img = request.files['profile_img']

            new_store = request.form

            return store_service.register_store(new_store=new_store,
                                                profile_img=profile_img)
        except Exception:
            return jsonify(msg=output.UNEXPECTED_ERROR), 400

    @store_bp.route('/<uuid:store_id>', methods=['DELETE'])
    def delete_store(store_id):
        return store_service.delete_store_info(store_id=store_id)

    @store_bp.route('/info', methods=['GET'])
    def store_info():
        store_id = request.args.get('store_id')
        return store_service.get_store_info(store_id)

    # new & near 의 가변적 params로 매장리스트 뽑아내기.
    @store_bp.route('/list/<sort>', methods=['GET'])
    def get_new_store(sort):
        if sort == "new":
            off_set = request.args.get('off')
            limit = request.args.get('lim')
            return store_service.new_stores(off_set, limit)
        elif sort == "near":
            latitude = request.args.get('latitude')
            longitude = request.args.get('longitude')
            return store_service.near_store(latitude=latitude, longitude=longitude)
        elif sort == 'all':
            off_set = request.args.get('off')
            limit = request.args.get('lim')
            return store_service.get_all_store(off_set=off_set, limit=limit)
        elif sort == "search":
            off_set = request.args.get('off')
            limit = request.args.get('lim')
            words = request.args.get('words')
            return store_service.get_store_by_word(words=words, off_set=off_set, limit=limit)
        else:
            return jsonify(msg=output.INVALID_ACCESS), 405

    # 매장이 가지고 있는 모든 음료 정보 가져오기
    @store_bp.route('/<uuid:store_id>/all-beverage', methods=['GET'])
    def get_all_beverage_info(store_id):
        return store_service.get_all_info(store_id)

    @store_bp.route('/<uuid:store_id>/menus', methods=['POST'])
    def create_menu(store_id):
        payload = request.json
        return store_service.create_new_menu(payload=payload,
                                             store_id=store_id)

    @store_bp.route('/<uuid:store_id>/option', methods=['POST'])
    def create_option(store_id):
        payload = request.json

        return store_service.create_new_option(payload=payload,
                                               store_id=store_id)

    @store_bp.route('/<uuid:store_id>/menus/<uuid:menu_id>', methods=['PATCH'])
    def modify_menus(store_id, menu_id):
        payload = request.json
        return store_service.modify_new_menu(store_id=store_id,
                                             menu_id=menu_id,
                                             payload=payload)

    @store_bp.route('/<uuid:store_id>/option/<uuid:option_id>', methods=['PATCH'])
    def modify_option(store_id, option_id):
        payload = request.json
        return store_service.modify_new_option(store_id=store_id,
                                               option_id=option_id,
                                               payload=payload)


    @store_bp.route('/<uuid:store_id>/menus/category/<uuid:category_id>', methods=['GET'])
    def get_all_menus(store_id , category_id):
        off_set = request.args.get('off')
        limit = request.args.get('lim')
        return store_service.all_menus_by_category(store_id=store_id, category_id=category_id,
                                                   off_set=off_set, limit=limit)

    @store_bp.route('/option/<uuid:store_id>', methods=['GET'])
    def get_all_option(store_id):
        return store_service.all_option(store_id)


    # 근처 매장 찾기 !
    @store_bp.route('/list/near', methods=['GET'])
    def get_near_store():
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        return store_service.near_store(latitude=latitude, longitude=longitude)


