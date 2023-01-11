from flask import current_app as app, flash


class Wishlist:
    def __init__(self, uid, product_id):
        self.uid = uid
        self.product_id = product_id

    @staticmethod
    def get(uid):
        rows = app.db.execute('''
SELECT uid, product_id
FROM Wishlist
WHERE uid = :uid
''',
                              uid= uid)
        return [Wishlist(*row) for row in rows]
    
  #  @staticmethod
  #  def get_items_in_cart_by_uid(uid):
  #      rows = app.db.execute('''
#SELECT uid, product_id, quantity
#FROM Carts
#WHERE uid = :uid
 #       ''', uid = uid)
  #      return [Cart(*row) for row in rows]
        
class Wishlistitem:
    def __init__(self, product_name, price, product_id):
        self.product_name = product_name
        self.price = price
        self.product_id = product_id
    
    @staticmethod
    def get_items_in_wishlist_by_uid(uid):
        rows = app.db.execute('''
SELECT Products.product_name, Products.price, Products.product_id
FROM Wishlist, Products
WHERE uid = :uid
  AND Wishlist.product_id = Products.product_id
''',
        uid = uid)
        return [Wishlistitem(*row) for row in rows]

    def add_item_to_wishlist(uid, product_id): #Will add functionality to choose quantity/update outstanding orders later
        try:
            rows = app.db.execute("""
INSERT INTO Wishlist(uid, product_id)
VALUES(:uid, :product_id)
""",
                                uid = uid,
                                product_id = product_id)
        except Exception as e:
            print("Failed to add to cart")
        #flash("Item Added")
        return None         

    @staticmethod
    def remove_item_from_wishlist(uid, product_id):
        try:
            rows = app.db.execute("""
DELETE FROM Wishlist WHERE uid = :uid AND product_id = :product_id 
""",
                                uid = uid,
                                product_id = product_id)
        except Exception as e:
            print("failed to delete item from cart")
        return None

    @staticmethod
    def clear_wishlist(uid):
        try:
            rows = app.db.execute("""
DELETE FROM Wishlist WHERE uid = :uid
""",
                                uid = uid)
        except Exception as e:
            print("Failed to delete user cart contents")
        return None
