from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from datetime import date
from werkzeug.security import generate_password_hash
from faker import Faker
import pytz


TIMEZONE = 'Asia/Ho_Chi_Minh'
tz = pytz.timezone(TIMEZONE)


db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask("__name__", template_folder='website/templates', static_folder='website/static')
    app.config['SECRET_KEY'] = 'jfpamcoakr ncldprnkea'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Bank, Post

    with app.app_context():
        db.create_all()

        try:
            User.create_admin()
            User.create_random_staffs()
            Bank.create_bank_data()
            Post.create_random_post()
        except Exception as e:
            print(f'Exception: {e}')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = ""
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app