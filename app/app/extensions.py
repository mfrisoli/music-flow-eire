from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail
from flask_login import LoginManager


# All Extensions need to be initialized in main app/__init__.py
bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
mail = Mail()

login_manager = LoginManager()
# This will redirect un-authorized users to /auth/login
login_manager.login_view = 'auth.login'