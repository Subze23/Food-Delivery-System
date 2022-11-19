from app import db

class Users(db.Model):
    uid = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    email = db.Column(db.String(45))
    phno = db.Column(db.Integer)
    address = db.Column(db.String(45))
    password = db.Column(db.String(45))

    def __init__(self, name, email, password, address, phno):
        self.name = name
        self.email = email
        self.password = password
        self.address = address
        self.phno = phno

def add_user(details):
    pass

def get_user():
    pass