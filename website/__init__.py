from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from datetime import date
from werkzeug.security import generate_password_hash
from faker import Faker


db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask("__name__", template_folder='website/templates', static_folder='website/static')
    app.config['SECRET_KEY'] = 'ajjflajfoc oaenakjcap'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Customer, Bank, Supplier, Unit, Ingredient

    with app.app_context():
        db.create_all()

        try:
            User.create_admin()
            User.create_random_staffs()
            Customer.create_random_customers()
            Bank.create_bank_data()
            Supplier.create_random_suppliers()
            Unit.create_units()
            Ingredient.create_ingredients()
        except Exception as e:
            print(f'Exception: {e}')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = ""
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app