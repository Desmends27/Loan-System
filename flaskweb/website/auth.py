from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from website.models import User, ClaimLoan
from flask_login import login_required, logout_user, current_user, login_user
import json

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        acc_num = request.form.get('account_num')
        password = request.form.get('pass')

        user = User.query.filter_by(ID_number=acc_num).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=False)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Account does not exist', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/admin')
@login_required
def admin():
    print(User.query.all())
    return render_template('admin.html', now=current_user, loans=ClaimLoan.query.all(), users=User.query.all())


@auth.route('/admin_signup', methods=['GET', 'POST'])
@login_required
def admin_signup():
    if request.method == 'POST':
        firstName = request.form.get('fname')
        lastName = request.form.get('lname')
        middleName = request.form.get('mname')
        phone = request.form.get('phone')
        email = request.form.get('email')
        date_of_birth = request.form.get('dob')
        ID_number = request.form.get('IDno')
        password = request.form.get('password')
        password1 = request.form.get('password1')

        invalid = 0
        user = User.query.filter_by(email=email.lower()).first()
        if user:
            flash('Email already exists', category='error')
            return render_template('signup.html')
        # check validity
        # if len(password) < 7:
        #     flash('Password too short, must be at least 7 characters', category='error')
        if password1 != password:
            flash('Password mismatch', category='error')
            return render_template('signup.html')
        else:
            new_user = User(
                firstName=firstName.title(),
                middleName=middleName.title(),
                lastName=lastName.title(),
                phone=phone,
                email=email.lower(),
                date_of_birth=date_of_birth,
                ID_number=ID_number,
                is_admin=True,
                password=generate_password_hash(password, method='sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            flash('New admin created', category='success')
            return redirect(url_for('auth.admin'))
    return render_template('adminSignup.html', user=current_user)


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        firstName = request.form.get('fname')
        lastName = request.form.get('lname')
        middleName = request.form.get('mname')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        phone = request.form.get('phone')
        email = request.form.get('email')
        date_of_birth = request.form.get('dob')
        ID_number = request.form.get('IDno')
        password = request.form.get('password')
        password1 = request.form.get('password1')

        admin_check = User.query.all()
        print(admin_check)
        if not admin_check:
            superuser = True
        else:
            superuser = False

        # check if account exists
        invalid = 0
        user = User.query.filter_by(email=email.lower()).first()
        if user:
            flash('Email already exists', category='error')
            return render_template('signup.html')
        # check validity
        # if len(password) < 7:
        #     flash('Password too short, must be at least 7 characters', category='error')
        if password1 != password:
            flash('Password mismatch', category='error')
            return render_template('signup.html')
        else:
            new_user = User(
                firstName=firstName.title(),
                middleName=middleName.title(),
                lastName=lastName.title(),
                address=address,
                city=city,
                state=state,
                phone=phone,
                email=email.lower(),
                date_of_birth=date_of_birth,
                ID_number=ID_number,
                is_superuser=superuser,
                is_admin=superuser,
                password=generate_password_hash(password, method='sha256')
            )
            print(new_user)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created', category='success')
            return redirect(url_for('auth.send-email'))
    return render_template('signup.html', user=current_user)


@auth.route('/send-email')
@login_required
def send_mail():
    me = 'ansongandy04@gmail.com'
    you = 'barry2000allen5@gmail.com'
    password = 'avexjyhlxjkhhhwo'
    message = MIMEMultipart()
    message['subject'] = "Test"
    message['from'] = me
    message['to'] = you
    message.attach(MIMEText("This is a test.\nDo not reply"))
    try:
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.ehlo()
        server.starttls()
        server.login(me, password)
        server.sendmail(me, you, message.as_string())
        server.quit()
        print(f'Email sent to {current_user.email}')
        flash(f'Account created, Email sent to {current_user.email}', category='success')
        return redirect(url_for('views.home'))
    except Exception as e:
        flash('Account created', category='success')
        print(f'Error in sending message: {e}')
        flash('Account created, could not send email', category='error')
        return redirect(url_for('views.home'))


@auth.route('/delete-user', methods=['POST'])
def delete_user():
    user = json.loads(request.data)
    userid = user['userid']
    user = User.query.get(userid)
    if user:
        if current_user.is_superuser:
            db.session.delete(user)
            db.session.commit()
    return jsonify({})


@auth.route('/delete-loan', methods=['POST'])
def delete_loan():
    loan = json.loads(request.data)
    loanid = loan['loanid']
    loan = ClaimLoan.query.get(loanid)
    if loan:
        if current_user.is_admin:
            db.session.delete(loan)
            db.session.commit()
    return jsonify({})
