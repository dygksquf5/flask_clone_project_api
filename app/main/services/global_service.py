from sqlalchemy import inspect

from app.main.models.user_dao import Users

from app.main import db
from app.main import jwt
from app.main import jwt_redis_blocklist


# 이부분이 공식문서 참조,  object 리스트 dict 로 바꾸기
def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def get_user_info(user_id):
    user_info = db.session.query(Users).filter(Users.uuid == user_id).one()
    return user_info

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Users.query.filter_by(uuid=identity).one_or_none()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None
