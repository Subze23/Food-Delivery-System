from flask import Flask, render_template

app = Flask(__name__)

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

@app.route('/signup')
def signup_page():
    return render_template("signup.html")

@app.route('/reset-password')
def reset_password_page():
    return render_template("reset_password.html")

@app.route('/verify-email')
def verify_email_page():
    return render_template("verify_email.html")

app.run(host='0.0.0.0', port=81, debug=True)