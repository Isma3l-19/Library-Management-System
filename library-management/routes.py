from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from models import db, Book, Member, Transaction
from datetime import datetime

app = Blueprint("routes", __name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/books")
def books_page():
    books = Book.query.all()
    return render_template("books.html", books=books)

@app.route("/members")
def members_page():
    members = Member.query.all()
    return render_template("members.html", members=members)

# 📌 Route to show "Add Book" form
@app.route("/add-book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        isbn = request.form["isbn"]
        category = request.form["category"]
        
        new_book = Book(title=title, author=author, isbn=isbn, category=category)
        db.session.add(new_book)
        db.session.commit()
        
        flash("Book added successfully!", "success")
        return redirect(url_for("routes.books_page"))
    
    return render_template("add_book.html")

# 📌 Route to show "Add Member" form
@app.route("/add-member", methods=["GET", "POST"])
def add_member():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        
        new_member = Member(name=name, email=email, phone=phone)
        db.session.add(new_member)
        db.session.commit()
        
        flash("Member added successfully!", "success")
        return redirect(url_for("routes.members_page"))
    
    return render_template("add_member.html")


@app.route("/borrow", methods=["GET", "POST"])
def borrow_page():
    if request.method == "POST":
        book_id = request.form["book_id"]
        member_id = request.form["member_id"]

        book = Book.query.get(book_id)
        member = Member.query.get(member_id)

        if book and member and book.status == "Available":
            book.status = "Borrowed"
            transaction = Transaction(book_id=book.id, member_id=member.id)
            db.session.add(transaction)
            db.session.commit()
            flash("Book borrowed successfully!", "success")
        else:
            flash("Error: Book not available or Member not found.", "danger")

        return redirect(url_for("routes.borrow_page"))

    books = Book.query.filter_by(status="Available").all()
    members = Member.query.all()
    return render_template("borrow.html", books=books, members=members)

@app.route("/return", methods=["GET", "POST"])
def return_page():
    if request.method == "POST":
        book_id = request.form["book_id"]
        transaction = Transaction.query.filter_by(book_id=book_id, status="Borrowed").first()

        if transaction:
            transaction.return_date = datetime.utcnow()
            transaction.status = "Returned"
            book = Book.query.get(transaction.book_id)
            book.status = "Available"
            db.session.commit()
            flash("Book returned successfully!", "success")
        else:
            flash("Error: No active borrow transaction found.", "danger")

        return redirect(url_for("routes.return_page"))

    borrowed_books = Transaction.query.filter_by(status="Borrowed").all()
    return render_template("return.html", borrowed_books=borrowed_books)
