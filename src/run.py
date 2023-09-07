from project import db, app
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from project import db
from flask import session


if __name__ == "__main__":
    with app.app_context():
        db.session.remove()
        db.create_all()
        migrate = Migrate(app, db)
        app.run(debug=True)
