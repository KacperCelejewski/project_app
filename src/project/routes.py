from project import app
from flask import render_template
from project.model import User
from project.forms import Register_Form

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home_page.html")

@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/login")
def login_page():
    return render_template("login_page.html")


@app.route("/register")
def register_page():
    form = Register_Form()
    return render_template("register.html",form=form)
