from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import validate

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@127.0.0.1:9906/demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Session(app)

db = SQLAlchemy(app)

@app.route('/')
def index():
    return 'Web App with Python Flask!'

@app.errorhandler(404)
def page_not_found(e):
    return '''<h2>Uhuh!! There's really nothing here</h2>
                <p>Goto <a href="/">Home</a></p>
        ''', 404

@app.route('/login')
def login_page():
    return render_template("login.html")

@app.route('/signup', methods=["GET", "POST"])
def signup_page():
    if ( request.method == "GET" ):
        return render_template("signup.html")
    form_data = request.form.to_dict()
    if ( validate.validate_signup(form_data) ):
        pass
    

@app.route('/reset-password')
def reset_password_page():
    return render_template("reset_password.html")

@app.route('/verify-email')
def verify_email_page():
    return render_template("verify_email.html")

app.run(host='0.0.0.0', port=81, debug=True)