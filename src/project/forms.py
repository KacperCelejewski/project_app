from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, HiddenField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from project.model import User, Project
import re


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
        
    def validate_password(self, password1):
        self.password1 = password1
    
        if not any(c.islower() for c in password1.data):
            raise ValidationError('Password must contain at least one lowercase letter.')
    
        if not any(c.isupper() for c in password1.data):
            raise ValidationError('Password must contain at least one uppercase letter.')
    
        if not any(c.isdigit() for c in password1.data):
            raise ValidationError('Password must contain at least one digit.')
        
    def validate_name(self, field):
        if not re.match(r'^[A-Z][a-z]*$', field.data):
            raise ValidationError('In Name one capital letter, only at the beginning')
        
    def validate_surrname(self, field2):
        if not re.match(r'^[A-Z][a-z]*$', field2.data):
            raise ValidationError('In Surrname one capital letter, only at the beginning')

        

    username = StringField(label="Username: ", validators=[Length(min=2, max=30), DataRequired()])
    surrname = StringField(
        label="Surrname: ", validators=[Length(min=2, max=30), DataRequired(), validate_surrname]
    )
    name = StringField(
        label="name: ", validators=[Length(min=2, max=30), DataRequired(), validate_name]
    )
    email = StringField(label="E-mail adress: ", validators=[Email(), DataRequired()])
    password1 = PasswordField(
        label="Password: ", validators=[Length(min=6), DataRequired(), validate_password]
    )
    password2 = PasswordField(
        label="Confirm password: ", validators=[EqualTo("password1"), DataRequired()]
    )

    submit = SubmitField(label="Confirm your Account")


class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Sign in")


class create_project(FlaskForm):

    def validate_title(self, title_to_check,):
        project = Project.query.filter_by(title=title_to_check.data).first()
        if project:
            raise ValidationError("You need to take another title, because this topic already exist!")
        
    def process_title(self, field):
        if not re.match(r'[A-Z]{1}[0-9a-zA-Z\s]*$', field.data):
            raise ValidationError('One capital letter, only at the beginning of the title.')

    title = StringField(label="Title", validators=[Length(min= 2, max=30), DataRequired(), validate_title, process_title])
    submite = SubmitField(label="Apply")

    
        