from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config["SECRET_KEY"] = "09b3b371eb6546919f68bd28"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"


app.config.update(
    dict(
        SECRET_KEY="09b3b371eb6546919f68bd28",
        WTF_CSRF_SECRET_KEY="09b3b371eb6546919f68bd28y",
    )
)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

from project import routes


@login_manager.user_loader
def load_user(user_id):
    from project.model import User

    return User.query.get(int(user_id))
