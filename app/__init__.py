from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

# For CSRF
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initializing flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Route for the login page

# User loader callback from flask-login docs
from app.models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app import views, models




