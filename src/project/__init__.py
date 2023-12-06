from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import Flask, Response
from flask_principal import Principal, Permission, RoleNeed
from dotenv import load_dotenv

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")


app.config.update(
    dict(
        WTF_CSRF_SECRET_KEY=os.environ.get("WTF_CSRF_SECRET_KEY")
)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
principal = Principal(app)
login_manager = LoginManager()
login_manager.init_app(app)

from project import routes


@login_manager.user_loader
def load_user(user_id):
    from project.model import User

    return User.query.get(int(user_id))



