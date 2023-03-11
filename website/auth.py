from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, logout_user, current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from website.models import User, ClaimLoan, PayLoan
from email.mime.multipart import MIMEMultipart
from werkzeug.utils import secure_filename
from email.mime.text import MIMEText
import mediapipe as mp
import uuid as uuid
import cv2 as cv
from . import db
import smtplib
import random
import json
import os

auth = Blueprint('auth', __name__)

with open(r'password.txt', 'r') as file:
    epassword = file.readline()
    me = file.readline()
    epassword = epassword.rstrip()


def payment_mail(C_user, C_loan, paying):
    you = C_user.email
    message = MIMEMultipart()
    message['subject'] = "MatchFinance has received your payment"
    message['from'] = me
    message['to'] = you
    message.attach(MIMEText(
        f"Dear {C_user.firstName},.\nYou have successfully payed {paying}\nYour remaining dept is {C_loan.left_to_pay - int(paying)}"))
    try:
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.ehlo()
        server.starttls()
        server.login(me, epassword)
        server.sendmail(me, you, message.as_string())
        server.quit()
        C_loan.left_to_pay -= int(paying)
        db.session.commit()
        if C_loan.left_to_pay <= 0:
            db.session.delete(C_loan)
            db.session.commit()
    except Exception as e:
        flash("Could not process form, please try again", category="error")
        return render_template('signup.html', user=current_user)


def send_mail(C_user):
    you = C_user.email
    message = MIMEMultipart()
    message['subject'] = "MatchFinance welcomes you"
    message['from'] = me
    message['to'] = you
    message.attach(MIMEText(f"Your account has been successfully created!\nWelcome {C_user.firstName}.\nYour account "
                            f"number is {C_user.accountNo}\nUse it to log into your account and perform other "
                            f"related actions.\nMatchFinance is here to support you financially."))
    try:
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.ehlo()
        server.starttls()
        server.login(me, epassword)
        server.sendmail(me, you, message.as_string())
        server.quit()
        db.session.add(C_user)
        db.session.commit()
    except Exception as e:
        flash("Could not process form, Please try again", category="error")
        return render_template('signup.html', user=current_user)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        acc_num = request.form.get('account_num')
        password = request.form.get('pass')

        user = User.query.filter_by(accountNo=acc_num).first()
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
    c = current_user
    return render_template('admin.html', now=current_user, pays=PayLoan.query.all(), loans=ClaimLoan.query.all(),
                           users=User.query.all())


@auth.route('/admin_signup', methods=['GET', 'POST'])
@login_required
def admin_signup():
    randNo = random.randint(1000000000, 999999999999)
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
        pic = request.files['pic']
        picname = secure_filename(pic.filename)
        pic_name = f'{str(uuid.uuid1())}_{email}_{picname}'

        if picname.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            pic.save(os.path.join("website/static/profiles/", pic_name))
        else:
            flash('Please upload a picture', category='error')
            return render_template('signup.html', user=current_user)

        mpFace = mp.solutions.face_detection
        face = mpFace.FaceDetection(min_detection_confidence=0.9)
        frame = cv.imread(os.path.join("website/static/profiles/", pic_name))
        gray = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = face.process(gray)
        if results.detections:
            pass
        else:
            flash('Please upload a picture of your face', category='error')
            return render_template('signup.html', user=current_user)

        user = User.query.filter_by(email=email.lower()).first()
        if user:
            flash('Email already exists', category='error')
            return render_template('adminSignup.html', user=current_user)
        if len(password) < 7:
            flash('Password too short, must be at least 7 characters', category='error')
            return render_template('adminSignup.html', user=current_user)
        if password1 != password:
            flash('Password mismatch', category='error')
            return render_template('adminSignup.html', user=current_user)
        else:
            new_user = User(
                firstName=firstName.title(),
                middleName=middleName.title(),
                lastName=lastName.title(),
                phone=phone,
                email=email.lower(),
                img=pic_name,
                accountNo=randNo,
                date_of_birth=date_of_birth,
                ID_number=ID_number,
                is_admin=True,
                password=generate_password_hash(password, method='sha256')
            )
            send_mail(new_user)
            Check = User.query.filter_by(email=email.lower())
            if Check:
                flash('New admin created, check email for login details', category='success')
                return redirect(url_for('auth.admin'))
            else:
                os.remove(os.path.join("website/static/profiles/", pic_name))
                flash('Form could not processed please try again', category='error')
    return render_template('adminSignup.html', user=current_user)


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    randNo = random.randint(1000000000, 999999999999)
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
        ID_type = request.form.get('id_type')
        password = request.form.get('password')
        password1 = request.form.get('password1')
        pic = request.files['pic']
        picname = secure_filename(pic.filename)
        pic_name = f'{str(uuid.uuid1())}_{email}_{picname}'

        if picname.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            pic.save(os.path.join("website/static/profiles/", pic_name))
        else:
            flash('Please upload a picture', category='error')
            return render_template('signup.html', user=current_user)

        mpFace = mp.solutions.face_detection
        face = mpFace.FaceDetection(min_detection_confidence=0.9)
        frame = cv.imread(os.path.join("website/static/profiles/", pic_name))
        gray = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = face.process(gray)
        if results.detections:
            pass
        else:
            flash('Please upload a picture of your face', category='error')
            return render_template('signup.html', user=current_user)

        admin_check = User.query.all()
        if not admin_check:
            superuser = True
        else:
            superuser = False

        user = User.query.filter_by(accountNo=randNo).first()
        if user:
            flash('Could generate accountID, please try again', category='error')
            return render_template('signup.html')

        user = User.query.filter_by(email=email.lower()).first()
        if user:
            flash('Email already exists', category='error')
            return render_template('signup.html', user=current_user)
        if len(password) < 7:
            flash('Password too short, must be at least 7 characters', category='error')
            return render_template('signup.html', user=current_user)
        if password1 != password:
            flash('Password mismatch', category='error')
            return render_template('signup.html', user=current_user)
        else:
            new_user = User(
                firstName=firstName.title(),
                middleName=middleName.title(),
                lastName=lastName.title(),
                address=address,
                city=city,
                ID_type=ID_type,
                state=state,
                phone=phone,
                img=pic_name,
                accountNo=randNo,
                email=email.lower(),
                date_of_birth=date_of_birth,
                ID_number=ID_number,
                is_superuser=superuser,
                is_admin=superuser,
                password=generate_password_hash(password, method='sha256')
            )
            send_mail(new_user)
            Check = User.query.filter_by(email=email.lower())
            if Check:
                flash('Account created, check email for your account number to login.', category='success')
                return redirect(url_for("auth.login"))
            os.remove(os.path.join("website/static/profiles/", pic_name))
            flash('Form could not processed please try again', category='error')
    return render_template('signup.html', user=current_user)


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


@auth.route('/delete-pay', methods=['POST'])
def delete_pay():
    pay = json.loads(request.data)
    payid = pay['payid']
    pay = ClaimLoan.query.get(payid)
    if pay:
        if current_user.is_admin:
            db.session.delete(pay)
            db.session.commit()
    return jsonify({})


@auth.route('/pay_loan', methods=['GET', 'POST'])
@login_required
def pay_loan():
    if request.method == 'POST':
        firstname = request.form.get('fname')
        acc_no = request.form.get('acc_no')
        paying = request.form.get('pay')
        method = request.form.get('payment-method')
        mNumber = request.form.get('mobile_number')
        mName = request.form.get('mobile_name')
        bNumber = request.form.get('bank_name')
        user = User.query.filter_by(accountNo=acc_no).first()
        if not user:
            flash('Account number not found', category='error')
            return render_template('pay_loan.html', user=current_user)
        claimloan = ClaimLoan.query.filter_by(user_id=user.id).first()
        if not claimloan:
            flash('Not in dept', category='error')
            return render_template('pay_loan.html', user=current_user)
        if claimloan.left_to_pay < paying:
            flash('Payment amount exceeded current dept', category='error')
            return render_template('pay_loan.html', user=current_user)
        if (mNumber and mName) or (mNumber or bNumber):
            payment_mail(user, claimloan, paying)
            payloan = PayLoan(
                accountNo=acc_no,
                fname=firstname,
                amount=paying,
                payMethod=method,
                cNumber=mNumber,
                cName=mName,
                bNumber=bNumber
            )
            db.session.add(payloan)
            db.session.commit()
            flash('Payment in process, check email for confirmation', category='success')
            return redirect(url_for("views.home"))
        else:
            flash('Please make sure all rows are filled', category='error')
    return render_template('pay_loan.html', user=current_user)
