from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, LoginManager, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
from models import db, Book, Member, Transaction, User
from datetime import datetime

app = Blueprint("routes", __name__)
bcrypt = Bcrypt()
login_manager = LoginManager()

login_manager.login_view = "routes.login"  # Redirect unauthorized users to login


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 📌 Landing Page - Books by Category
@app.route("/")
def index():
    categories = db.session.query(Book.category).distinct().all()
    books_by_category = {category[0]: Book.query.filter_by(category=category[0]).all() for category in categories}
    return render_template("index.html", books_by_category=books_by_category)


# 📌 View Book Details (Public)
@app.route("/book/<int:book_id>")
def view_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        flash("Book not found!", "danger")
        return redirect(url_for("routes.index"))

    return render_template("book.html", book=book)


# 📌 Read Full Book (Login Required)
@app.route("/read/<int:book_id>")
@login_required
def read_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        flash("Book not found!", "danger")
        return redirect(url_for("routes.index"))

    return render_template("read_book.html", book=book)


# 📌 User Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("routes.index"))
        else:
            flash("Invalid email or password. Please try again.", "danger")

    return render_template("login.html")


# 📌 User Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form.get("role", "reader")  # Default role is "reader"

        # Check if email is already registered
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already in use. Try another.", "danger")
            return redirect(url_for("routes.signup"))

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(username=username, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please login.", "success")
        return redirect(url_for("routes.login"))

    return render_template("signup.html")


# 📌 Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("routes.index"))


# 📌 View All Books
@app.route("/books")
def books_page():
    books = Book.query.all()
    return render_template("books.html", books=books)


# 📌 View All Members (Admins Only)
@app.route("/members")
@login_required
def members_page():
    if current_user.role != "admin":
        flash("Access denied! Only admins can view members.", "danger")
        return redirect(url_for("routes.index"))

    members = Member.query.all()
    return render_template("members.html", members=members)


# 📌 Add a Book (Admins Only)
@app.route("/add-book", methods=["GET", "POST"])
@login_required
def add_book():
    if current_user.role != "admin":
        flash("Access denied! Only admins can add books.", "danger")
        return redirect(url_for("routes.index"))

    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        isbn = request.form["isbn"]
        category = request.form["category"]
        summary = request.form["summary"]
        content_url = request.form["content_url"]

        new_book = Book(title=title, author=author, isbn=isbn, category=category, summary=summary, content_url=content_url)
        db.session.add(new_book)
        db.session.commit()
        flash("Book added successfully!", "success")
        return redirect(url_for("routes.books_page"))

    return render_template("add_book.html")


# 📌 Add a Member (Admins Only)
@app.route("/add-member", methods=["GET", "POST"])
@login_required
def add_member():
    if current_user.role != "admin":
        flash("Access denied! Only admins can add members.", "danger")
        return redirect(url_for("routes.index"))

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


# 📌 Borrow a Book (Login Required)
@app.route("/borrow", methods=["GET", "POST"])
@login_required
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


# 📌 Return a Book (Login Required)
@app.route("/return", methods=["GET", "POST"])
@login_required
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
