from flask import Flask
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Database
db.init_app(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables
    app.run(debug=True)
