from flask import Blueprint, g, request

from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user

order_bp = Blueprint('order_bp', __name__, url_prefix='/order')


def order_endpoint(order_service):
    @order_bp.route('/new', methods=['POST'])
    @jwt_required()
    def start_order():
        order_info = request.json
        user_id = current_user.uuid
        return order_service.new_order(order_info, user_id)

    @order_bp.route('/status/<uuid:order_id>', methods=['GET'])
    @jwt_required()
    def get_order_status(order_id):
        user_id = current_user.uuid
        return order_service.check_order_status(user_id=user_id, main_order_id=order_id)

    # 이건 날짜 요청따라 뽑아주기!
    @order_bp.route('/list/detail', methods=['GET'])
    @jwt_required()
    def get_order_detail():
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        user_id = current_user.uuid
        return order_service.order_detail(date_from=date_from, date_to=date_to, user_id=user_id)

    # order status 변경 할 수 있음.
    @order_bp.route('/status', methods=['PATCH'])
    def update_status():
        payload = request.json
        return order_service.change_status(payload=payload)


    @order_bp.route('/<uuid:order_id>/reorder', methods=['POST'])
    @jwt_required()
    def reorder_create(order_id):
        payload = request.json
        user_id = current_user.uuid
        return order_service.reorder(order_id=order_id, payload=payload,user_id=user_id)



    ##### for scheduling #####
    @order_bp.route('/schedule', methods=['GET'])
    def _scheduling_order():
        return order_service.scheduling_order_status()



