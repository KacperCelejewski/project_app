from project import app
from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    current_app,
    jsonify,
    make_response,
)
from project.model import User, Project, Issues, Event
from project.forms import Register_Form, Loginform, create_project
from project.forms import addForm, editForm, addEvent
from project import db
from flask_login import login_user, logout_user, login_required, current_user
from flask import request, session
from sqlalchemy.exc import SQLAlchemyError
from flask_wtf.csrf import generate_csrf
from sqlalchemy.orm import make_transient
from flask_login import LoginManager
from flask_principal import Principal, Permission, Identity, identity_changed, RoleNeed
import json

principal = Principal(app)


admin_role = Permission(RoleNeed("admin"))
user_role = RoleNeed("user")
admin_permission = Permission(admin_role)
user_permission = Permission(user_role)


# first contact page
@app.route("/login", methods=["GET", "POST"])
def login_page():
    # class in forms.py file, that creates textboxes to log in
    # types of textboxes: -username -password -button to confirm and connect with DB
    form = Loginform()
    if form.validate_on_submit():  #  when user clicks submit button
        #  searching query
        #  to find first username that's the same as textbox input
        attempted_user = User.query.filter_by(username=form.username.data).first()
        #  user has to exist
        #  hashed password equls to plain password (as argument takes plain password)
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            #  condistion fulfilled
            #  assigning user as logged in in session
            login_user(attempted_user)
            flash(
                f"Success! You are logged in as: {attempted_user.username}",
                category="success",
            )
            session["username"] = attempted_user.username
            if current_user.is_authenticated:
                if current_user.is_admin:
                    identity = Identity(current_user.id)
                    identity.provides.add(RoleNeed("admin"))
                    identity_changed.send(
                        current_app._get_current_object(), identity=identity
                    )
                else:
                    identity = Identity(current_user.id)
                    identity.provides.add(RoleNeed("user"))
                    identity_changed.send(
                        current_app._get_current_object(), identity=identity
                    )

            return redirect(url_for("home_page"))

        else:
            flash(
                "Username and password do not match! Please try again!",
                category="danger",
            )

    return render_template("login_page.html", form=form)


@app.route("/")
def home_page():
    return render_template("home_page.html")


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
    form = editForm()
    add = addForm()
    surrname = add.surrname.data
    if add.validate_on_submit():
        return redirect(url_for("addUser", project_id=project.id, surrname=surrname))

    timeDict = {}
    users_projects = Project.query.filter(Project.users.any(id=current_user.id)).all()
    projects = []

    for project in users_projects:
        projects.append(project)

    for project in projects:
        timeToEnd = project.deadline - project.deadlineEnd
        # dict with key(id):value(time in days)
        timeDict.update({project.id: timeToEnd.days})
    return render_template(
        "users_project.html", projects=projects, timeDict=timeDict, form=form, add=add
    )


@app.route("/logout")
@login_required
def logout_page():
    logout_user()
    flash("You have been logged out!", category="info")
    return redirect(url_for("login_page"))


@app.route("/New Project", methods=["GET", "POST"])
@login_required
def new_project():
    form = create_project()

    if form.validate_on_submit():
        from datetime import datetime

        projectToCreate = Project(
            users=[current_user],
            title=form.title.data,
            author=current_user.username,
            deadline=form.deadline.data,
            deadlineEnd=form.deadlineEnd.data,
            description=form.description.data,
        )
        with app.app_context():
            db.session.add(projectToCreate)
            db.session.commit()

            flash(f"Successfully added project", category="info")

    else:
        flash(form.errors)
    return render_template("new_project.html", form=form, csrf_token=generate_csrf())


@app.route("/Your Projects/<int:project_id>", methods=["GET", "POST"])
@login_required
def issue(project_id):
    project = Project.query.get(project_id)

    return render_template("issue_page.html", project=project)


@login_required
@app.route("/change_status/<int:id>", methods=["POST"])
def change_status(id):
    new_status = request.json.get("newStatus")
    print(new_status)
    project = Project.query.get(id)
    if project:
        project.status = new_status
        db.session.commit()
        return jsonify(message="Status changed successfully")

    else:
        return jsonify(message="Project not found"), 404


@login_required
@app.route("/Your Projects/edit/<int:project_id>", methods=["GET", "POST"])
def edit(project_id):
    project = Project.query.get_or_404(project_id)
    form = editForm(obj=project)

    if request.method == "POST":
        if form.title.data:
            project.title = form.title.data
        if form.deadline.data:
            project.deadline = form.deadline.data
        if form.deadlineEnd.data:
            project.deadlineEnd = form.deadlineEnd.data
        if form.description.data:
            project.description = form.description.data
        project.status = "Edited"
        try:
            db.session.commit()
            flash("Changes saved successfully.", "success")
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            db.session.rollback()

    return redirect(url_for("projects_page") + "#projectEditWindow")


@login_required
@app.route("/Your Projects/addUser/<int:project_id>", methods=["GET", "POST"])
def addUser(project_id):
    surrname = request.form.get("surrname")
    project = Project.query.get(project_id)
    user = User.query.filter_by(surrname=surrname).first()

    if user and project:
        project.users.append(user)
        db.session.commit()
        flash("User added to project successfully.", "success")
    else:
        flash("User or project not found.", "error")
        flash(surrname)

    return redirect(url_for("projects_page"))


from datetime import datetime


@app.route("/Schedule", methods=["POST", "GET"])
@login_required
def schedule():
    try:
        eventForm = addEvent()
        if eventForm.validate_on_submit():
            # print(eventForm.data)
            if eventForm.example.data == "task":
                taskValue = True
                eventValue = False
            else:
                taskValue = False
                eventValue = True

            newEvent = Event(
                name=eventForm.name.data,
                startDate=eventForm.startDate.data,
                endDate=eventForm.endDate.data,
                event=eventValue,
                task=taskValue,
                user=current_user,
            )

            try:
                db.session.add(newEvent)
                db.session.commit()
                flash("Event added successfully!", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Error adding event: {e}", "error")

    except Exception as e:
        flash(e)

    # response = make_response(jsonify(eventData))

    return render_template("schedule.html", eventForm=eventForm)


@app.route("/sendEvent", methods=["GET"])
@login_required
def send_event():
    try:
        users_event = Event.query.filter(User.events.any(id=current_user.id)).all()
        if users_event:
            # print(users_event)
            # event_data = {
            #     "name": users_event.name,
            #     "startDate": users_event.startDate,
            #     "endDate": users_event.endDate,
            #     "event": users_event.event,
            #     "task": users_event.task,
            # }
            event_list = []
            for event in users_event:
                event_data = {
                    "name": event.name,
                    "startDate": event.startDate,
                    "endDate": event.endDate,
                    "event": event.event,
                    "task": event.task,
                }

                event_list.append(event_data)

            return jsonify(event_list)

        else:
            return jsonify({"error": "No event found for the current user"})
    except Exception as e:
        return jsonify({"error": str(e)})
