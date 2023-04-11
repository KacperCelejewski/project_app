import project
from project import db, app
from flask_migrate import Migrate


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        migrate = Migrate(app, db)
        app.run(debug=True)
