import re	
import random	
from flask import Flask, render_template, request, session, redirect	
from flask_session import Session	
from flask_sqlalchemy import SQLAlchemy	
from flask_mail import Mail, Message	
import validate	
app = Flask(__name__)	
app.config["SESSION_PERMANENT"] = False	
app.config["SESSION_TYPE"] = "filesystem"	
Session(app)	
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:MYSQL_ROOT_PASSWORD@127.0.0.1:9906/food_delivery_system'	
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False	
app.config['MAIL_SERVER']='smtp.gmail.com'	
app.config['MAIL_PORT'] = 465	
app.config['MAIL_USERNAME'] = '200701257@rajalakshmi.edu.in'	
app.config['MAIL_PASSWORD'] = 'REC202099529'	
app.config['MAIL_USE_TLS'] = False	
app.config['MAIL_USE_SSL'] = True	
mail = Mail(app)	
db = SQLAlchemy(app)	
class User(db.Model):	
    uid = db.Column("id", db.Integer, primary_key=True)	
    name = db.Column(db.String(50))	
    email = db.Column(db.String(50))	
    password = db.Column(db.String(50))	
    address = db.Column(db.String(50))	
    phno = db.Column(db.Integer)	
    def __init__(self, name, email, password, address, phno):	
        self.name = name	
        self.email = email	
        self.password = password	
        self.address = address	
        self.phno = phno	
class Food(db.Model):	
    uid = db.Column("id", db.Integer, primary_key=True)	
    fname = db.Column(db.String(50))	
    price = db.Column(db.Integer)	
    def __init__(self, fname, price):	
        self.fname = fname	
        self.price = price	
@app.route('/')	
def hello_world():	
    return '''<h2>Page under construction</h2>	
                <p>Goto <a href="/signup">Signup</a> Page</p>	
        '''	
@app.errorhandler(404)	
def page_not_found(e):	
    return '''<h2>Uhuh!! There's really nothing here</h2>	
                <p>Goto <a href="/signup">Signup</a> Page</p>	
        ''', 404	
@app.route('/signup', methods=["POST", "GET"])	
def signup_page():	
    if ( 'user' in session ):	
        return redirect('/home')	
    if ( request.method == "POST" ):	
        details = request.form.to_dict()	
        if ( validate.validate_signup(details) ):	
            session['new_user'] = User(details['name'], details['email'], details['password'],details['address'], details['phno'])	
            session['sgotp'] = send_otp(details['email'])	
            return redirect('/verify-email')	
    return render_template("signup.html")	
@app.route('/verify-email', methods=["POST", "GET"])	
def verify_email_page():	
    if ( 'user' in session ):	
        return redirect('/home')	
    if ( request.method == "GET" ):	
        return render_template("verify_email.html")	
    if ( request.method == "POST" ):	
        if ( session['sgotp'] == int(request.form['otp']) ):	
            db.session.add(session['new_user'])	
            db.session.commit()	
            return redirect('/login')	
        return ('', 204)	
@app.route('/login', methods=["POST", "GET"])	
def login_page():	
    if ( 'user' in session ):	
        return redirect('/home')	
    if ( request.method == "POST" ):	
        user = User.query.filter_by(name=request.form['name']).first()	
        if ( user and user.password == request.form['password'] ):	
            session['user'] = user.uid	
            return redirect('/home')	
    return render_template("login.html")	
@app.route('/forgot-password', methods=["POST", "GET"])	
def forgot_password_page():	
    if ( 'user' in session ):	
        return redirect('/home')	
    if ( request.method == "POST" ):	
        print(request.form)	
        if ( 'tmpusr' not in session ):	
            session['tmpusr'] = User.query.filter_by(username=request.form['name']).first()	
        if ( 'otp' in request.form ):	
            if ( 'tries' not in session ):	
                session['tries'] = 3	
            if ( session['tries'] == 0 ):	
                return render_template("login.html")	
            recv_otp = request.form['otp']	
            print("RECV_OTP =", recv_otp)	
            print("OTP =", session['otp'])	
            if ( int(recv_otp) == session['otp'] ):	
                session['otpid'] = session['tmpusr'].uid	
                return redirect('/reset-password')	
            else:	
                session['tries'] -= 1	
                return ('', 204)    	
        else:	
            if ( re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", request.form['name']) ): 	
                email = request.form['name']	
            else:	
                email = session['tmpusr'].email	
            print("BEFORE OTP:",request.form['name'], email)	
            if ( 'otp' not in session ):	
                session['otp'] = send_otp(email)	
            print("OTP =", session['otp'])	
            return ('', 204)	
    else:	
        return render_template("forgot.html")	
@app.route('/home')	
def home_page():	
    if ( 'user' not in session ): return redirect('/login')	
    return render_template('home.html')	

def send_otp(email):
    otp = random.randint(100000, 999999)
    msg = Message(
                'OTP - Tech-A-Thon',
                sender = 'myemail@id.com',
                recipients = [email]
               )
    msg.body = 'Hello! A OTP was requested\nThis is your OTP: ' + str(otp) + "\nDo not share with anyone"
    mail.send(msg)
    return otp

app.run(debug=True)