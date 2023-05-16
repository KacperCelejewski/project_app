from project import app
from flask import render_template, redirect,url_for, flash, get_flashed_messages
from project.model import User, Project
from project.forms import Register_Form, LoginForm, create_project
from project import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home_page.html")

@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Succes! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('projects_page'))
        
        else:
            flash('Username or password are not match! Please try again.', category='danger')
    
    return render_template("login_page.html", form=form)


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
        login_user(user_to_create)
        flash(f'Account created succesfully! You are now logged in as {user_to_create.username}', category='success')

        return redirect(url_for("home_page"))
    if form.errors != {}: #if there are not erroers from the validations
        for err_msg in form.errors.values():
            flash(f"There was an error with creating a user: {err_msg}",category='danger')
    return render_template("register.html",form=form)


@app.route("/Your Projects")
@login_required
def projects_page():
    projects = Project.query.all()
    return render_template('users_project.html', projects=projects)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have benn logged out!', category='info')
    return redirect(url_for('home_page'))

@app.route('/create_new_project', methods=['GET', 'POST'])
@login_required
def new_project_page():
    form = create_project()
    #check if user clicked on apply button
    if form.validate_on_submit():
        project_to_create = Project(title=form.title.data, user_id=current_user.id)
        db.session.add(project_to_create)
        db.session.commit()
        flash(f'Project "{project_to_create.title}" created succesfully!', category='success')
        
        return redirect(url_for('projects_page'))
    
    if form.errors != {}:
        for error_msg in form.errors.values():
            flash(f'There was an error with creating a project {error_msg}', category='danger')
    return render_template('new_project.html', form=form)
