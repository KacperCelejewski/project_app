from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class Register_Form(FlaskForm):
    username= StringField(label="User name: ")
    surrname= StringField(label="Surrname: ")
    name= StringField(label="name: ")
    email= StringField(label="E-mail adress: ")
    password1= PasswordField(label="Password: ")
    password2= PasswordField(label="Confirm password: ")
   
    submit=SubmitField(label='Confirm your Account')
    