from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET KEY'] = '09b3b371eb6546919f68bd28'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

app.config.update(dict(
    SECRET_KEY="09b3b371eb6546919f68bd28",
    WTF_CSRF_SECRET_KEY="09b3b371eb6546919f68bd28y"
))
db = SQLAlchemy(app)




from project import routes
