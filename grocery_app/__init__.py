from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from grocery_app.extensions import db
from grocery_app.auth.routes import auth
from grocery_app.routes import main

# Initialize Flask extensions
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    from grocery_app.models import User
    return User.query.get(user_id)

def create_app():
    app = Flask(__name__)
    app.config.from_object('grocery_app.config')

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app
