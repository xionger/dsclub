from flask import Flask
#from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

from config import app_config


#Initialize database
db = SQLAlchemy()

login_manager = LoginManager()

#Create the app
def create_app(config_name):
	app = Flask(__name__, instance_relative_config=True)

	app.config.from_object(app_config[config_name])
	app.config.from_pyfile('config.py')

	Bootstrap(app)

	#db.app = app

	db.init_app(app)

	#scheduler = APScheduler()
	#scheduler.init_app(app)
	#scheduler.start()

	login_manager.init_app(app)
	login_manager.login_message = "You must login to access the pages."
	login_manager.login_view = "auth.login"

	migrate = Migrate(app, db)

	from app import models 

	from .admin import admin as admin_blueprint
	app.register_blueprint(admin_blueprint, url_prefix='/admin')

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	from .event import event as event_blueprint
	app.register_blueprint(event_blueprint)

	from .home import home as home_blueprint
	app.register_blueprint(home_blueprint)

	from .message import message as message_blueprint
	app.register_blueprint(message_blueprint)

	from .project import project as project_blueprint
	app.register_blueprint(project_blueprint)

	from .forum import forum as forum_blueprint
	app.register_blueprint(forum_blueprint)

	return app