from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import date
from faker import Faker
from werkzeug.security import generate_password_hash
import requests, random


# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(150), unique=True)
    phone = db.Column(db.String(20), default="")
    cccd = db.Column(db.String(20), default="")
    password = db.Column(db.String(150))
    address = db.Column(db.String(10000), default="")
    role = db.Column(db.String(10000), default="staff")
    dob = db.Column(db.Date(), default=date(2000, 1, 1))
    avatar_url = db.Column(db.String(10000), default='../static/sneat/assets/img/avatars/1.png')

    def create_admin():
        admin_user = User(
                name='Admin',
                email='admin@plc.com',
                phone='',
                cccd='',
                password=generate_password_hash('admin@plc.com'),
                address='',
                role='admin',
                dob=date(2000, 1, 1),
                avatar_url = '../static/sneat/assets/img/avatars/1.png'
            )
        db.session.add(admin_user)
        db.session.commit()

    def create_random_staffs():
        fake = Faker()
        for _ in range(15):
            staff = User(
                name=fake.name(),
                email=fake.unique.email(),
                phone=fake.phone_number(),
                cccd=random.randint(100000000000, 999999999999),
                password=generate_password_hash('staff'),
                address=fake.address(),
                role='staff',
                dob=fake.date_of_birth(tzinfo=None, minimum_age=20, maximum_age=60),
                avatar_url = '../static/sneat/assets/img/avatars/1.png'
            )
            db.session.add(staff)
        db.session.commit()


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(150), unique=True)
    phone = db.Column(db.String(20), default="")
    cccd = db.Column(db.String(20), default="")
    address = db.Column(db.String(10000), default="")
    dob = db.Column(db.Date(), default=date(2000, 1, 1))
    note = db.Column(db.String(10000), default="")

    def create_random_customers():
        fake = Faker()
        for _ in range(15):
            customer = Customer(
                name=fake.name(),
                email=fake.unique.email(),
                phone=fake.phone_number(),
                cccd=random.randint(100000000000, 999999999999),
                address=fake.address(),
                dob=fake.date_of_birth(tzinfo=None, minimum_age=20, maximum_age=60),
                note=fake.text(max_nb_chars=20)
            )
            db.session.add(customer)
        db.session.commit()


class Bank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    code = db.Column(db.String(100), unique=True)
    bin = db.Column(db.String(10))
    shortName = db.Column(db.String(1000), default="")
    logo = db.Column(db.String(1000), default="")
    swift_code = db.Column(db.String(10), default="")
    suppliers = db.relationship('Supplier')

    def create_bank_data():
        try:
            response = requests.get('https://api.vietqr.io/v2/banks')
            if response.status_code==200:
                data = response.json()['data']
                for bank in data:
                    new_bank = Bank(
                        id = bank['id'],
                        name = bank['name'],
                        code = bank['code'],
                        bin = bank['bin'],
                        shortName = bank['shortName'],
                        logo = bank['logo'],
                        swift_code = bank['swift_code']
                    )
                    db.session.add(new_bank)
            db.session.commit()
        except Exception as e:
            print(f"Exception: {e}")
        

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(150), unique=True)
    phone = db.Column(db.String(20), default="")
    address = db.Column(db.String(10000), default="")
    cccd = db.Column(db.String(20), default="")
    dob = db.Column(db.Date(), default=date(2000, 1, 1))
    note = db.Column(db.String(10000), default="")
    stk = db.Column(db.String(20), default="")
    bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'))

    def create_random_suppliers():
        fake = Faker()
        for _ in range(15):
            supplier = Supplier(
                name=fake.name(),
                email=fake.unique.email(),
                phone=fake.phone_number(),
                address=fake.address(),
                cccd=random.randint(100000000000, 999999999999),
                dob=fake.date_of_birth(tzinfo=None, minimum_age=20, maximum_age=60),
                note=fake.text(max_nb_chars=20),
                stk=str(random.randint(100000, 9999999999999999)),
                bank_id = random.randint(1, 20)
            )
            db.session.add(supplier)
        db.session.commit()


class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    note = db.Column(db.String(10000), default="")
    ingredients = db.relationship('Ingredient')

    def create_units():
        data = [
            {'name': 'Cái', 'note': ''},
            {'name': 'm2', 'note': 'mét vuông'},
            {'name': 'cm', 'note': 'cen ti mét'},
            {'name': 'Cuộn', 'note': ''},
            {'name': 'cm2', 'note': 'cen ti mét vuông'},
        ]
        for unit in data:
            new_unit = Unit(name=unit['name'], note=unit['note'])
            db.session.add(new_unit)
        db.session.commit()


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    long = db.Column(db.Integer, default=0)
    wide = db.Column(db.Integer, default=0)
    high = db.Column(db.Integer, default=0)
    buy = db.Column(db.Integer, default=0)
    sale = db.Column(db.Integer, default=0)
    note = db.Column(db.String(10000), default="")
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))

    def create_ingredients():
        data = [
            {'name': 'Xốp', 'long': 0, 'wide': 0, 'high': 0, 'buy': 0, 'sale':0, 'note': '', 'unit_id': 3},
            {'name': 'Bìa cứng', 'long': 0, 'wide': 0, 'high': 0, 'buy': 0, 'sale':0, 'note': '', 'unit_id': 1},
            {'name': 'Băng dính', 'long': 10, 'wide': 10, 'high': 10, 'buy': 0, 'sale':0, 'note': '', 'unit_id': 4},
            {'name': 'giấy', 'long': 0, 'wide': 0, 'high': 0, 'buy': 0, 'sale':0, 'note': '', 'unit_id': 2},
        ]
        for ingredient in data:
            new_ingredient = Ingredient(name=ingredient['name'],
                                        long=ingredient['long'],
                                        wide=ingredient['wide'],
                                        high=ingredient['high'],
                                        buy=ingredient['buy'],
                                        sale=ingredient['sale'],
                                        note=ingredient['note'],
                                        unit_id=ingredient['unit_id'],)
            db.session.add(new_ingredient)
        db.session.commit()