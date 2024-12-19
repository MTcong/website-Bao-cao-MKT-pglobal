from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from . import db
import json
from .models import *
from datetime import *


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html', user=current_user)


@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@views.route('/customer', methods=['GET', 'POST'])
@login_required
def customer():

    if request.method == 'POST':
        form_id = request.form.get('form_id')

        if form_id == 'form-add':
            name = request.form.get('name')
            address = request.form.get('address')
            phone = request.form.get('phone')
            cccd = request.form.get('cccd')
            email = request.form.get('email')
            dob_str = request.form.get('dob')
            note = request.form.get('note')

            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

            new_customer = Customer(name=name, address=address, phone=phone, cccd=cccd, email=email, dob=dob, note=note)

            db.session.add(new_customer)
            db.session.commit()
            flash("Thêm khách hàng mới thành công!", category='success')

        if form_id == 'form-edit':
            id = request.form.get('edit-id')
            customer = Customer.query.get(id)

            if customer:
                customer.name = request.form.get('edit-name')
                customer.address = request.form.get('edit-address')
                customer.phone = request.form.get('edit-phone')
                customer.cccd = request.form.get('edit-cccd')
                customer.email = request.form.get('edit-email')
                customer.note = request.form.get('edit-note')
                
                dob_str = request.form.get('edit-dob')
                
                customer.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

                db.session.commit()
                flash("Chỉnh sửa thông tin khách hàng thành công!", category='success')
            else:
                flash("Khách hàng không còn tồn tại trên hệ thống.", category='error')

    customers = Customer.query.all()
    customer_list = []
    for customer in customers:
        customer_data = {
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone,
            'cccd': customer.cccd,
            'address': customer.address,
            'dob': customer.dob.strftime("%d/%m/%Y"),
            'note': customer.note
        }
        customer_list.append(customer_data)

    return render_template('customer.html', user=current_user, customer_list=customer_list)


@views.route('/customer/delete/<int:id>', methods=['POST'])
@login_required
def delete_customer(id):
    customer = Customer.query.get(id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        flash("Xoá khách hàng thành công!", category='success')
    else:
        flash("Khách hàng không còn tồn tại trên hệ thống.", category='error')
    return redirect(url_for('views.customer'), user=current_user)


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


@views.route('/supplier', methods=['GET', 'POST'])
@login_required
def supplier():

    if request.method == 'POST':
        form_id = request.form.get('form_id')

        if form_id == 'form-add':
            name = request.form.get('name')
            address = request.form.get('address')
            phone = request.form.get('phone')
            cccd = request.form.get('cccd')
            email = request.form.get('email')
            dob_str = request.form.get('dob')
            stk = request.form.get('stk')
            bank_id = request.form.get('bank_id')
            note = request.form.get('note')

            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

            new_supplier = Supplier(name=name, address=address, phone=phone, cccd=cccd, email=email, dob=dob, stk=stk, bank_id=bank_id, note=note)

            db.session.add(new_supplier)
            db.session.commit()
            flash("Thêm nhà cung cấp mới thành công!", category='success')

        if form_id == 'form-edit':
            id = request.form.get('edit-id')
            supplier = Supplier.query.get(id)
            print(request.form)
            if supplier:
                supplier.name = request.form.get('edit-name')
                supplier.address = request.form.get('edit-address')
                supplier.phone = request.form.get('edit-phone')
                supplier.cccd = request.form.get('edit-cccd')
                supplier.email = request.form.get('edit-email')
                supplier.stk = request.form.get('edit-stk')
                supplier.bank_id = request.form.get('edit-bank_id')
                supplier.note = request.form.get('edit-note')

                dob_str = request.form.get('edit-dob')
                
                supplier.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

                db.session.commit()
                flash("Chỉnh sửa thông tin nhà cung cấp thành công!", category='success')
            else:
                flash("Nhà cung cấp không còn tồn tại trên hệ thống.", category='error')

    suppliers = Supplier.query.all()
    supplier_list = []
    for supplier in suppliers:

        bank = Bank.query.get(supplier.bank_id)

        supplier_data = {
            'id': supplier.id,
            'name': supplier.name,
            'email': supplier.email,
            'phone': supplier.phone,
            'address': supplier.address,
            'cccd': supplier.cccd,
            'dob': supplier.dob.strftime("%d/%m/%Y"),
            'stk': supplier.stk,
            'bank_id': supplier.bank_id,
            'bank_shortName': bank.shortName,
            'note': supplier.note,
        }
        supplier_list.append(supplier_data)

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

    return render_template('supplier.html', user=current_user, supplier_list=supplier_list, bank_list=bank_list)


@views.route('/supplier/delete/<int:id>', methods=['POST'])
@login_required
def delete_supplier(id):
    supplier = Supplier.query.get(id)
    if supplier:
        db.session.delete(supplier)
        db.session.commit()
        flash("Xoá nhà cung cấp thành công!", category='success')
    else:
        flash("Nhà cung cấp không còn tồn tại trên hệ thống.", category='error')
    return redirect(url_for('views.supplier'), user=current_user)


@views.route('/supplier/<int:id>', methods=['GET', 'POST'])
@login_required
def supplier_details(id):

    if request.method == 'POST':
        form_id = request.form.get('form_id')
        
        if form_id == 'form-edit':
            # id = request.form.get('edit-id')
            supplier = Supplier.query.get(id)

            if supplier:
                supplier.name = request.form.get('edit-name')
                supplier.address = request.form.get('edit-address')
                supplier.phone = request.form.get('edit-phone')
                supplier.cccd = request.form.get('edit-cccd')
                supplier.email = request.form.get('edit-email')
                supplier.stk = request.form.get('edit-stk')
                supplier.bank_id = request.form.get('edit-bank_id')
                supplier.note = request.form.get('edit-note')

                dob_str = request.form.get('edit-dob')
                
                supplier.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

                db.session.commit()
                flash("Chỉnh sửa thông tin nhà cung cấp thành công!", category='success')
            else:
                flash("Nhà cung cấp không còn tồn tại trên hệ thống.", category='error')

    supplier = Supplier.query.get(id)
    if supplier:
        bank = Bank.query.get(supplier.bank_id)
        supplier_data = {
            'id': supplier.id,
            'name': supplier.name,
            'email': supplier.email,
            'phone': supplier.phone,
            'address': supplier.address,
            'cccd': supplier.cccd,
            'dob': supplier.dob.strftime("%d/%m/%Y"),
            'stk': supplier.stk,
            'bank_id': supplier.bank_id,
            'bank_shortName': bank.shortName,
            'bank_bin': bank.bin,
            'note': supplier.note
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

    return render_template('supplierDetails.html', user=current_user, supplier=supplier_data, bank_list=bank_list)


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
            dob_str = request.form.get('dob')

            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

            new_staff = User(name=name, address=address, phone=phone, cccd=cccd, email=email, dob=dob, role="staff", password=generate_password_hash('A@123456'))

            db.session.add(new_staff)
            db.session.commit()
            flash("Thêm nhà cung cấp mới thành công!", category='success')

        if form_id == 'form-edit':
            id = request.form.get('edit-id')
            staff = User.query.get(id)
            
            if staff:
                staff.name = request.form.get('edit-name')
                staff.address = request.form.get('edit-address')
                staff.phone = request.form.get('edit-phone')
                staff.cccd = request.form.get('edit-cccd')
                staff.email = request.form.get('edit-email')

                dob_str = request.form.get('edit-dob')
                
                staff.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

                db.session.commit()
                flash("Chỉnh sửa thông tin nhà cung cấp thành công!", category='success')
            else:
                flash("Nhà cung cấp không còn tồn tại trên hệ thống.", category='error')

    staffs = User.query.filter_by(role='staff').all()
    staff_list = []
    for staff in staffs:
        staff_data = {
            'id': staff.id,
            'name': staff.name,
            'email': staff.email,
            'phone': staff.phone,
            'address': staff.address,
            'cccd': staff.cccd,
            'dob': staff.dob.strftime("%d/%m/%Y")
        }
        staff_list.append(staff_data)

    return render_template('staff.html', user=current_user, staff_list=staff_list)


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


@views.route('/unit', methods=['GET', 'POST'])
@login_required
def unit():

    if request.method == 'POST':
        form_id = request.form.get('form_id')

        if form_id == 'form-add':
            name = request.form.get('name')
            note = request.form.get('note')

            new_unit = Unit(name=name, note=note)
            db.session.add(new_unit)
            db.session.commit()
            flash("Thêm đơn vị mới thành công!", category='success')

        if form_id == 'form-edit':
            id = request.form.get('edit-id')
            unit = Unit.query.get(id)
            
            if unit:
                unit.name = request.form.get('edit-name')
                unit.note = request.form.get('edit-note')

                db.session.commit()
                flash("Chỉnh sửa thông tin đơn vị thành công!", category='success')
            else:
                flash("Đơn vị không còn tồn tại trên hệ thống.", category='error')

    units = Unit.query.all()
    unit_list = []
    for unit in units:
        unit_data = {
            'id': unit.id,
            'name': unit.name,
            'note': unit.note
        }
        unit_list.append(unit_data)

    return render_template('unit.html', user=current_user, unit_list=unit_list)


@views.route('/unit/delete/<int:id>', methods=['POST'])
@login_required
def delete_unit(id):
    unit = Unit.query.get(id)
    if unit:
        db.session.delete(unit)
        db.session.commit()
        flash("Xoá đơn vị thành công!", category='success')
    else:
        flash("Đơn vị không còn tồn tại trên hệ thống.", category='error')
    return redirect(url_for('views.unit'), user=current_user)


@views.route('/ingredient', methods=['GET', 'POST'])
@login_required
def ingredient():

    if request.method == 'POST':
        form_id = request.form.get('form_id')

        if form_id == 'form-add':
            name = request.form.get('name')
            long = request.form.get('long')
            wide = request.form.get('wide')
            high = request.form.get('high')
            buy = request.form.get('buy')
            sale = request.form.get('sale')
            note = request.form.get('note')
            unit_id = request.form.get('unit_id')

            new_ingredient = Ingredient(name=name, long=long, wide=wide, high=high, buy=buy, sale=sale, note=note, unit_id=unit_id)
            db.session.add(new_ingredient)
            db.session.commit()
            flash("Thêm đơn vị mới thành công!", category='success')

        if form_id == 'form-edit':
            id = request.form.get('edit-id')
            ingredient = Ingredient.query.get(id)
            
            if ingredient:
                ingredient.name = request.form.get('edit-name')
                ingredient.long = request.form.get('edit-long')
                ingredient.wide = request.form.get('edit-wide')
                ingredient.high = request.form.get('edit-high')
                ingredient.buy = request.form.get('edit-buy')
                ingredient.sale = request.form.get('edit-sale')
                ingredient.note = request.form.get('edit-note')
                ingredient.unit_id = request.form.get('edit-unit_id')

                db.session.commit()
                flash("Chỉnh sửa thông tin đơn vị thành công!", category='success')
            else:
                flash("Đơn vị không còn tồn tại trên hệ thống.", category='error')

    ingredients = Ingredient.query.all()
    ingredient_list = []
    for ingredient in ingredients:
        unit = Unit.query.get(ingredient.unit_id)
        ingredient_data = {
            'id': ingredient.id,
            'name': ingredient.name,
            'long': ingredient.long,
            'wide': ingredient.wide,
            'high': ingredient.high,
            'buy': ingredient.buy,
            'sale': ingredient.sale,
            'note': ingredient.note,
            'unit_id': ingredient.unit_id,
            'unit_name': unit.name,
        }
        ingredient_list.append(ingredient_data)

    units = Unit.query.all()
    unit_list = []
    for unit in units:
        unit_data = {
            'id': unit.id,
            'name': unit.name,
            'note': unit.note
        }
        unit_list.append(unit_data)

    return render_template('ingredient.html', user=current_user, ingredient_list=ingredient_list, unit_list=unit_list)


@views.route('/ingredient/delete/<int:id>', methods=['POST'])
@login_required
def delete_ingredient(id):
    ingredient = Ingredient.query.get(id)
    if ingredient:
        db.session.delete(ingredient)
        db.session.commit()
        flash("Xoá nguyên liệu thành công!", category='success')
    else:
        flash("Nguyên liệu không còn tồn tại trên hệ thống.", category='error')
    return redirect(url_for('views.ingredient'), user=current_user)