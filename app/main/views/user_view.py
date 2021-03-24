from flask import Blueprint, request, jsonify, current_app, g, send_file
from werkzeug.utils import secure_filename
from app.main import output
from sqlalchemy.exc import IntegrityError

from app.main import jwt
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_jwt_extended import current_user
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jti

from app.main import jwt_redis_blocklist

from app.main.tasks import what



user_bp = Blueprint('user_bp', __name__, url_prefix='/user')



def user_endpoint(user_service):

    @user_bp.route("/ping", methods=['GET'])
    def ping():
        what.delay()
        return jsonify(msg='pong'), 200

    # 약관
    @user_bp.route('/sign-up-terms', methods=['GET'])
    def sign_up_terms():
        return user_service.get_terms()

    @user_bp.route("/sign-up", methods=['POST'])
    def sign_up():
        if 'profile_img' not in request.files:
            profile_img = None
        else:
            profile_img = request.files['profile_img']

        new_user = request.form

        return user_service.new_user(new_user=new_user, profile_img=profile_img)

    @user_bp.route("/current", methods=['GET'])
    @jwt_required()
    def get_user_info():
        return user_service.get_user_info_by_id(user_id=current_user.uuid)

    @user_bp.route("/login", methods=['POST'])
    def login():
        login_info = request.json
        return user_service.user_login(login_info)

    @user_bp.route("/logout", methods=["DELETE"])
    @jwt_required()
    def logout():
        refresh_token = request.headers.get('Refresh-token')
        jti = get_jwt()["jti"]
        jti_re = get_jti(refresh_token)
        jwt_redis_blocklist.set(jti, "", ex=current_app.config['ACCESS_EXPIRES'])
        jwt_redis_blocklist.set(jti_re, "", ex=current_app.config['REFRESH_EXPIRES'])
        return jsonify(msg=output.REVOKED_SUCCESS)

    @user_bp.route("/refresh", methods=['POST'])
    @jwt_required(refresh=True)
    def refresh():
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return jsonify(access_token=access_token)

    @user_bp.route("/image", methods=['PATCH'])
    @jwt_required()
    def upload_profile_img():
        user_id = current_user.uuid

        if 'profile_img' not in request.files:
            return jsonify(msg=output.NOTHING_PARAMS_ERROR), 404

        profile_img = request.files['profile_img']

        if profile_img.filename == '':
            return jsonify(msg=output.NOTHING_PARAMS_ERROR), 404

        filename = secure_filename(profile_img.filename)
        return user_service.update_profile_picture(profile_img, filename, user_id)


    # 정보수정, 패스워드, 이름, 결제패스워스 update 가능, body에 어떤 prams 넘기냐에 따라 다르게 작동
    @user_bp.route("/info", methods=['PATCH'])
    @jwt_required()
    def modify_user_info():
        payload = request.json
        return user_service.update_user_info(user=current_user, payload=payload)

    # 유저삭제
    @user_bp.route("/out", methods=['DELETE'])
    @jwt_required()
    def delete_user_info():
        # 토큰 revoke
        user = current_user
        result = user_service.delete_user(user=user)
        if result == IntegrityError:
            return jsonify(msg=output.DATABASE_ERROR), 400
        elif result == Exception:
            return jsonify(msg=Exception), 400

        refresh_token = request.headers.get('Refresh-token')
        jti = get_jwt()["jti"]
        jti_re = get_jti(refresh_token)
        jwt_redis_blocklist.set(jti, "", ex=current_app.config['ACCESS_EXPIRES'])
        jwt_redis_blocklist.set(jti_re, "", ex=current_app.config['REFRESH_EXPIRES'])

        return result


    # pay password 새롭게 만들거나 check 가능한 api
    @user_bp.route("/pay-password", methods=['POST'])
    @jwt_required()
    def set_or_check_pay_password():
        data = request.json
        return user_service.new_or_check_pay_password(data)


