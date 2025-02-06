from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class Admin(db.Model, UserMixin):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False) # Hashed password

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    category = db.Column(db.String(100))
    status = db.Column(db.String(20), default="Available")

class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    membership_date = db.Column(db.Date, default=datetime.utcnow)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    borrow_date = db.Column(db.Date, default=datetime.utcnow)
    return_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), default="Borrowed")

    # relationship
    book = db.relationship("Book", backref="transactions")
    member = db.relationship("Member", backref="transactions")
