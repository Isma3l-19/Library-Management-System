from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config
from models import db, User
from routes import app as routes_app
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Extensions
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "routes.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register Blueprints
app.register_blueprint(routes_app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
