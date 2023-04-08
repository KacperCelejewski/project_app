import project
from project import db, app

if __name__ == "__main__":
    with app.app_context():
        project.app.run(debug=True)
