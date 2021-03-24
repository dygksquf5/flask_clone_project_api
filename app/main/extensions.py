from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_redis import Redis
from celery import Celery


db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
jwt_redis_blocklist = Redis()
celery = Celery()


