from flask import Flask, render_template

app = Flask(__name__)


@app.route("/home")
def Home_Page():
    return render_template("home_page.html")


app.run()
