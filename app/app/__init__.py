from flask import Flask, render_template, redirect, url_for, session, flash
from flask_mail import Message
from datetime import datetime


# Import extensions
from .extensions import bootstrap
from .extensions import moment
from .extensions import db
from .extensions import mail
from .extensions import login_manager

######################################################
# CONFIGURATION IS SET IN 'config.py' -> config_name #
from .config import config, config_name              #
######################################################

def create_app(config_name='default'):

    app = Flask(__name__)

    # Configurations
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Extensions
    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    from .blueprints.player import player as player_blueprint
    from .blueprints.library import library as library_blueprint
    from .blueprints.main import main as main_blueprint
    app.register_blueprint(library_blueprint)
    app.register_blueprint(player_blueprint)
    app.register_blueprint(main_blueprint)

    from .blueprints.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .blueprints.profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint, url_prefix='/profile')

    # Import Models
    from .models import User, Role

    @app.cli.command('db_create')
    def db_create():
        db.create_all()
    
    @app.cli.command('db_drop')
    def db_drop():
        db.drop_all()

    @app.cli.command('db_seed')
    def db_seed():
        admin_role = Role(name='Admin')
        mod_role = Role(name='Moderator')
        user_role = Role(name='User')

        user_john = User(username='John', role=admin_role)

        user_marco = User(email = 'marcof787@gmail.com',
                          username = 'marco',
                          confirmed = True,
                          password = '123',
                          role = admin_role)

        db.session.add_all([admin_role, mod_role, user_role, user_marco])
        db.session.commit()
        
    return app

