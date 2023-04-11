from project import app
from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    get_flashed_messages,
    request,
    current_app,
)
from project.model import User, Project
from project.forms import Register_Form, Loginform, create_project
from project import db
from flask_login import login_user, logout_user, login_required, current_user
from flask import request, session
from sqlalchemy.exc import SQLAlchemyError
from flask_wtf.csrf import generate_csrf


import pendulum
from flask_login import LoginManager


@app.route("/home")
@login_required
def home_page():

    return render_template("home_page.html")


@app.route("/about")
@login_required
def about_page():
    return render_template("about.html")


login_manager = LoginManager(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    # load user object from database or some other storage mechanism
    return User.get(id)


@login_manager.unauthorized_handler
def unauthorized():
    # redirect unauthorized users to the login page
    flash("To access this page you have to be logged in", category="danger")
    return redirect(url_for("login_page"))


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
            session["username"] = attempted_user.username
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
        with app.app_context():
            user_to_create = User(
                username=form.username.data,
                email=form.email.data,
                plain_password=form.password1.data,
                surrname=form.surrname.data,
                name=form.name.data,
            )
            db.session.add(user_to_create)
            db.session.commit()
            login_user(user_to_create)
            return redirect(url_for("home_page"))
    if form.errors != {}:  # if there are not erroers from the validations
        for err_msg in form.errors.values():
            flash(
                f"There was an error with creating a user: {err_msg}", category="danger"
            )
    return render_template("register.html", form=form)


@app.route("/Your Projects")
@login_required
def projects_page():
    projects = Project.query.all()

    return render_template("users_project.html", projects=projects)


@app.route("/logout")
@login_required
def logout_page():
    logout_user()
    flash("You have been logged out!", category="info")
    return redirect(url_for("login_page"))


@app.route("/New Project", methods=["GET", "POST"])
@login_required
def n_project():

    form = create_project()

    if form.validate_on_submit():

        project_to_create = Project(user_id=int(current_user.id), title=form.title.data)
        with app.app_context():
            db.session.add(project_to_create)
            db.session.commit()

            flash(f"Successfully added project", category="info")
    else:
        flash(form.errors)

    return render_template("new_project.html", form=form, csrf_token=generate_csrf())
