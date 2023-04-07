from project import app
from flask import render_template, redirect,url_for, flash, get_flashed_messages
from project.model import User
from project.forms import Register_Form
from project import db

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


@app.route("/register",methods=["GET","POST"])
def register_page():
    form = Register_Form()
    #check if user clicked on submit button
    if form.validate_on_submit():
        #read data from input fields to create User object
        user_to_create= User(username = form.username.data,
                            email = form.email.data,
                            password= form.password1.data,
                            surrname=form.surrname.data,
                            name=form.name.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for("home_page"))
    if form.errors != {}: #if there are not erroers from the validations
        for err_msg in form.errors.values():
            flash(f"There was an error with creating a user: {err_msg}",category='danger')
    return render_template("register.html",form=form)


@app.route("/Your Projects")
def projects_page():
    return render_template('users_project.html')
