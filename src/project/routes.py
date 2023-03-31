from project import app
from flask import render_template
from project.model import User


@app.route("/home")
def Home_Page():
    return render_template("home_page.html")


@app.route("/")
def login_page():
    return render_template("login_page.html")


@app.route("/register")
def register_page():
    return render_template("register.html")
