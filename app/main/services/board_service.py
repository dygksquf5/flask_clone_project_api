from flask import g, request, jsonify, json
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError


from app.main.models.board_dao import Board
from app.main import output
from app.main.models.board_dao import Comment


import pandas as pd
import boto3


class BoardService:
    def __init__(self, db, app):
        self.db = db
        self.app = app

    # 사진파일 저장 s3 (AWS)
    def save_board_image(self, picture, filename):
        try:
            # s3 커넥트 관련
            s3 = boto3.client(
                "s3",
                aws_access_key_id=self.app.config['S3_ACCESS_KEY'],
                aws_secret_access_key=self.app.config['S3_SECRET_KEY']
            )

            s3.upload_fileobj(
                picture,
                self.app.config['S3_BUCKET'],
                filename
            )
            image_url = f"{self.app.config['S3_BUCKET_URL']}{filename}"

            return jsonify({'msg': output.SUCCESS,
                            'img_url': image_url}), 200

        except Exception as err:
            return jsonify({'msg': err}), 401

    # 인피닛스크롤 위해 off, lim
    def get_board_img(self, store_id, off_set, limit):
        try:
            board_info = self.db.session.query(Board).filter(Board.store_id == store_id) \
                .order_by(Board.create_at.desc()).offset(off_set).limit(limit)

            results = []
            for board in board_info:
                results.append({
                    'id': board.id,
                    'store_id': board.store_id,
                    'image_url': board.image
                })

            return jsonify(results), 200
        except Exception as err:
            jsonify({'msg': err}), 400

    def new_board(self, user_id, store_id, user_board):
        try:
            try:
                content = user_board['content']
                image = user_board['image']
            except KeyError:
                return jsonify({'msg': output.CHECK_KEY }), 500

            if len(content) > 300:
                return '글자수 제한 300', 400
            try:
                new_content = Board(user_id=user_id, content=content, store_id=store_id, image=image)
                self.db.session.add(new_content)
                self.db.session.commit()
                return jsonify({'msg': output.SUCCESS }), 200
            except IntegrityError:
                self.db.session.rollback()
                return jsonify({'msg': output.INVALID_ACCESS }), 400

        except Exception as err:
            return jsonify({'msg': err}), 400

    def new_comment(self, user_id, board_id, user_comment):
        try:
            comment = user_comment['comment']

            if len(comment) > 300:
                return jsonify({'msg' : output.CHECK_KEY }), 400
            try:
                new_comment = Comment(content=comment, user_id=user_id, board_id=board_id)
                self.db.session.add(new_comment)
                self.db.session.commit()
                return jsonify({'msg': output.SUCCESS }), 200
            except IntegrityError:
                self.db.session.rollback()
                return jsonify({'msg': output.CHECK_KEY }), 400

        except Exception as err:
            return jsonify({'msg': err}), 400

    def get_board(self):
        user_id = g.user_id
        timeline = self.db.session.query(Board).filter(Board.user_id == user_id)

        df = pd.read_sql(timeline.statement, timeline.session.bind)
        results = json.loads(df.to_json(orient='records'))

        return jsonify(results), 200

    def like_board(self, user_id, board_id):
        try:
            board = self.db.session.query(Board).filter(Board.id == board_id).one()
            if user_id == board.user_id:
                return jsonify({'msg': output.INVALID_ACCESS }), 400
            else:
                try:
                    board.like.append(g.user)
                    self.db.session.commit()
                    return jsonify({'msg': output.SUCCESS }), 200
                except IntegrityError:
                    self.db.session.rollback()
                    return jsonify({'msg': output.INVALID_ACCESS }), 400

        except Exception as err:
            return jsonify({'msg': err}), 400

    def unlike_board(self, board_id):
        try:
            try:
                board = self.db.session.query(Board).filter(Board.id == board_id).one()
            except IntegrityError:
                return jsonify({'msg': output.INVALID_ACCESS }), 400
            try:
                board.like.remove(g.user)
                self.db.session.commit()
                return jsonify({'msg': output.SUCCESS }), 200
            except Exception as err:
                return jsonify({'msg': output.NOTHING_FOUND }), 404

        except Exception as err:
            return jsonify({'msg': err}), 400
