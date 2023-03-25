from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash
from email.mime.multipart import MIMEMultipart
from website.auth import epassword, me
from website.models import ClaimLoan
from email.mime.text import MIMEText
from website import db
import datetime
import smtplib

views = Blueprint('views', __name__)


@views.route('/')
def home():
    if not current_user.is_anonymous:
        loan = ClaimLoan.query.filter_by(user_id=current_user.id).first()
        return render_template('index.html', user=current_user, loan=loan)
    return render_template('index.html', user=current_user)


def send_loan_mail(new_loan, type):
    you = current_user.email
    message = MIMEMultipart()
    message['from'] = me
    message['to'] = you
    if type == "personal":
        message['subject'] = "MatchFinance Personal Loan"
    if type == "student":
        message['subject'] = "MatchFinance Student Loan"
    if type == "business":
        message['subject'] = "MatchFinance Business Loan"
    message.attach(MIMEText(f"Dear, {current_user.firstName}"
                            f"\nYou have been credited a loan of GHc{new_loan.amount_taken}"
                            f"\nYou would pay an amount GHc{new_loan.left_to_pay}"
                            f"\nThis loan is to be payed by {new_loan.time_span}"
                            f"\nThank you for banking with us."))
    try:
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.ehlo()
        server.starttls()
        server.login(me, epassword)
        server.sendmail(me, you, message.as_string())
        server.quit()
        flash('Sending loan, check email for confirmation', category='success')
        return redirect(url_for("views.home"))

    except Exception as e:
        flash('Could not connect, please try again', category='error')


@login_required
def loan_creation(loan_type):
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        purpose = request.form.get('loanpurpose')
        amount = request.form.get('loanamount')
        guarantor = request.form.get('collateral')
        duration = request.form.get('duration')
        rate = 0.1
        period = datetime.timedelta(int(duration) * 31)
        now = datetime.date.today()
        span = now + period
        new_loan = ClaimLoan(
            name = name,
            email=current_user.email,
            user_id=current_user.id,
            amount_taken=amount,
            time_span=span,
            purpose=purpose,
            left_to_pay=float(amount) + (rate * float(amount) * float(duration)),
            collateral=guarantor
        )
        send_loan_mail(new_loan, type=loan_type)
        db.session.add(new_loan)
        db.session.commit()
        return redirect(url_for("views.home"))


@views.route('/personal_loans', methods=['GET', 'POST'])
@login_required
def personal_loans():
    loan = ClaimLoan.query.filter_by(user_id=current_user.id).first()
    if loan:
        userloan = loan.amount_taken
        return render_template('personal_loans.html', userloan=userloan, user=current_user)
    loan_creation("personal")
    return render_template('personal_loans.html', user=current_user)


@views.route('/business_loans', methods=['GET', 'POST'])
@login_required
def business_loans():
    loan = ClaimLoan.query.filter_by(user_id=current_user.id).first()
    if loan:
        userloan = loan.amount_taken
        return render_template('business_loans.html', userloan=userloan, user=current_user)
    loan_creation("business")
    return render_template('business_loans.html', user=current_user)


@views.route('/student_loans')
@login_required
def student_loans():
    loan = ClaimLoan.query.filter_by(user_id=current_user.id).first()
    if loan:
        userloan = loan.amount_taken
        return render_template('student_loans.html', userloan=userloan, user=current_user)
    loan_creation('student')
    return render_template('student_loans.html', user=current_user)
