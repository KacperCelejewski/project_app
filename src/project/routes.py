from project import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from project.model import User
from project.forms import Register_Form, Loginform
from project import db
from flask_login import login_user, logout_user


@app.route("/home")
def home_page():
    return render_template("home_page.html")


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/", methods=["GET", "POST"])
def login_page():
    form = Loginform()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(
                f"Success! You are logged in as: {attempted_user.username}",
                category="success",
            )
            return redirect(url_for("home_page"))
        else:
            flash(
                "Username and password are not match! Please try again!",
                category="danger",
            )

    return render_template("login_page.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = Register_Form()
    # check if user clicked on submit button
    if form.validate_on_submit():
        # read data from input fields to create User object

        user_to_create = User(
            username=form.username.data,
            email=form.email.data,
            plain_password=form.password1.data,
            surrname=form.surrname.data,
            name=form.name.data,
        )
        with app.app_context():
            db.create_all()
            db.session.add(user_to_create)
            db.session.commit()
        with app.app_context():
            db.create_all()
            db.session.add(user_to_create)
            db.session.commit()
        return redirect(url_for("home_page"))
    if form.errors != {}:  # if there are not erroers from the validations
        for err_msg in form.errors.values():
            flash(
                f"There was an error with creating a user: {err_msg}", category="danger"
            )
    return render_template("register.html", form=form)


@app.route("/Your Projects")
def projects_page():
    return render_template("users_project.html")


@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have been logged out!", category="info")
    return redirect(url_for("login_page"))
