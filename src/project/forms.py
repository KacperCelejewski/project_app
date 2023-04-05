from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class Register_Form(FlaskForm):
    username= StringField(label="User name: ")
    email= StringField(label="E-mail adress: ")
    password1= PasswordField(label="Password: ")
    password2= PasswordField(label="Confirm password: ")
    submit=SubmitField(label='Confirm your Account')