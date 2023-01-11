from flask import current_app as app


#CREATE TABLE Seller_Reviews(
#    seller_id INT NOT NULL REFERENCES Sellers(uid),
#    reviewer_id INT NOT NULL REFERENCES Users(uid),
#    review VARCHAR(65535) NOT NULL,
#    review_time timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
#    rating INT NOT NULL,
#    PRIMARY KEY(reviewer_id, seller_id)
#);
class Seller_Review:
    def __init__(self, seller_id, reviewer_id, review, review_time, rating):
        self.seller_id = seller_id
        self.reviewer_id = reviewer_id
        self.review = review
        self.review_time = review_time
        self.rating = rating

    @staticmethod
    def addSellerReview(seller_id, reviewer_id, review, review_time, rating):
        app.db.execute("""
    INSERT INTO Seller_Reviews(seller_id, reviewer_id, review, review_time, rating)
    VALUES(:seller_id, :reviewer_id, :review, :review_time, :rating)
    """,
                                seller_id = seller_id, reviewer_id=reviewer_id, review=review, review_time = review_time, rating = rating)
            
        return 1

    @staticmethod
    def getAllUserReview(reviewer_id):
        rows = app.db.execute("""
    SELECT seller_id, reviewer_id, review, review_time, rating
    FROM Seller_Reviews
    WHERE reviewer_id = :reviewer_id
    ORDER BY review_time DESC
    """,
                                reviewer_id = reviewer_id)
        return [Seller_Review(*row) for row in rows] 
    
    @staticmethod
    def getAllSellerReview(seller_id):
        rows = app.db.execute("""
    SELECT seller_id, reviewer_id, review, review_time, rating
    FROM Seller_Reviews
    WHERE seller_id = :seller_id
    ORDER BY review_time DESC
    """,
                                seller_id = seller_id)
        return [Seller_Review(*row) for row in rows] 

    def get_all_sellers():
        rows = app.db.execute("""
    SELECT seller_id, reviewer_id, review, review_time, rating
    FROM Seller_Reviews
    ORDER BY review_time DESC
    """,
                                )
        return [Seller_Review(*row) for row in rows] 
    
    def get_all_seller_reviews(search_key):
        rows = app.db.execute("""
    SELECT seller_id, reviewer_id, review, review_time, rating
    FROM Seller_Reviews
    WHERE review LIKE CONCAT('%', :search_key, '%')
    """,search_key = search_key
                                )
        return [Seller_Review(*row) for row in rows] 
    
    def get_all_seller_reviews_most_recent(search_key):
        rows = app.db.execute("""
    SELECT seller_id, reviewer_id, review, review_time, rating
    FROM Seller_Reviews
    WHERE review LIKE CONCAT('%', :search_key, '%')
    ORDER BY review_time DESC
    """,search_key = search_key
                                )
        return [Seller_Review(*row) for row in rows] 
    
    def get_all_seller_reviews_rating_asc(search_key):
        rows = app.db.execute("""
    SELECT seller_id, reviewer_id, review, review_time, rating
    FROM Seller_Reviews
    WHERE review LIKE CONCAT('%', :search_key, '%')
    ORDER BY rating ASC
    """,search_key = search_key
                                )
        return [Seller_Review(*row) for row in rows] 
    
    def get_all_seller_reviews_rating_desc(search_key):
        rows = app.db.execute("""
    SELECT seller_id, reviewer_id, review, review_time, rating
    FROM Seller_Reviews
    WHERE review LIKE CONCAT('%', :search_key, '%')
    ORDER BY rating DESC
    """,search_key = search_key
                                )
        return [Seller_Review(*row) for row in rows] 


    def deleteSellerReview(reviewer_id, seller_id):
        rows = app.db.execute("""
    DELETE FROM Seller_Reviews
    WHERE reviewer_id = :reviewer_id AND seller_id = :seller_id
    """,
                                reviewer_id = reviewer_id, seller_id = seller_id)

        return 1
    
    def updateSellerReview(uid, product_id, review, review_time, rating):
        rows = app.db.execute("""
    UPDATE Seller_Reviews
    SET review = :review, review_time = :review_time, rating = :rating
    WHERE reviewer_id = :reviewer_id AND seller_id = :seller_id
    """,
                                reviewer_id = reviewer_id, seller_id = seller_id, review = review, 
                                review_time = review_time, rating = rating)

        return 1

    @staticmethod
    def get_average_seller_product_rating(uid, available=True):
        avg_rating = app.db.execute('''

    SELECT SUM(a.avg_rating)/COUNT(a.avg_rating) as complete_avg
    FROM (SELECT AVG(pr.rating) as avg_rating
    FROM Products as p, Product_Reviews as pr, Sellers as s
    WHERE s.uid = :uid 
    AND p.product_id = pr.product_id
    AND p.seller_id = s.uid
    GROUP BY p.product_id, s.uid, pr.rating) a
    ''', 
    
                            uid = uid)
        return avg_rating