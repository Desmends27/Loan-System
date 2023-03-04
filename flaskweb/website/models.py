from . import db
from flask_login import UserMixin
import datetime


class ClaimLoan(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Integer, nullable=False)
    left_to_pay = db.Column(db.Integer, nullable=False)
    date_taken = db.Column(db.Date, default=datetime.date.today())
    time_span = db.Column(db.Date, nullable=False)
    purpose = db.Column(db.String(200), nullable=False)
    collateral = db.Column(db.String(200), nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    firstName = db.Column(db.String(50))
    middleName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    address = db.Column(db.String(50))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    phone = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    date_of_birth = db.Column(db.String(12))
    ID_number = db.Column(db.Integer, unique=True)
    password = db.Column(db.String(150), nullable=False)
    is_superuser = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    loans = db.relationship('ClaimLoan')
