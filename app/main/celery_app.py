from app.main import create_app

from celery import Celery


class CeleryConfig:
    CELERY_IMPORTS = ('app.main.tasks')
    CELERY_TASK_RESULT_EXPIRES = 30

    CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'Asia/Seoul'
    CELERY_ENABLE_UTC = False

    CELERYBEAT_SCHEDULE = {
        "time_scheduler": {
            "task": "app.main.tasks.what",
            "schedule": 60.0

        }

    }


def make_celery(app):
    celery = Celery(app.import_name,
                    broker='amqp://yosuniiiii:rladygks123!@localhost:5672/',
                    backend='amqp://yosuniiiii:rladygks123!@localhost:5672/'
                    )

    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    celery.config_from_object(CeleryConfig)
    return celery


app = create_app( register_blueprints=False, config_name='dev')
celery = make_celery(app)

