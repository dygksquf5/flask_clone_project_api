from flask import Flask
from flask.json import JSONEncoder

from flask_cors import CORS

from app.main.config import config_by_name
from .extensions import db, jwt, migrate, jwt_redis_blocklist





class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return JSONEncoder.default(self, obj)


def create_app(register_blueprints, config_name=None):
    app = Flask(__name__)
    CORS(app)

    app.json_encoder = CustomJSONEncoder


    if config_name is None:
        app.config.from_object(config_by_name['dev'])
    else:
        app.config.from_object(config_by_name[config_name])

    # 디비 커넥팅
    from app.main.models import board_dao, store_dao, user_dao, menu_dao, order_dao

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    jwt_redis_blocklist.init_app(app)

    # persistence layer
    from .models import UserDao, OrderDao, StoreDao, MenuDao, BoardDao
    usersdao = UserDao(db, board_dao, store_dao, menu_dao, order_dao)
    orderdao = OrderDao(db, board_dao, store_dao, user_dao, menu_dao)
    storedao = StoreDao(db, board_dao, user_dao, menu_dao, order_dao)
    menudao = MenuDao(db, board_dao, store_dao, user_dao, order_dao)
    boarddao = BoardDao(db, store_dao, user_dao, menu_dao, order_dao)

    # business layer
    from .services import UserService, OrderService, StoreService, BoardService
    user_service = UserService(usersdao, app)
    order_service = OrderService(orderdao, app)
    store_service = StoreService(storedao, app)
    board_service = BoardService(db, app)


    from .views.user_view import user_endpoint
    from .views.order_view import order_endpoint
    from .views.store_view import store_endpoint
    from .views.board_view import board_endpoint

    # present layer
    user_endpoint(user_service)
    order_endpoint(order_service)
    store_endpoint(store_service)
    board_endpoint(board_service)

    if register_blueprints:
        app = register_blueprint(app)



    return app



def register_blueprint(app):
    from .views import user_bp, store_bp, order_bp, board_bp

    # blueprint
    app.register_blueprint(user_bp)
    app.register_blueprint(board_bp)
    app.register_blueprint(store_bp)
    app.register_blueprint(order_bp)

    return app

