import os
from models import db, User
from flask_bcrypt import Bcrypt
from flask import Flask
from dotenv import load_dotenv

# Load environment variables
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
bcrypt = Bcrypt(app)
db.init_app(app)

with app.app_context():
    username = "admin"
    email = "admin@example.com"
    password = "12345"  # Change to a strong password

    # Check if an admin already exists
    existing_admin = User.query.filter_by(role="admin").first()
    if existing_admin:
        print("⚠️ Admin user already exists!")
    else:
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_admin = User(username=username, email=email, password=hashed_password, role="admin")
        db.session.add(new_admin)
        db.session.commit()
        print("✅ Admin Created Successfully!")
