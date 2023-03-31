from project import db


class User(db.Model):
    ID = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=40), nullable=False)
    surrname = db.Column(db.String(length=40), nullable=False, unique=True)
    email = db.Column(db.String(length=40), nullable=False, unique=True)
    username = db.Column(db.String(length=40), nullable=False, unique=True)
    password = db.Column(db.String(length=40), nullable=False, unique=True)

    def __repr__(self):
        return f"Name: {self.name}, Surrname: {self.surrname}, Email: {self.email}. Username: {self.username}, Passwod: {self.password} "
