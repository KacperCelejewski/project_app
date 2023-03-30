from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(app)


class User(db.Model):
    ID = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=40), nulable=False)
    surrname = db.Column(db.String(length=40), nulable=False, unique=True)
    email = db.Column(db.String(length=40), nulable=False, unique=True)
    username = db.Column(db.String(length=40), nulable=False, unique=True)
    password = db.Column(db.String(length=40), nulable=False, unique=True)
    ID = db.Column


@app.route("/home")
def Home_Page():
    return render_template("home_page.html")


@app.route("/")
def login_page():
    return render_template("login_page.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


app.run()
