from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import *
from datetime import *
from sqlalchemy import or_, and_
from dateutil.relativedelta import relativedelta
import re


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return redirect(url_for(f'views.user', id=current_user.id))


@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    if request.method == 'POST':
        print(request.form)
        current_user.avatar_url = request.form.get('avatar_url')
        current_user.name = request.form.get('name')
        current_user.cccd = request.form.get('cccd')
        current_user.email = request.form.get('email')
        current_user.phone = request.form.get('phone')
        current_user.address = request.form.get('address')
        current_user.stk = request.form.get('stk')
        current_user.bank_id = request.form.get('bank_id')

        dob_str = request.form.get('dob')
        current_user.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

        db.session.commit()
        flash("Chỉnh sửa thông tin thành công!", category='success')

    banks = Bank.query.all()
    bank_list = []
    for bank in banks:
        if current_user.bank_id == bank.id:
            user_bank_shortName = bank.shortName
        bank_data = {
            'id': bank.id,
            'name': bank.name,
            'code': bank.code,
            'bin': bank.bin,
            'shortName': bank.shortName,
            'logo': bank.logo,
            'swift_code': bank.swift_code
        }
        bank_list.append(bank_data)

    return render_template('profile.html', user=current_user, bank_list=bank_list, user_bank_shortName=user_bank_shortName)


@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():

    if request.method == 'POST':
        currentPassword = request.form.get('currentPassword')
        newPassword = request.form.get('newPassword')
        confirmPassword = request.form.get('confirmPassword')

        if not check_password_hash(current_user.password, currentPassword):
            flash('Mật khẩu hiện tại không chính xác!', category='error')
            return render_template('settings.html', user=current_user)
        elif len(newPassword) < 8:
            flash('Mật khẩu mới phải có ít nhất 8 kí tự!', category='error')
            return render_template('settings.html', user=current_user)
        elif not bool(re.search(r'\d', newPassword)):
            flash('Mật khẩu mới phải có ít nhất 1 số!', category='error')
            return render_template('settings.html', user=current_user)
        elif not bool(re.search(r'[A-Z]', newPassword)):
            flash('Mật khẩu mới phải có ít nhất 1 kí tự viết hoa!', category='error')
            return render_template('settings.html', user=current_user)
        elif not bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', newPassword)):
            flash('Mật khẩu mới phải có ít nhất 1 kí tự đặt biệt!', category='error')
            return render_template('settings.html', user=current_user)
        elif not newPassword==confirmPassword:
            flash('Mật khẩu mới phải trùng với mật khẩu xác nhận!', category='error')
            return render_template('settings.html', user=current_user)
        else:
            current_user.password = generate_password_hash(newPassword)
            db.session.commit()
            flash('Cập nhập mật khẩu mới thành công!', category='success')
        
    return render_template('settings.html', user=current_user)


@views.route('/bank', methods=['GET', 'POST'])
@login_required
def bank():

    if request.method == 'POST':
        form_id = request.form.get('form_id')

        if form_id == 'form-add':
            name = request.form.get('name')
            shortName = request.form.get('shortName')
            code = request.form.get('code')
            bin = request.form.get('bin')
            swift_code = request.form.get('swift_code')

            new_bank = Bank(name=name, shortName=shortName, code=code, bin=bin, swift_code=swift_code)

            db.session.add(new_bank)
            db.session.commit()
            flash("Thêm ngân hàng mới thành công!", category='success')

        if form_id == 'form-edit':
            id = request.form.get('edit-id')
            bank = Bank.query.get(id)
            
            if bank:
                bank.name = request.form.get('edit-name')
                bank.shortName = request.form.get('edit-shortName')
                bank.code = request.form.get('edit-code')
                bank.bin = request.form.get('edit-bin')
                bank.swift_code = request.form.get('edit-swift_code')

                db.session.commit()
                flash("Chỉnh sửa thông tin ngân hàng thành công!", category='success')
            else:
                flash("Ngân hàng không còn tồn tại trên hệ thống.", category='error')

    banks = Bank.query.all()
    bank_list = []
    for bank in banks:
        bank_data = {
            'id': bank.id,
            'name': bank.name,
            'code': bank.code,
            'bin': bank.bin,
            'shortName': bank.shortName,
            'logo': bank.logo,
            'swift_code': bank.swift_code
        }
        bank_list.append(bank_data)

    return render_template('bank.html', user=current_user, bank_list=bank_list)


@views.route('/bank/delete/<int:id>', methods=['POST'])
@login_required
def delete_bank(id):
    bank = Bank.query.get(id)
    if bank:
        db.session.delete(bank)
        db.session.commit()
        flash("Xoá ngân hàng thành công!", category='success')
    else:
        flash("Ngân hàng không còn tồn tại trên hệ thống.", category='error')
    return redirect(url_for('views.bank'), user=current_user)


@views.route('/staff', methods=['GET', 'POST'])
@login_required
def staff():
    if request.method == 'POST':
        form_id = request.form.get('form_id')

        if form_id == 'form-add':
            name = request.form.get('name')
            address = request.form.get('address')
            phone = request.form.get('phone')
            cccd = request.form.get('cccd')
            email = request.form.get('email')
            stk = request.form.get('stk')
            bank_id = request.form.get('bank_id')

            dob_str = request.form.get('dob')
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

            new_staff = User(name=name, address=address, phone=phone, cccd=cccd, email=email, dob=dob, role="staff",
                             password=generate_password_hash('A@123456'), stk=stk, bank_id=bank_id)

            db.session.add(new_staff)
            db.session.commit()
            flash("Thêm nhân viên mới thành công!", category='success')

        if form_id == 'form-edit':
            id = request.form.get('edit-id')
            staff = User.query.get(id)
            
            if staff:
                staff.name = request.form.get('edit-name')
                staff.address = request.form.get('edit-address')
                staff.phone = request.form.get('edit-phone')
                staff.cccd = request.form.get('edit-cccd')
                staff.email = request.form.get('edit-email')
                staff.stk = request.form.get('edit-stk')
                staff.bank_id = request.form.get('edit-bank_id')

                dob_str = request.form.get('edit-dob')
                staff.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

                db.session.commit()
                flash("Chỉnh sửa thông tin nhân viên thành công!", category='success')
            else:
                flash("Nhân viên không còn tồn tại trên hệ thống.", category='error')

    staffs = User.query.filter_by(role='staff').all()
    staff_list = []
    for staff in staffs:

        bank = Bank.query.get(staff.bank_id)

        staff_data = {
            'id': staff.id,
            'name': staff.name,
            'email': staff.email,
            'phone': staff.phone,
            'address': staff.address,
            'cccd': staff.cccd,
            'dob': staff.dob.strftime("%d/%m/%Y"),
            'avatar_url': staff.avatar_url,
            'stk': staff.stk,
            'bank_id': staff.bank_id,
            'bank_shortName': bank.shortName
        }
        staff_list.append(staff_data)

    banks = Bank.query.all()
    bank_list = []
    for bank in banks:
        bank_data = {
            'id': bank.id,
            'name': bank.name,
            'code': bank.code,
            'shortName': bank.shortName,
        }
        bank_list.append(bank_data)

    return render_template('staff.html', user=current_user, staff_list=staff_list, bank_list=bank_list)


@views.route('/staff/delete/<int:id>', methods=['POST'])
@login_required
def delete_staff(id):
    staff = User.query.get(id)
    if staff:
        db.session.delete(staff)
        db.session.commit()
        flash("Xoá nhân viên thành công!", category='success')
    else:
        flash("Nhân viên không còn tồn tại trên hệ thống.", category='error')
    return redirect(url_for('views.staff'), user=current_user)


@views.route('/staff/<int:id>', methods=['GET', 'POST'])
@login_required
def staff_details(id):

    if request.method == 'POST':
        form_id = request.form.get('form_id')
        
        if form_id == 'form-edit':
            # id = request.form.get('edit-id')
            staff = User.query.get(id)

            if staff:
                staff.name = request.form.get('edit-name')
                staff.address = request.form.get('edit-address')
                staff.phone = request.form.get('edit-phone')
                staff.cccd = request.form.get('edit-cccd')
                staff.email = request.form.get('edit-email')
                staff.stk = request.form.get('edit-stk')
                staff.bank_id = request.form.get('edit-bank_id')

                dob_str = request.form.get('edit-dob')
                
                staff.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

                db.session.commit()
                flash("Chỉnh sửa thông tin nhà cung cấp thành công!", category='success')
            else:
                flash("Nhà cung cấp không còn tồn tại trên hệ thống.", category='error')

    staff = User.query.get(id)
    if staff:
        bank = Bank.query.get(staff.bank_id)
        staff_data = {
            'id': staff.id,
            'name': staff.name,
            'email': staff.email,
            'phone': staff.phone,
            'address': staff.address,
            'cccd': staff.cccd,
            'dob': staff.dob.strftime("%d/%m/%Y"),
            'stk': staff.stk,
            'bank_id': staff.bank_id,
            'bank_shortName': bank.shortName,
            'bank_bin': bank.bin
        }

    banks = Bank.query.all()
    bank_list = []
    for bank in banks:
        bank_data = {
            'id': bank.id,
            'name': bank.name,
            'code': bank.code,
            'bin': bank.bin,
            'shortName': bank.shortName,
            'logo': bank.logo,
            'swift_code': bank.swift_code
        }
        bank_list.append(bank_data)

    return render_template('staffDetails.html', user=current_user, staff=staff_data, bank_list=bank_list)


@views.route('/bao-cao-gio', methods=['GET'])
@login_required
def bcgio():
    today = date.today()
    return redirect(url_for(f'views.bao_cao_gio', y=today.year, m=today.month, d=today.day))


@views.route('/bao-cao-gio/<int:y>-<int:m>-<int:d>', methods=['GET', 'POST'])
@login_required
def bao_cao_gio(y, m, d):
    try:
        now = datetime.now()
        ddate = datetime.strptime(f'{y}-{m}-{d}', '%Y-%m-%d').date()
        time_1130 = datetime.combine(ddate, datetime.min.time()).replace(hour=11, minute=40, second=0, microsecond=0)
        time_1700 = datetime.combine(ddate, datetime.min.time()).replace(hour=17, minute=10, second=0, microsecond=0)

        if now > time_1700:
            render_table = 0
        elif now > time_1130:
            render_table = 1
        else:
            render_table = 2

        staffs = User.query.all()
        for staff in staffs:
            if Hour_report.query.filter(and_( Hour_report.user_id == staff.id, or_(Hour_report.time == time_1130, Hour_report.time == time_1700))).all():
                continue
            else:
                user_id = staff.id
                new_report_1130 = Hour_report(user_id=user_id, time=time_1130)
                db.session.add(new_report_1130)
                new_report_1700 = Hour_report(user_id=user_id, time=time_1700)
                db.session.add(new_report_1700)
                db.session.commit()

        if request.method == 'POST':
            form_id = request.form.get('form_id')

            if form_id == 'form-1130':
                user_id = request.form.get('user_id')
                report = Hour_report.query.filter_by(user_id=user_id, time=time_1130).first()
                if report:
                    report.cost = request.form.get('cost')
                    report.phoneNumber = request.form.get('phoneNumber')
                    report.revenue = request.form.get('revenue')
                    db.session.commit()
                flash("Báo cáo thành công!", category='success')

            if form_id == 'form-1700':
                user_id = request.form.get('user_id')
                report = Hour_report.query.filter_by(user_id=user_id, time=time_1700).first()
                if report:
                    report.cost = request.form.get('cost')
                    report.phoneNumber = request.form.get('phoneNumber')
                    report.revenue = request.form.get('revenue')
                    db.session.commit()
                flash("Báo cáo thành công!", category='success')

        staffs = User.query.all()
        staff_list = []
        for staff in staffs:
            staff_data = {
                'id': staff.id,
                'name': staff.name,
                'avatar_url': staff.avatar_url,
            }
            staff_list.append(staff_data)
        
        reports = Hour_report.query.filter(or_(Hour_report.time == time_1130, Hour_report.time == time_1700)).all()
        report_list = []

        for report in reports:
            report_data = {
                'user_id': report.user_id,
                'time': '1130' if report.time==time_1130 else '1700',
                'cost': f'{report.cost:,}',
                'phoneNumber': f'{report.phoneNumber:,}',
                'costPerPhone': f'{int(round(report.cost/report.phoneNumber, 0) if report.phoneNumber != 0 else 0):,}',
                'revenue': f'{report.revenue:,}',
                'cpqc': f'{round(report.cost/report.revenue * 100 if report.revenue != 0 else 0, 2):,}',
                'roat': f'{round(report.revenue/report.cost if report.cost != 0 else 0, 2):,}'
            }
            report_list.append(report_data)

        return render_template('bao-cao-gio.html', user=current_user, staff_list=staff_list, report_list=report_list, ddate=ddate, render_table=render_table)
    except:
        return render_template('404.html')


@views.route('/bao-cao-ngay', methods=['GET'])
@login_required
def bcngay():
    today = date.today()
    yesterday = today - timedelta(days=1)
    return redirect(url_for(f'views.bao_cao_ngay', y=yesterday.year, m=yesterday.month, d=yesterday.day))


@views.route('/bao-cao-ngay/<int:y>-<int:m>-<int:d>', methods=['GET', 'POST'])
@login_required
def bao_cao_ngay(y, m, d):
    # try:
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    ddate = datetime.strptime(f'{y}-{m}-{d}', '%Y-%m-%d').date()
    time_1000 = datetime.combine(ddate, datetime.min.time()).replace(hour=10, minute=10, second=0, microsecond=0)

    if yesterday > time_1000:
        render_table = False
    else:
        render_table = True

    staffs = User.query.all()
    for staff in staffs:
        if Day_report.query.filter_by(user_id=staff.id, time=time_1000).all():
            continue
        else:
            user_id = staff.id
            new_report = Day_report(user_id=user_id, time=time_1000)
            db.session.add(new_report)
            db.session.commit()

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        report = Day_report.query.filter_by(user_id=user_id, time=time_1000).first()
        if report:
            report.newRevenue = request.form.get('newRevenue')
            report.advanceBudget = request.form.get('advanceBudget')
            report.realBudget = request.form.get('realBudget')
            report.phoneNumber = request.form.get('phoneNumber')
            report.mess = request.form.get('mess')
            db.session.commit()
        flash("Báo cáo thành công!", category='success')

    staffs = User.query.all()
    staff_list = []
    for staff in staffs:
        staff_data = {
            'id': staff.id,
            'name': staff.name,
            'avatar_url': staff.avatar_url,
        }
        staff_list.append(staff_data)
    
    reports = Day_report.query.filter_by(time=time_1000).all()
    report_list = []

    for report in reports:
        report_data = {
            'user_id': report.user_id,
            'newRevenue': f'{report.newRevenue:,}',
            'advanceBudget': f'{report.advanceBudget:,}',
            'realBudget': f'{report.realBudget:,}',
            'phoneNumber': f'{report.phoneNumber:,}',
            'mess': f'{report.mess:,}',
            'cpp': f'{int(round(report.realBudget/report.phoneNumber, 0) if report.phoneNumber != 0 else 0):,}',
            'cpr': f'{float(round(report.advanceBudget/report.newRevenue*100, 2) if report.newRevenue != 0 else 0):,}',
            'ppm': f'{float(round(report.phoneNumber/report.mess*100, 2) if report.mess != 0 else 0):,}',
            'bpm': f'{int(round(report.realBudget/report.mess, 0) if report.mess != 0 else 0):,}',
        }
        report_list.append(report_data)

    return render_template('bao-cao-ngay.html', user=current_user, staff_list=staff_list, report_list=report_list, ddate=ddate, fdate=f'{d}/{m}/{y}', render_table=render_table)
    # except:
    #     return render_template('404.html')


@views.route('/bao-cao-bai-test', methods=['GET'])
@login_required
def bcbtest():
    today = date.today()
    one_month_before = today - relativedelta(months=1)
    return redirect(url_for(f'views.bao_cao_bai_test', yb=one_month_before.year, mb=one_month_before.month, dbb=one_month_before.day, y=today.year, m=today.month, d=today.day))


@views.route('/bao-cao-bai-test/<int:yb>-<int:mb>-<int:dbb>-<int:y>-<int:m>-<int:d>', methods=['GET', 'POST'])
@login_required
def bao_cao_bai_test(yb, mb, dbb, y, m, d):
    try:
        date1 = datetime.strptime(f'{yb}-{mb}-{dbb}', '%Y-%m-%d').date()
        date2 = datetime.strptime(f'{y}-{m}-{d}', '%Y-%m-%d').date()

        if request.method == 'POST':
            form_id = request.form.get('form_id')

            if form_id == 'form-date-filter':
                dateInput1 = request.form.get('dateInput1')
                dateInput2 = request.form.get('dateInput2')

                date1 = datetime.strptime(dateInput1, '%Y-%m-%d').date()
                date2 = datetime.strptime(dateInput2, '%Y-%m-%d').date()

                return redirect(url_for(f'views.bao_cao_bai_test', yb=date1.year, mb=date1.month, dbb=date1.day, y=date2.year, m=date2.month, d=date2.day))

            if form_id == 'form-add':
                user_id = request.form.get('user_id')
                link = request.form.get('link')
                content = request.form.get('content')
                type = request.form.get('type')
                budget = request.form.get('budget') if request.form.get('budget') != '' else 0
                cpm = request.form.get('cpm') if request.form.get('cpm') != '' else 0
                cpc = request.form.get('cpc') if request.form.get('cpc') != '' else 0
                ctr = request.form.get('ctr') if request.form.get('ctr') != '' else 0
                cpa = request.form.get('cpa') if request.form.get('cpa') != '' else 0
                order = request.form.get('order') if request.form.get('order') != '' else 0
                review = request.form.get('review')
                new_post = Post(user_id=user_id, time=date.today(), link=link, content=content,
                                type=type, budget=budget, cpm=cpm, cpc=cpc, ctr=ctr, cpa=cpa, order=order, review=review)
                db.session.add(new_post)
                db.session.commit()
                flash("Thêm bài test mới thành công!", category='success')

            if form_id == 'form-edit':
                id = request.form.get('edit-post_id')
                post = Post.query.get(id)
                if post:
                    post.link = request.form.get('edit-link')
                    post.content = request.form.get('edit-content')
                    post.type = request.form.get('edit-type')
                    post.budget = request.form.get('edit-budget') if request.form.get('budget') != '' else 0
                    post.cpm = request.form.get('edit-cpm') if request.form.get('cpm') != '' else 0
                    post.cpc = request.form.get('edit-cpc') if request.form.get('cpc') != '' else 0
                    post.ctr = request.form.get('edit-ctr') if request.form.get('ctr') != '' else 0
                    post.cpa = request.form.get('edit-cpa') if request.form.get('cpa') != '' else 0
                    post.order = request.form.get('edit-order') if request.form.get('order') != '' else 0
                    post.review = request.form.get('edit-review')
                    db.session.commit()
                    flash("Chỉnh sửa bài test thành công!", category='success')

        staffs = User.query.all()
        staff_list = []
        for staff in staffs:
            staff_data = {
                'id': staff.id,
                'name': staff.name,
                'avatar_url': staff.avatar_url,
            }
            staff_list.append(staff_data)
        
        posts = Post.query.filter(Post.time.between(date1, date2)).all()
        post_list = []

        for post in posts:
            post_data = {
                'id': post.id,
                'user_id': post.user_id,
                'time': post.time.strftime("%d/%m/%Y"),
                'link': post.link,
                'type': post.type,
                'content': post.content,
                'budget': f'{post.budget:,}',
                'cpm': f'{post.cpm:,}',
                'cpc': f'{post.cpc:,}',
                'ctr': round(post.ctr, 2),
                'cpa': f'{post.cpa:,}',
                'cpPerCpa': f'{int(round(post.budget/post.cpa, 0) if post.cpa != 0 else 0):,}',
                'order': f'{post.order:,}',
                'cpPerOrder': f'{int(round(post.budget/post.order, 0) if post.order != 0 else 0):,}',
                'review': post.review,
            }
            post_list.append(post_data)

        return render_template('bao-cao-bai-test.html', user=current_user, staff_list=staff_list, post_list=post_list, date1=date1, date2=date2)
    except:
        return render_template('404.html')


@views.route('/post/delete/<int:id>', methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get(id)
    if post:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('views.bao-cao-bai-test'), user=current_user)


@views.route('/user/<int:id>', methods=['GET', 'POST'])
@login_required
def user(id):
    try:
        now = datetime.now()
        staff = User.query.get(id)

        reports = Day_report.query.filter(Day_report.user_id == id, Day_report.time <= now).all()
        report_list = []
        for report in reports:
            report_data = {
                'id': report.id,
                'time': report.time.strftime('%d/%m/%Y'),
                'newRevenue': f'{report.newRevenue:,}',
                'advanceBudget': f'{report.advanceBudget:,}',
                'realBudget': f'{report.realBudget:,}',
                'phoneNumber': f'{report.phoneNumber:,}',
                'mess': f'{report.mess:,}',
                'cpp': f'{int(round(report.realBudget/report.phoneNumber, 0) if report.phoneNumber != 0 else 0):,}',
                'cpr': f'{float(round(report.newRevenue/report.realBudget*100, 2) if report.realBudget != 0 else 0):,}',
                'ppm': f'{float(round(report.phoneNumber/report.mess*100, 2) if report.mess != 0 else 0):,}',
                'bpm': f'{int(round(report.realBudget/report.mess, 0) if report.mess != 0 else 0):,}',
            }
            report_list.append(report_data)

        return render_template('user.html', user=current_user, staff=staff, report_list=report_list)
    except:
        return render_template('404.html')


