import project


if __name__ == "__main__":
    project.app.run(debug=True)
    project.app.app_context().push()
