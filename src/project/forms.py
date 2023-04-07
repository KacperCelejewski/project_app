from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired



class Register_Form(FlaskForm):
    username= StringField(label="Username: ", validators=[Length(min=2,max=30),DataRequired()])
    surrname= StringField(label="Surrname: ",validators=[Length(min=2,max=30),DataRequired()])
    name= StringField(label="name: ",validators=[Length(min=2,max=30),DataRequired()])
    email= StringField(label="E-mail adress: ",validators=[Email(),DataRequired()])
    password1= PasswordField(label="Password: ", validators=[Length(min=6),DataRequired()])
    password2= PasswordField(label="Confirm password: ",validators=[EqualTo('password1'),DataRequired()])
   
    submit=SubmitField(label='Confirm your Account')
    