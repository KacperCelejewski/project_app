from project import db
from project import bcrypt

class User(db.Model):
    ID = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=40), nullable=False)
    surrname = db.Column(db.String(length=40), nullable=False)
    email = db.Column(db.String(length=40), nullable=False, unique=True)
    username = db.Column(db.String(length=40), nullable=False, unique=True)
    password = db.Column(db.String(length=60), nullable=False)
   #  projects=db.relationship('Project'),backref='owened_user', lazy=True)
    
    @property
    def plain_password(self):
        return self.plain_password
    @plain_password.setter
    def plain_password(self, plain_text_password):
        self.password= bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    def __repr__(self):
        return f"Name: {self.name}, Surrname: {self.surrname}, Email: {self.email}. Username: {self.username}, Password: {self.password} "
    