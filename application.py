from flask import Flask, session
from flask_session import Session
from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine('postgres://ntcwaduvpgeowm:b5459817675574612c7cf55ba6ffbb0752457b10239c15c7084ef858b9277349@ec2-54-83-17-151.compute-1.amazonaws.com:5432/dce25fb79tcjcv', echo = True)
db = scoped_session(sessionmaker(bind=engine))

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app = Flask(__name__)

@app.route("/")
def index():
       return render_template("index.html",error="Login to give book review")


# after login main (book) section start here

@app.route("/givereview/<int:book_id>")
def givereview(book_id):  
       bookselect = db.execute("SELECT * FROM book WHERE book_id = :book_id", {"book_id": book_id}).fetchone()
       return render_template("givereview.html", book=bookselect, error="this is your selected book give review")



@app.route("/savereview", methods=["POST"])
def savereview():
       if request.method == 'POST':
              scale = request.form.get('star')
              texts = request.form.get('texts')
              return "save review"
              '''
              student_id = db.execute("SELECT student_id FROM student WHERE username = :username", {"username": username}).fetchone();
              book_id = db.execute("SELECT book_id FROM book WHERE book_id = :book_id", {"book_id": book_id}).fetchone();
              db.execute("INSERT INTO review (scale, texts, student, book) VALUES (:scale, :texts, :student, :book)",
                    {"scale": scale, "texts": texts, "student": student_id, "book": book_id})
              '''


@app.route("/viewreview")
def viewreview():
       return render_template("viewreview.html")




# LOGIN AND CREATE ACCOUNT

@app.route("/login", methods=['GET', 'POST'])
def login():
       if request.method == 'POST':
              username = request.form.get('username')
              password = request.form.get('password')
              if db.execute("SELECT username FROM student WHERE username = :username", {"username": username}).rowcount == 0:
                     return render_template("createaccount.html", error="Account not exits, create account first")
              else:
                     raw_password = db.execute("SELECT passwrd FROM student WHERE username = :username", {"username": username}).fetchone()
                     password_db = raw_password[0]
                     if(password == password_db):
                            booksdb = db.execute("SELECT * FROM book ").fetchall()
                            return render_template("book.html", books=booksdb, error="login succesfull, select book to give review", username=username)
                     else:
                            return render_template("index.html",error="Try login again, password not match")
       else:
              return render_template("index.html",error="something went wrong, try again")


@app.route("/createaccount")
def createaccount():
       return render_template("createaccount.html",error="welcome new user")


@app.route("/register", methods=['GET', 'POST'])
def register():
       username = request.form.get('username')
       password = request.form.get('password')

       if db.execute("SELECT username FROM student WHERE username = :username", {"username": username}).rowcount == 0:
              db.execute("INSERT INTO student (username, passwrd) VALUES (:username, :passwrd)",
                    {"username": username, "passwrd": password})
              db.commit()
              return render_template("index.html", name=username,error="account create success, login now" )

       
       else:
              return render_template("index.html", error="Username exist, login now")

       return render_template("createaccount.html", errro="something went wrong try again")



if __name__ == '__main__':
       app.run()


