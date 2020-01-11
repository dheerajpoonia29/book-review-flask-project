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
username = None

@app.route("/", methods=['GET', 'POST'])
def index():
       session.pop('username', None)
       if request.method == 'POST':
              return render_template("index.html",error="Logout! Pleasure to see you again",username="Good Bye")
       
       return render_template("index.html",error="Msg- Login to give review on book",username="Welcome")


# after login main (book) section start here

@app.route("/givereview/<int:book_id>")
def givereview(book_id):  
       username = session.get('username')
       bookselect = db.execute("SELECT * FROM book WHERE book_id = :book_id", {"book_id": book_id}).fetchone()
       return render_template("givereview.html", book=bookselect, error="Msg- This is your selected book give review now",username=username)



@app.route("/savereview/<int:book_id>", methods=["POST"])
def savereview(book_id):
       if request.method == 'POST':
              scale = request.form.get('star')
              texts = request.form.get('texts')
              username = session.get('username')

              sid = db.execute("SELECT student_id FROM student WHERE username = :username", {"username": username}).fetchone();
              student_id = sid[0]
              bid = db.execute("SELECT book_id FROM book WHERE book_id = :book_id", {"book_id": book_id}).fetchone();
              book_id = bid[0]
              
              booksdb = db.execute("SELECT * FROM book LIMIT 10 ").fetchall()

              if db.execute("SELECT * FROM review WHERE student = :student_id and book = :book_id", {"student_id": student_id, "book_id": book_id}).rowcount == 0:
                     db.execute("INSERT INTO review (scale, texts, student, book) VALUES (:scale, :texts, :student, :book)",
                            {"scale": scale, "texts": texts, "student": student_id, "book": book_id})
                     db.commit()
                     return render_template("book.html", books=booksdb, error="Success! Review save successfull, click on view review", username=username)

              return render_template("book.html", books=booksdb, error="Error! Select another book, You give review on this book", username=username)
              


@app.route("/viewreview")
def viewreview():
       username = session.get('username')
       if(username is None):
              return render_template("index.html",error="Error! Login first to view your review",username="Login First")
       
       sid = db.execute("SELECT student_id FROM student WHERE username = :username", {"username": username}).fetchone();
       student_id = sid[0]
       usrreview = db.execute("SELECT * FROM review where student = :student_id", {"student_id": student_id}).fetchall();
       
       
       return render_template("viewreview.html", review=usrreview, error="Msg- Your total books review list", username=username)




# LOGIN AND CREATE ACCOUNT

@app.route("/login", methods=['GET', 'POST'])
def login():
       if request.method == 'POST':
              username = request.form.get('username')
              password = request.form.get('password')
              if db.execute("SELECT username FROM student WHERE username = :username", {"username": username}).rowcount == 0:
                     return render_template("createaccount.html", error="Error! Account not exits, create account first")
              else:
                     raw_password = db.execute("SELECT passwrd FROM student WHERE username = :username", {"username": username}).fetchone()
                     password_db = raw_password[0]
                     if(password == password_db):
                            booksdb = db.execute("SELECT * FROM book LIMIT 10").fetchall()
                            session['username'] = username
                            return render_template("book.html", books=booksdb, error="Msg- Select book by click on isbn no or search to give review", username=username)
                     else:
                            return render_template("index.html",error="Error! Try login again, password not match",username="Login First")
       else:
              return render_template("index.html",error="Error! Fill the login form first",username="Login First")


@app.route("/createaccount")
def createaccount():
       return render_template("createaccount.html",error="Msg- Welcome you on book review application",username="Welcome")


@app.route("/register", methods=['GET', 'POST'])
def register():
       username = request.form.get('username')
       password = request.form.get('password')

       if db.execute("SELECT username FROM student WHERE username = :username", {"username": username}).rowcount == 0:
              db.execute("INSERT INTO student (username, passwrd) VALUES (:username, :passwrd)",
                    {"username": username, "passwrd": password})
              db.commit()
              return render_template("index.html", name=username,error="Sucess! Account create successfull, login now" )

       
       else:
              return render_template("index.html", error="Msg- Username exist, login now")

       return render_template("createaccount.html", errro="Error! Something went wrong try again")


if __name__ == "__main__":
    app.run(debug=True)