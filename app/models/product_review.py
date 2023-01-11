from flask import current_app as app


#   product_id INT NOT NULL REFERENCES Products(product_id),
#    uid INT NOT NULL REFERENCES Users(uid),
#    review VARCHAR(65535) NOT NULL,
#    review_time timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
#    PRIMARY KEY(uid, product_id)
class Product_Review:
    def __init__(self, product_id, uid, review, review_time, rating):
        self.product_id = product_id
        self.uid = uid
        self.review = review
        self.review_time = review_time
        self.rating = rating

    @staticmethod
    def get(product_id, uid):
        rows = app.db.execute('''
SELECT product_id, uid, review, review_time, rating
FROM Product_Reviews
WHERE product_id = :product_id AND uid = :uid
''',
                              product_id=product_id, 
                              uid=uid)
        return Product_Review(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT product_id, uid, review, review_time, rating
FROM Product_Reviews
''',
                              )
        return [Product_Review(*row) for row in rows]

    @staticmethod
    def get_recent_reviews(uid):
        rows = app.db.execute('''
SELECT product_id, uid, review, review_time, rating
FROM Product_Reviews
WHERE uid = :uid
ORDER BY review_time DESC
LIMIT 5
''',
                              uid=uid)
        return [Product_Review(*row) for row in rows]

    @staticmethod
    def addProductReview(product_id, uid, review, review_time, rating):
        app.db.execute("""
    INSERT INTO Product_Reviews(product_id, uid, review, review_time, rating)
    VALUES(:product_id, :uid, :review, :review_time, :rating)
    """,
                                uid = uid, product_id=product_id, review=review, review_time = review_time, rating = rating)
            
        return 1

    @staticmethod
    def getAllUserReview(uid):
        rows = app.db.execute("""
    SELECT product_id, uid, review, review_time, rating
    FROM Product_Reviews
    WHERE uid = :uid
    ORDER BY review_time DESC
    """,
                                uid = uid)
        return [Product_Review(*row) for row in rows] 

    @staticmethod
    def getAllProductReview(pid):
        rows = app.db.execute("""
    SELECT product_id, uid, review, review_time, rating
    FROM Product_Reviews
    WHERE product_id = :pid
    ORDER BY review_time DESC
    """,
                                pid = pid)
        return [Product_Review(*row) for row in rows] 
    
    @staticmethod
    def getAllProducts():
        rows = app.db.execute("""
    SELECT product_id, uid, review, review_time, rating
    FROM Product_Reviews
    ORDER BY review_time DESC
    """,
                                )
        return [Product_Review(*row) for row in rows] 
    
    def get_all_product_reviews(search_key):
        rows = app.db.execute("""
    SELECT product_id, uid, review, review_time, rating
    FROM Product_Reviews
    WHERE review LIKE CONCAT('%', :search_key, '%')
    """,search_key = search_key
                                )
        return [Product_Review(*row) for row in rows] 
    
    def get_all_by_rating_asc(search_key):
        rows = app.db.execute("""
    SELECT product_id, uid, review, review_time, rating
    FROM Product_Reviews
    WHERE review LIKE CONCAT('%', :search_key, '%')
    ORDER BY rating ASC
    """,search_key = search_key
                                )
        return [Product_Review(*row) for row in rows] 
    
    def get_all_by_rating_desc(search_key):
        rows = app.db.execute("""
    SELECT product_id, uid, review, review_time, rating
    FROM Product_Reviews
    WHERE review LIKE CONCAT('%', :search_key, '%')
    ORDER BY rating DESC
    """,search_key= search_key
                                )
        return [Product_Review(*row) for row in rows] 
    
    def get_all_by_most_recent(search_key):
        rows = app.db.execute("""
    SELECT product_id, uid, review, review_time, rating
    FROM Product_Reviews
    WHERE review LIKE CONCAT('%', :search_key, '%')
    ORDER BY review_time DESC
    """,search_key  = search_key
                                )
        return [Product_Review(*row) for row in rows] 

    def deleteUserReview(uid, product_id):
        rows = app.db.execute("""
    DELETE FROM Product_Reviews
    WHERE uid = :uid AND product_id = :product_id
    """,
                                uid = uid, product_id = product_id)

        return 1
    
    def updateUserReview(uid, product_id, review, review_time, rating):
        rows = app.db.execute("""
    UPDATE Product_Reviews
    SET review = :review, review_time = :review_time, rating = :rating
    WHERE uid = :uid AND product_id = :product_id
    """,
                                uid = uid, product_id = product_id, review = review, 
                                review_time = review_time, rating = rating)

        return 1
