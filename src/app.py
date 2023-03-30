from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def Home_Page():
    return render_template("home_page.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


app.run()
