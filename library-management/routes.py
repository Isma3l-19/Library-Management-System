from flask import Blueprint, request, jsonify
from models import db, Book, Member, Transaction
from datetime import datetime

# Create a Blueprint
app = Blueprint("routes", __name__)

@app.route("/")
def index():
    return "Welcome to Library Management System"

@app.route("/books", methods=["GET"])
def get_books():
    books = Book.query.all()
    return jsonify([{"id": b.id, "title": b.title, "author": b.author, "status": b.status} for b in books])

@app.route("/books", methods=["POST"])
def add_book():
    data = request.json
    new_book = Book(title=data["title"], author=data["author"], isbn=data["isbn"], category=data["category"])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added successfully!"}), 201

@app.route("/members", methods=["POST"])
def add_member():
    data = request.json
    new_member = Member(name=data["name"], email=data["email"], phone=data["phone"])
    db.session.add(new_member)
    db.session.commit()
    return jsonify({"message": "Member added successfully!"}), 201

@app.route("/borrow", methods=["POST"])
def borrow_book():
    data = request.json
    book = Book.query.get(data["book_id"])
    member = Member.query.get(data["member_id"])

    if book and member and book.status == "Available":
        book.status = "Borrowed"
        transaction = Transaction(book_id=book.id, member_id=member.id)
        db.session.add(transaction)
        db.session.commit()
        return jsonify({"message": "Book borrowed successfully!"})
    return jsonify({"error": "Book not available or member not found"}), 400

@app.route("/return", methods=["POST"])
def return_book():
    data = request.json
    transaction = Transaction.query.filter_by(book_id=data["book_id"], member_id=data["member_id"], status="Borrowed").first()

    if transaction:
        transaction.return_date = datetime.utcnow()
        transaction.status = "Returned"
        book = Book.query.get(transaction.book_id)
        book.status = "Available"
        db.session.commit()
        return jsonify({"message": "Book returned successfully!"})
    return jsonify({"error": "Transaction not found"}), 400
