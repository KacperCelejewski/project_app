from project import db, login_manager
from project import bcrypt
from flask_login import UserMixin
import pendulum


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=40), nullable=False)
    surrname = db.Column(db.String(length=40), nullable=False)
    email = db.Column(db.String(length=40), nullable=False, unique=True)
    username = db.Column(db.String(length=40), nullable=False, unique=True)
    password = db.Column(db.String(length=60), nullable=False)
    projects = db.relationship("Project", backref="user", lazy=True)

    def get(user_id):
        return User.query.get(int(user_id))

    @property
    def plain_password(self):
        return self.plain_password

    @plain_password.setter
    def plain_password(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode(
            "utf-8"
        )

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)

    def __repr__(self):
        return f"Name: {self.name}, Surrname: {self.surrname}, Email: {self.email}. Username: {self.username}, Password: {self.password} "


class Project(db.Model):
    __tablename__ = "Project"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(length=40), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # deadline = db.Column(db.DateTime, nullable=False)

    def __repr__(self) -> str:
        return f"Title:{self.title}"


"""
    def __init__(
        self, name, author, members=[], years_to_end=0, months_to_end=0, days_to_end=0
    ) -> None:
        self.name = name
        self.members = []
        if members is not None:
            for i, member in enumerate(members):
                self.members.append((member, i))

        utc_time = pendulum.now("UTC")
        self.deadline = utc_time.add(
            years=years_to_end, months=months_to_end, days=days_to_end
        )

    def __repr__(self):
        return f"Project {self.name}, deadline {self.deadline}"
"""
