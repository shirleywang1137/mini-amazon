from flask import current_app as app
from flask_login import current_user


class Seller:
    def __init__(self, uid, seller):
        self.uid = uid
        self.seller = seller

    def registerSeller(uid,seller):
        rows = app.db.execute("""
INSERT INTO Sellers(uid, seller)
VALUES(:uid, :seller)
RETURNING uid
""",
                                  uid = uid, seller = seller)
        return 1
    
    def checkSeller(uid):
        rows = app.db.execute("""
        SELECT uid, seller
        FROM Sellers
        WHERE uid = :uid
""",
                                  uid = uid)
        return 1 if rows else 0
