from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from project.model import User



class Register_Form(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already exist! Please try a different username")

    def validate_email(self, email_to_check):    #Klakson zeby dzialal poprawnie modul rejestracji to hasło nie może się składać z samych cyfr bo pokazuje się błąd
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError("Email already exists! Please try a different email")

    username= StringField(label="Username: ", validators=[Length(min=2,max=30),DataRequired()])
    surrname= StringField(label="Surrname: ",validators=[Length(min=2,max=30),DataRequired()])
    name= StringField(label="name: ",validators=[Length(min=2,max=30),DataRequired()])
    email= StringField(label="E-mail adress: ",validators=[Email(),DataRequired()])
    password1= PasswordField(label="Password: ", validators=[Length(min=6),DataRequired()])
    password2= PasswordField(label="Confirm password: ",validators=[EqualTo('password1'),DataRequired()])
   
    submit=SubmitField(label='Confirm your Account')
    