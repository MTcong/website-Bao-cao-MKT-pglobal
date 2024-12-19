from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')



        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Đăng nhập thành công!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Sai mật khẩu. Vui lòng thử lại!', category='error')
        else:
            flash('Địa chỉ email này chưa đăng ký tài khoản!', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Địa chỉ email này đã đăng ký tài khoản!", category='error')
            return redirect(url_for('auth.register'))

        if password1 != password2:
            flash("Xác nhận mật khẩu không thành công. Vui lòng thử lại!", category='error')
        elif len(password1) < 8:
            flash("Mật khẩu phải dài hơn 8 kí tự!", category='error')
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Tạo tài khoản thành công!", category='success')
            return redirect(url_for('views.home'))

    return render_template('register.html', user=current_user)