from flask import Blueprint, request, jsonify, render_template
from models import db, Book, Member, Transaction
from datetime import datetime

app = Blueprint("routes", __name__)

@app.route("/")
def index():
    return render_template("index.html")  # Load home page

@app.route("/books")
def books_page():
    books = Book.query.all()
    return render_template("books.html", books=books)  # Pass data to template

@app.route("/members")
def members_page():
    members = Member.query.all()
    return render_template("members.html", members=members)

@app.route("/borrow")
def borrow_page():
    books = Book.query.filter_by(status="Available").all()
    members = Member.query.all()
    return render_template("borrow.html", books=books, members=members)
