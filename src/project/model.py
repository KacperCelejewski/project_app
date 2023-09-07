from project import db, login_manager
from project import bcrypt
from flask_login import UserMixin
from flask import flash, redirect, url_for


@login_manager.user_loader
def load_user(id):
    # load user object from database or some other storage mechanism
    return User.get(id)


@login_manager.unauthorized_handler
def unauthorized():
    # redirect unauthorized users to the login page
    flash("To access this page you have to be logged in", category="danger")
    return redirect(url_for("login_page"))


project_users = db.Table(
    "project_user",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("project_id", db.Integer, db.ForeignKey("Project.id"), primary_key=True),
)


class Project(db.Model):
    __tablename__ = "Project"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(length=40), nullable=False)
    users = db.relationship("User", secondary=project_users, back_populates="projects")
    deadline = db.Column(db.Date, nullable=False)
    deadlineEnd = db.Column(db.Date, nullable=False)
    author = db.Column(db.String(length=40), nullable=False)

    description = db.Column(db.String(length=300))
    status = db.Column(db.String(length=9), default="In Progress")
    # membrs szukanie w bazie istniejacego uzytkownika
    # category

    def __repr__(self) -> str:
        return f"Title:{self.title}"


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=40), nullable=False)
    surrname = db.Column(db.String(length=40), nullable=False)
    email = db.Column(db.String(length=40), nullable=False, unique=True)
    username = db.Column(db.String(length=40), nullable=False, unique=True)
    password = db.Column(db.String(length=60), nullable=False)
    projects = db.relationship(
        "Project", secondary=project_users, back_populates="users"
    )
    events = db.relationship("Event", backref="user", lazy=True)
    is_admin = db.Column(db.Boolean(), default=False, nullable=False)

    def get(user_id):
        return User.query.get(int(user_id))

    @property
    def plain_password(self):
        raise AttributeError("plain_password is not a readable attribute")

    @plain_password.setter
    def plain_password(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode(
            "utf-8"
        )

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)

    def __repr__(self):
        return f"Name: {self.name}, Surrname: {self.surrname}, Email: {self.email}. Username: {self.username}, Password: {self.password} "

    """def __init__(
        self, author, members=[], years_to_end=0, months_to_end=0, days_to_end=0
    ) -> None:
        self.author = author
        self.members = []
        if members is not None:
            for i, member in enumerate(members):
                self.members.append((member, i))

        utc_time = pendulum.now("UTC")
        self.deadline = utc_time.add(
            years=years_to_end, months=months_to_end, days=days_to_end
        )

    def __repr__(self):
        return f"Project {self.title}""
        """


class Issues(db.Model):
    __tablename__ = "issues"
    id = db.Column(db.Integer(), primary_key=True)
    issue_name = db.Column(db.String(length=40), nullable=False)
    content = db.Column(db.Text(length=40), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("Project.id"))

    def __repr__(self) -> str:
        return f"Issue Name: {self.issue_name}"


class Event(db.Model, UserMixin):
    __tablename__ = "calendar"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=20), nullable=False)
    startDate = db.Column(db.DateTime, nullable=False)
    endDate = db.Column(db.DateTime, nullable=False)
    event = db.Column(db.Boolean(), default=True)
    task = db.Column(db.Boolean(), default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # this.name = name;
    # this.endTime = endTime;
    # this.duration = duration;
    # this.startTime = startTime
