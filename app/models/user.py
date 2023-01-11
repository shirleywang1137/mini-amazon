from random import randint
from flask_login import UserMixin, current_user
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login

class User(UserMixin):
    def __init__(self, uid, email, firstname, lastname, address, password, balance):
        self.uid = uid
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.password = password
        self.balance = balance

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT uid, email, firstname, lastname, address, password, balance
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows: 
            print("1") # email not found
            return None
        elif not check_password_hash(rows[0][5], password):
            print("0")
            # incorrect password
            return None
        else:
            return User(*(rows[0][0:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT uid, email, firstname, lastname, address, password, balance
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    def register(email, password, firstname, lastname, address):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, firstname, lastname, address, password, balance)
VALUES(:email, :firstname, :lastname, :address, :password, :balance)
RETURNING uid
""",
                                email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname, lastname=lastname, address = address, balance = 0.0)
            uid = rows[0][0]
            return User.get(uid)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    @login.user_loader
    def get(uid):
        rows = app.db.execute("""
SELECT uid, email, firstname, lastname, address, password, balance
FROM Users
WHERE uid = :uid
""",
                              uid=uid)
        return User(*(rows[0])) if rows else None

    @staticmethod
    def addBal(uid, additional):
        app.db.execute("""
UPDATE Users
SET balance = balance + :additional
WHERE uid = :uid
""",
                              uid = uid, additional=additional)
        
        return 1
    
    @staticmethod
    def setBal(uid, set):
        app.db.execute("""
UPDATE Users
SET balance = :set
WHERE uid = :uid
""",
                              uid = uid, set=set)
        
        return 1
    
    def withdrawBal(uid, less):
        app.db.execute("""
UPDATE Users
SET balance = balance - :less
WHERE uid = :uid
""",
                              uid = uid, less=less)
        
        return 1
    
    def changeName(uid, firstname, lastname):
        app.db.execute("""
UPDATE Users
SET firstname = :firstname, lastname = :lastname
WHERE uid = :uid
""",
                              uid = uid, firstname = firstname, lastname = lastname)
        
        return 1

    def changeEmail(uid, email):
        app.db.execute("""
UPDATE Users
SET email = :email
WHERE uid = :uid
""",
                              uid = uid, email = email)
        return 1
    def changePassword(uid, passw):
            app.db.execute("""
    UPDATE Users
    SET email = :passw
    WHERE uid = :uid
    """,
                                uid = uid, passw = passw)
            return 1
    
    def changeAddress(uid, address):
        app.db.execute("""
UPDATE Users
SET address = :address
WHERE uid = :uid
""",
                              uid = uid, address = address)
        
        return 1
    @staticmethod

    def getUser(uid):
        rows = app.db.execute("""
SELECT uid, email, firstname, lastname, address, password, balance
FROM Users
WHERE uid = :uid
""",
                              uid=uid)
        return User(*(rows[0][0:]))
