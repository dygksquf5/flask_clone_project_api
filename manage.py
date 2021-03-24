import atexit
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app.main import create_app
from app.main.extensions import db
from apscheduler.schedulers.background import BackgroundScheduler
from app.main.scheduler import sensor


app = create_app(register_blueprints=True, config_name='dev')

app.app_context().push()


manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


# 스케줄러
scheduler = BackgroundScheduler()
scheduler.add_job(func=sensor, trigger="interval", seconds=30) # 30초 간격!
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


@manager.command
def run():
    app.run()


if __name__ == '__main__':
    manager.run()
