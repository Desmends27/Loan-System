from flask_login import UserMixin
from . import db
import datetime


class PayLoan(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    accountNo = db.Column(db.Integer)
    fname = db.Column(db.String(50))
    amount = db.Column(db.Integer)
    payMethod = db.Column(db.String(30))
    date_payed = db.Column(db.Date, default=datetime.date.today())
    cNumber = db.Column(db.Integer)
    cName = db.Column(db.String(50))
    bNumber = db.Column(db.String(50))
    pay_id = db.Column(db.Integer, db.ForeignKey('claimloan.id'))


class ClaimLoan(db.Model):
    name = db.Column(db.String(50))
    pay = db.relationship('PayLoan', cascade='all,delete-orphan')
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount_taken = db.Column(db.Integer, nullable=False)
    to_pay = db.Column(db.Integer, default=0)
    left_to_pay = db.Column(db.Integer)
    date_taken = db.Column(db.Date, default=datetime.date.today())
    time_span = db.Column(db.Date, nullable=False)
    purpose = db.Column(db.String(200), nullable=False)
    sent = db.Column(db.String, default="False")
    collateral = db.Column(db.String(200), nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    firstName = db.Column(db.String(50))
    middleName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    accountNo = db.Column(db.Integer, unique=True)
    address = db.Column(db.String(50))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    phone = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    date_of_birth = db.Column(db.String(12))
    img = db.Column(db.String(), nullable=False)
    ID_number = db.Column(db.Integer, unique=True)
    ID_type = db.Column(db.String(30))
    password = db.Column(db.String(150), nullable=False)
    is_superuser = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    loans = db.relationship('ClaimLoan', cascade='all,delete-orphan')