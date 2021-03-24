from flask import Blueprint, request, Response, jsonify, g

# main
from werkzeug.utils import secure_filename
from app.main import output

from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user


board_bp = Blueprint("board_bp", __name__, url_prefix='/board')


def board_endpoint(board_service):
    # 스토리 작성할 수 있는 부분
    @board_bp.route("/content/<int:store_id>", methods=['POST'])
    @jwt_required()
    def board(store_id):
        try:
            user_board = request.json
            user_id = current_user.uuid
            return board_service.new_board(user_id, store_id, user_board)
        except Exception as err:
            return jsonify({'msg': err}), 400

    # 게시판 사진 업로드부분, 디비 저장하지 않고 s3에 업로드 후 url만 반환.
    @board_bp.route("/content/img", methods=['POST'])
    @jwt_required()
    def board_img():
        try:
            if 'image' not in request.files:
                return 'There is no file', 404

            board_image = request.files['image']

            if board_image.filename == '':
                return jsonify({'msg' : output.NOTHING_FOUND }), 404

            filename = secure_filename(board_image.filename)
            image_url = board_service.save_board_image(board_image, filename)
            return image_url
        except Exception as err:
            return jsonify({'msg': err}), 400

    # 지정 스토어 스토리 단 사람들 사진파일 , 인피닛스크롤 -> off, lim
    @board_bp.route("/image-get/store/<int:store_id>/off/<int:off_set>/lim/<int:limit>", methods=['GET'])
    def board_img_get_by_store(store_id, off_set, limit):
        try:
            return board_service.get_board_img(store_id, off_set, limit)
        except Exception as err:
            return jsonify({'msg': err}), 400

    # 댓글 달 수 있는부분 - 게시글 지정
    @board_bp.route('/comment/<int:board_id>', methods=['POST'])
    @jwt_required()
    def comment(board_id):
        try:
            user_comment = request.json
            user_id = current_user.uuid
            return board_service.new_comment(user_id, board_id, user_comment)
        except Exception as err:
            return jsonify({'msg': err}), 400

    # 사용자가 작성한 게시글 불러오기
    @board_bp.route("/board-get", methods=['GET'])
    @jwt_required()
    def get_board():
        try:
            return board_service.get_board()
        except Exception as err:
            return jsonify({'msg': err}), 400

    # 게시글 좋아요
    @board_bp.route("/board-like/<int:board_id>", methods=['POST'])
    @jwt_required()
    def like_board(board_id):
        try:
            user_id = current_user.uuid
            return board_service.like_board(user_id, board_id)
        except Exception as err:
            return jsonify({'msg': err}), 400

    # 게시글 좋아요 취소
    @board_bp.route("/board-unlike/<int:board_id>", methods=['POST'])
    @jwt_required()
    def unlike_board(board_id):
        try:
            return board_service.unlike_board(board_id)
        except Exception as err:
            return jsonify({'msg': err }), 400
