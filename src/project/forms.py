from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    IntegerField,
    HiddenField,
    TextAreaField,
    DateTimeField,
    DateTimeLocalField,
    DateField,
    RadioField,
)
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from project.model import User


class Register_Form(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError(
                "Username already exist! Please try a different username"
            )

    def validate_email(
        self, email_to_check
    ):  # Klakson zeby dzialal poprawnie modul rejestracji to hasło nie może się składać z samych cyfr bo pokazuje się błąd
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError("Email already exists! Please try a different email")

    username = StringField(
        label="Username: ", validators=[Length(min=2, max=30), DataRequired()]
    )
    surrname = StringField(
        label="Surrname: ", validators=[Length(min=2, max=30), DataRequired()]
    )
    name = StringField(
        label="name: ", validators=[Length(min=2, max=30), DataRequired()]
    )
    email = StringField(label="E-mail adress: ", validators=[Email(), DataRequired()])
    password1 = PasswordField(
        label="Password: ", validators=[Length(min=6), DataRequired()]
    )
    password2 = PasswordField(
        label="Confirm password: ", validators=[EqualTo("password1"), DataRequired()]
    )

    submit = SubmitField(label="Confirm your Account")


class Loginform(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Sign in")


class editForm(FlaskForm):
    title = StringField(label="Title")
    deadline = DateField("Start Date", format="%Y-%m-%d")
    deadlineEnd = DateField("Due Date", format="%Y-%m-%d")
    description = TextAreaField(label="Description")
    submitBtn = SubmitField(label="Edit")


class create_project(FlaskForm):
    title = StringField(label="Title")
    deadline = DateField("Start Date", format="%Y-%m-%d")
    deadlineEnd = DateField("End Date", format="%Y-%m-%d")
    description = TextAreaField(label="Description")
    submite = SubmitField(label="Apply")


class addForm(FlaskForm):
    surrname = StringField(label="Choose your new Teammate!")
    submit = SubmitField(label="Add")


class IssuesForm(FlaskForm):
    issue_name = StringField(label="issue_name")
    content = TextAreaField(label="content")
    submite = SubmitField(label="Apply")


class addEvent(FlaskForm):
    name = StringField()
    startDate = DateTimeLocalField(format="%Y-%m-%dT%H:%M")
    endDate = DateTimeLocalField(format="%Y-%m-%dT%H:%M")
    example = RadioField(choices=[("value1", "Event"), ("value2", "Task")])
    submit = SubmitField(label="Save")
