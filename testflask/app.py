# import Flask class from flask module
from flask import Flask

# app is an instance of this Flask class
app = Flask(__name__)           # through __name__ we are passing the current app.py as module name and telling this form where flask application is started 

# routing 
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/dheeraj')
def dheeraj_method():
    return '<h1>Hi this is dheeraj poonia</h1>'

if __name__ == '__main__':     # __main__ is default name of current module and when this app.py module is import by someone else then __main__ became app.py
    # app.run(debug=True)     # optional 
    # alternative set variable from command line ps > $env:FLASK_ENV= "development" 
    pass