import os
from models import db, Admin
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
    username = "ADMIN"
    password = "12345"  # Change this to a secure password
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    
    new_admin = Admin(username=username, password=hashed_password)
    db.session.add(new_admin)
    db.session.commit()
    print("✅ Admin Created")
