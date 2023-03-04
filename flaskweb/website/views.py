from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash
import datetime

from website import db
from website.models import ClaimLoan

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('index.html', user=current_user)

@login_required
def loan_creation():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        phone = request.form.get('phone')
        email = request.form.get('email')
        purpose = request.form.get('loanpurpose')
        amount = request.form.get('loanamount')
        collate = request.form.get('collateral')
        duration = request.form.get('duration')
        password = request.form.get('password')
        if (firstname.title() != current_user.firstName.title()) and (phone != current_user.phone) and (
                email.lower() != current_user.email.lower()) and not (
                check_password_hash(current_user.password, password)):
            flash('Data given does not match current account credentials', category='error')
            return render_template('personal_loans.html', user=current_user)
        else:
            rate = 1.2
            period = datetime.timedelta(int(duration) * 31)
            now = datetime.date.today()
            span = now + period
            new_loan = ClaimLoan(
                email=email.lower(),
                user_id=current_user.id,
                amount=amount,
                time_span=span,
                purpose=purpose,
                left_to_pay=rate * float(amount) * float(duration),
                collateral=collate
            )
            db.session.add(new_loan)
            db.session.commit()
            flash('Preparing Loan', category='success')
            return redirect(url_for('views.home'))


@views.route('/personal_loans', methods=['GET', 'POST'])
@login_required
def personal_loans():
    loan_creation()
    loan = ClaimLoan.query.filter_by(user_id=current_user.id).first()
    if loan:
        userloan = loan.amount
        return render_template('personal_loans.html', userloan=userloan, user=current_user)
    else:
        return render_template('personal_loans.html', user=current_user)


@views.route('/business_loans', methods=['GET', 'POST'])
@login_required
def business_loans():
    loan_creation()
    loan = ClaimLoan.query.filter_by(user_id=current_user.id).first()
    if loan:
        userloan = loan.amount
        return render_template('business_loans.html', userloan=userloan, user=current_user)
    else:
        return render_template('business_loans.html', user=current_user)


@views.route('/student_loans')
@login_required
def student_loans():
    loan_creation()
    loan = ClaimLoan.query.filter_by(user_id=current_user.id).first()
    if loan:
        userloan = loan.amount
        return render_template('student_loans.html', userloan=userloan, user=current_user)
    else:
        return render_template('student_loans.html', user=current_user)


@views.route('/pay_loan')
@login_required
def pay_loan():
    return render_template('pay_loan.html', user=current_user)


@views.route('/debt_consolidation')
@login_required
def debt_consolidation():
    return render_template('debt_consolidation.html', user=current_user)
