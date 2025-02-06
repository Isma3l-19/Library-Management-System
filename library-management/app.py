from flask import Flask
from config import Config
from models import db
from routes import app as routes_app  # Import the routes

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Database
db.init_app(app)

# Register routes
app.register_blueprint(routes_app)  # Register the routes

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don’t exist
    app.run(debug=True)
