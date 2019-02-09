from flask import Flask, session
from flask_session import Session
from flask import Flask, render_template, request

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("username")
    return render_template("book.html", username=name)

@app.route("/createaccount")
def createaccount():
    return render_template("createaccount.html")

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("username")
    return render_template("index.html", name=name)



# after login main (book) section start here

@app.route("/givereview", methods=["POST"])
def givereview():
    return render_template("givereview.html")

@app.route("/savereview", methods=["POST"])
def savereview():
    return render_template("viewreview.html")

@app.route("/viewreview")
def viewreview():
    return render_template("viewreview.html")






