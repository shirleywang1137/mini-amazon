from flask import current_app as app, flash


class Cart:
    def __init__(self, uid, product_id, quantity):
        self.uid = uid
        self.product_id = product_id
        self.quantity = quantity

    @staticmethod
    def get(uid):
        rows = app.db.execute('''
SELECT uid, product_id, quantity
FROM Carts
WHERE uid = :uid
''',
                              uid= uid)
        return [Cart(*row) for row in rows]

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT uid, product_id
FROM Carts
WHERE uid = :uid
AND time_added_to_cart >= :since
ORDER BY time_added_to_cart DESC
''',
                              uid=uid,
                              since=since)
        return [Cart(*row) for row in rows]
    
  #  @staticmethod
  #  def get_items_in_cart_by_uid(uid):
  #      rows = app.db.execute('''
#SELECT uid, product_id, quantity
#FROM Carts
#WHERE uid = :uid
 #       ''', uid = uid)
  #      return [Cart(*row) for row in rows]
        
class UserCart:
    def __init__(self, product_name, quantity, price, product_id):
        self.product_name = product_name,
        self.quantity = quantity
        self.price = price
        self.product_id = product_id
    
    @staticmethod
    def get_items_in_cart_by_uid(uid):
        rows = app.db.execute('''
SELECT products.product_name, carts.quantity, products.price, products.product_id
FROM Carts, Products
WHERE uid = :uid
  AND carts.product_id = products.product_id
''',
        uid = uid)
        return [UserCart(*row) for row in rows]

    def add_item_to_cart(uid, product_id, quantity): #Will add functionality to choose quantity/update outstanding orders later
        try:
            rows = app.db.execute("""
INSERT INTO Carts(uid, product_id, quantity)
VALUES(:uid, :product_id, :quantity)
""",
                                uid = uid,
                                product_id = product_id,
                                quantity = quantity)
        except Exception as e:
            print("Failed to add to cart")
        #flash("Item Added")
        return None

    @staticmethod
    def update_amount_in_cart(uid, product_id, quantity):
        try:
            rows = app.db.execute("""
UPDATE Carts SET quantity = :quantity WHERE uid = :uid AND product_id = :product_id
""",
                                uid = uid,
                                product_id = product_id,
                                quantity = quantity)
        except Exception as e:
            print("failed to update amount in cart")
        return None            

    @staticmethod
    def remove_item_from_cart(uid, product_id):
        try:
            rows = app.db.execute("""
DELETE FROM Carts WHERE uid = :uid AND product_id = :product_id 
""",
                                uid = uid,
                                product_id = product_id)
        except Exception as e:
            print("failed to delete item from cart")
        return None

    @staticmethod
    def clear_cart(uid):
        try:
            rows = app.db.execute("""
DELETE FROM Carts WHERE uid = :uid
""",
                                uid = uid)
        except Exception as e:
            print("Failed to delete user cart contents")
        return None


