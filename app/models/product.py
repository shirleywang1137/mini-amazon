from flask import current_app as app
from random import randint


class Product:
    def __init__(self, product_id, product_name, category, description, image, price, available, seller_id, quantity):
        self.product_id = product_id
        self.product_name = product_name
        self.category = category
        self.description = description
        self.image = image
        self.price = price
        self.available = available
        self.seller_id = seller_id
        self.quantity = quantity

    @staticmethod
    def get(product_id):
        rows = app.db.execute('''
SELECT product_id, product_name, category, description, image, price, available, seller_id, quantity
FROM Products
WHERE product_id = :product_id
''',
                              product_id=product_id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT product_id, product_name, category, description, image, price, available, seller_id, quantity
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_all_by_seller(seller_id, available=True):
        rows = app.db.execute('''
SELECT product_id, product_name, category, description, image, price, available, seller_id, quantity
FROM Products
WHERE seller_id = :seller_id
AND available = :available
''',
                              seller_id=seller_id,
                              available=available)
        return [Product(*row) for row in rows]
    @staticmethod
    def get_all_by_seller_search(seller_id,search_key, available=True):
        rows = app.db.execute('''
SELECT product_id, product_name, category, description, image, price, available, seller_id, quantity
FROM Products
WHERE seller_id = :seller_id and product_name LIKE CONCAT('%', :search_key, '%') 
AND available = :available
''',
                              seller_id=seller_id, search_key = search_key,
                              available=available)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_all_by_seller_sort_price_asc(seller_id,search_key, available=True):
        rows = app.db.execute('''
SELECT product_id, product_name, category, description, image, price, available, seller_id, quantity
FROM Products
WHERE seller_id = :seller_id and product_name LIKE CONCAT('%', :search_key, '%')
AND available = :available
ORDER BY price ASC
''',
                              seller_id=seller_id, search_key = search_key,
                              available=available)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_all_by_seller_sort_price_desc(seller_id,search_key, available=True):
        rows = app.db.execute('''
SELECT product_id, product_name, category, description, image, price, available, seller_id, quantity
FROM Products
WHERE seller_id = :seller_id and product_name LIKE CONCAT('%', :search_key, '%')
AND available = :available
ORDER BY price DESC
''',
                              seller_id=seller_id, search_key = search_key,
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_k_products(k, available=True):
        rows = app.db.execute('''
SELECT product_id, product_name, category, description, image, price, available, seller_id, quantity
FROM Products
WHERE available = :available
ORDER BY price DESC
LIMIT :k
''',
                              k = k,
                              available=available)
        return [Product(*row) for row in rows]

    def addProducts(product_id, seller_id, product_name, category, description, image,  price, available, quantity):
        app.db.execute("""
INSERT INTO Products
VALUES (:product_id, :seller_id, :product_name, :category, :description, :image, :price, :available, :quantity)
""",
                              product_id = product_id, seller_id = seller_id, product_name = product_name, category = category, description = description, image = image, price = price, available = available, quantity = quantity)
        
        return 1
    
    def editProducts(seller_id, old_product_name, product_name, category, description, image,  price, available, quantity):
        app.db.execute("""
UPDATE Products
SET product_name = :product_name, category = :category, description = :description, image = :image, price = :price, available = :available, quantity = :quantity
WHERE product_name = :old_product_name and seller_id = :seller_id
""",
                               seller_id = seller_id, old_product_name = old_product_name, product_name = product_name, category = category, description = description, image = image, price = price, available = available, quantity = quantity)
        
        return 1
    
    def removeProducts(uid, product_name):
        app.db.execute("""
DELETE FROM Products
WHERE seller_id = :uid AND product_name = :product_name
""",
                              uid = uid, product_name=product_name)
        
        return 1
    
    def removeProducts2(product_id):
        app.db.execute("""
DELETE FROM Orders
WHERE product_id = :product_id;
DELETE FROM Product_Reviews 
WHERE product_id = :product_id;
DELETE FROM Carts
WHERE product_id = :product_id;
DELETE FROM Products 
WHERE product_id = :product_id;
""",
                              product_id = product_id)
        
        return 1
    
    @staticmethod
    def get_all_by_seller_id(seller_id):
        rows = app.db.execute('''
SELECT product_id, product_name, category, description, image, price, available, seller_id, quantity
FROM Products
WHERE seller_id = :seller_id
''',
                              seller_id = seller_id)
        return [Product(*row) for row in rows]

    @staticmethod
    def withdrawInv(product_id, less):
        app.db.execute("""
UPDATE Products
SET quantity = quantity - :less
WHERE product_id = :product_id
""",
                              product_id = product_id, less=less)
        return 1
    
    def setquantity(seller_id, additional, product_name):
        app.db.execute("""
    UPDATE Products
    SET quantity = :additional
    WHERE seller_id = :seller_id and product_name = :product_name
    """,
                                seller_id = seller_id, additional=additional, product_name= product_name)
            
        return 1
    


class P1:
    def __init__(self, product_id, product_name, category, description, image, price, available, seller_id, quantity, rating, seller):
        self.product_id = product_id
        self.product_name = product_name
        self.category = category
        self.description = description
        self.image = image
        self.price = price
        self.available = available
        self.seller_id = seller_id
        self.quantity = quantity
        self.rating = rating
        self.percentage = (rating/5)*100
        self.seller = seller

    @staticmethod
    def search_products(search_key, available=True):
        rows = app.db.execute('''
    SELECT DISTINCT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, AVG(pr.rating) as avg_rating, s.seller
    FROM Products as p, Product_Reviews as pr, Sellers as s
    WHERE p.product_name LIKE CONCAT('%', :search_key, '%') 
    AND p.product_id = pr.product_id
    AND p.seller_id = s.uid
    GROUP BY p.product_id, p.category, s.seller
    ''',
                                search_key = search_key,
                                available=available)
        return [P1(*row) for row in rows]

class P2:
    def __init__(self, product_id, product_name, category, description, image, price, available, seller_id, quantity, rating, review, seller):
        self.product_id = product_id
        self.product_name = product_name
        self.category = category
        self.description = description
        self.image = image
        self.price = price
        self.available = available
        self.seller_id = seller_id
        self.quantity = quantity
        self.rating = rating
        self.percentage = (rating/5)*100
        self.review = review
        self.seller = seller



    @staticmethod
    def get(product_id):
        rows = app.db.execute('''
SELECT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, pr.rating, pr.review, s.seller
FROM Products as p, Product_Reviews as pr, Sellers as s
WHERE p.product_id = :product_id 
AND p.product_id = pr.product_id
AND p.seller_id = s.uid
''',
                              product_id=product_id)
        return P2(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, pr.rating, pr.review, s.seller
FROM Products as p, Product_Reviews as pr, Sellers as s
WHERE p.available = :available 
AND p.product_id = pr.product_id
AND p.seller_id = s.uid
''',
                              available=available)
        return [P2(*row) for row in rows]

    @staticmethod
    def get_all_by_seller(seller_id, available=True):
        rows = app.db.execute('''
SELECT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, pr.rating, pr.review, s.seller
FROM Products as p, Product_Reviews as pr, Sellers as s
WHERE p.seller_id = :seller_id 
AND p.product_id = pr.product_id
AND p.available = :available
AND p.seller_id = s.uid
''',
                              seller_id=seller_id,
                              available=available)
        return [P2(*row) for row in rows]

    @staticmethod
    def get_k_products(k, available=True):
        rows = app.db.execute('''
SELECT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, pr.rating, pr.review, s.seller
FROM Products as p, Product_Reviews as pr, Sellers as s
WHERE p.product_name LIKE CONCAT('%', :search_key, '%') 
AND p.product_id = pr.product_id
AND p.seller_id = s.uid
ORDER BY p.price DESC
LIMIT :k
''',
                              k = k,
                              available=available)
        return [P2(*row) for row in rows]

    
   
    @staticmethod
    def specific_prod(prod_id, available=True):
        rows = app.db.execute('''
    SELECT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, pr.rating, pr.review, s.seller
    FROM Products as p, Product_Reviews as pr, Sellers as s
    WHERE p.product_id = pr.product_id AND p.product_id = :prod_id 
    AND p.seller_id = s.uid
    ''',
                                prod_id = prod_id,
                                available=available)
        return [P2(*row) for row in rows]

    def addProducts(product_id, seller_id, product_name, category, description, image,  price, available, quantity):
        app.db.execute("""
INSERT INTO Products
VALUES (:product_id, :seller_id, :product_name, :category, :description, :image, :price, :available, :quantity)
""",
                              product_id = product_id, seller_id = seller_id, product_name = product_name, category = category, description = description, image = 0, price = price, available = available, quantity = quantity)
        
        return 1
    
    def removeProducts(uid, product_name):
        app.db.execute("""
DELETE FROM Products
WHERE seller_id = :uid AND product_name = :product_name
""",
                              uid = uid, product_name=product_name)
        
        return 1
    
    @staticmethod
    def get_all_by_seller_id(seller_id):
        rows = app.db.execute('''
SELECT DISTINCT product_id, product_name, category, description, image, price, available, seller_id, quantity
FROM Products as p
WHERE seller_id = :seller_id
''',
                              seller_id = seller_id)
        return [P2(*row) for row in rows]
 
    
    @staticmethod
    def search_related_products(prod_name, available=True):
        rows = app.db.execute('''
    SELECT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, AVG(pr.rating) as avg_rating, pr.review, s.seller
    FROM Products as p, Product_Reviews as pr, Sellers as s
    WHERE p.product_name LIKE CONCAT('%', SUBSTRING(:prod_name, 0, 5), '%') 
    AND p.product_id = pr.product_id 
    AND p.seller_id = s.uid
    AND p.available = :available
    AND p.product_name != :prod_name
    GROUP BY p.product_id, p.category, pr.review, s.seller
    ''',
                                prod_name = prod_name,
                                available=available)
        return [P2(*row) for row in rows]

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
    SELECT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, AVG(pr.rating) as avg_rating, pr.review, s.seller
    FROM Products as p, Product_Reviews as pr, Sellers as s
    WHERE p.product_id = pr.product_id 
    AND p.seller_id = s.uid
    AND p.available = :available
    GROUP BY p.product_id, p.category, pr.review, s.seller
    ''',
                                available=available)
        return [P2(*row) for row in rows]

    @staticmethod
    def search_name(search_key, sort, available=True):
        order_by1 = ''
        if sort == 'Price: High to Low':
            order_by1 = 'ORDER BY p.price DESC'
        if sort == 'Price: Low to High':
            order_by1 = 'ORDER BY p.price ASC'
        if sort == 'Average Rating: High to Low':
            order_by1 = 'ORDER BY avg_rating DESC'
        if sort == 'Average Rating: Low to High':
            order_by1 = 'ORDER BY avg_rating ASC' 

        SQL_str ='''SELECT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, AVG(pr.rating) as avg_rating, pr.review, s.seller
    FROM Products as p, Product_Reviews as pr, Sellers as s
    WHERE p.product_name LIKE CONCAT('%', :search_key, '%') 
    AND p.product_id = pr.product_id
    AND p.seller_id = s.uid
    AND p.available = :available
    GROUP BY p.product_id, p.category, pr.review, s.seller
                    '''
        SQL_str = SQL_str + '\n' + order_by1
        rows = app.db.execute(SQL_str,
                              search_key = search_key,
                              available=available,
                              sort = sort
                              )
        return [P2(*row) for row in rows]


    staticmethod
    def search_desc(search_key, sort, available=True):
        order_by1 = ''
        if sort == 'Price: High to Low':
            order_by1 = 'ORDER BY p.price DESC'
        if sort == 'Price: Low to High':
            order_by1 = 'ORDER BY p.price ASC'
        if sort == 'Average Rating: High to Low':
            order_by1 = 'ORDER BY avg_rating DESC'
        if sort == 'Average Rating: Low to High':
            order_by1 = 'ORDER BY avg_rating ASC' 


        SQL_str ='''SELECT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, AVG(pr.rating) as avg_rating, pr.review, s.seller
    FROM Products as p, Product_Reviews as pr, Sellers as s
    WHERE p.description LIKE CONCAT('%', :search_key, '%') 
    AND p.product_id = pr.product_id
    AND p.seller_id = s.uid
    AND p.available = :available
    GROUP BY p.product_id, p.category, pr.review, s.seller
                    '''
        SQL_str = SQL_str + '\n' + order_by1
        rows = app.db.execute(SQL_str,
                              search_key = search_key,
                              available=available,
                              sort = sort
                              )
        return [P2(*row) for row in rows]
    
    @staticmethod
    def search_name_range_price(search_key, sort, low, high, available=True):
        order_by1 = ''
        if sort == 'Price: High to Low':
            order_by1 = 'ORDER BY p.price DESC'
        if sort == 'Price: Low to High':
            order_by1 = 'ORDER BY p.price ASC'
        if sort == 'Average Rating: High to Low':
            order_by1 = 'ORDER BY avg_rating DESC'
        if sort == 'Average Rating: Low to High':
            order_by1 = 'ORDER BY avg_rating ASC'   


        SQL_str ='''SELECT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, AVG(pr.rating) as avg_rating, pr.review, s.seller
    FROM Products as p, Product_Reviews as pr, Sellers as s
    WHERE p.product_name LIKE CONCAT('%', :search_key, '%') 
    AND p.price BETWEEN :low AND :high
    AND p.product_id = pr.product_id
    AND p.seller_id = s.uid
    AND p.available = :available
    GROUP BY p.product_id, p.category, pr.review, s.seller
                    '''
        SQL_str = SQL_str + '\n' + order_by1
        rows = app.db.execute(SQL_str,
                              search_key = search_key,
                              available=available,
                              sort = sort,
                              low = low,
                              high = high
                              )
        return [P2(*row) for row in rows]

    @staticmethod
    def search_desc_range_price(search_key, sort, low, high, available=True):
        order_by1 = ''
        if sort == 'Price: High to Low':
            order_by1 = 'ORDER BY p.price DESC'
        if sort == 'Price: Low to High':
            order_by1 = 'ORDER BY p.price ASC'
        if sort == 'Average Rating: High to Low':
            order_by1 = 'ORDER BY avg_rating DESC'
        if sort == 'Average Rating: Low to High':
            order_by1 = 'ORDER BY avg_rating ASC'   


        SQL_str ='''SELECT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, AVG(pr.rating) as avg_rating, pr.review, s.seller
    FROM Products as p, Product_Reviews as pr, Sellers as s
    WHERE p.description LIKE CONCAT('%', :search_key, '%') 
    AND p.price BETWEEN :low AND :high
    AND p.product_id = pr.product_id
    AND p.seller_id = s.uid
    AND p.available = :available
    GROUP BY p.product_id, p.category, pr.review, s.seller
                    '''
        SQL_str = SQL_str + '\n' + order_by1
        rows = app.db.execute(SQL_str,
                              search_key = search_key,
                              available=available,
                              sort = sort, 
                              low = low,
                              high = high
                              )
        return [P2(*row) for row in rows]
        
    @staticmethod
    def search_name_filter_category(search_key, cat, sort, available=True):
        order_by1 = ''
        if sort == 'Price: High to Low':
            order_by1 = 'ORDER BY p.price DESC'
        if sort == 'Price: Low to High':
            order_by1 = 'ORDER BY p.price ASC'
        if sort == 'Average Rating: High to Low':
            order_by1 = 'ORDER BY avg_rating DESC'
        if sort == 'Average Rating: Low to High':
            order_by1 = 'ORDER BY avg_rating ASC'  


        SQL_str ='''SELECT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, AVG(pr.rating) as avg_rating, pr.review, s.seller
                    FROM Products as p, Product_Reviews as pr, Sellers as s
                    WHERE p.product_name LIKE CONCAT('%', :search_key, '%') 
                        AND p.product_id = pr.product_id
                        AND p.category = :cat
                        AND p.seller_id = s.uid
                        AND p.available = :available
                    GROUP BY p.product_id, pr.review, s.seller
                    '''
        SQL_str = SQL_str + '\n' + order_by1
        rows = app.db.execute(SQL_str,
                              search_key = search_key,
                              available=available,
                              sort = sort,
                              cat = cat
                              )
        return [P2(*row) for row in rows]

    @staticmethod
    def search_desc_filter_category(search_key, cat, sort, available=True):
        order_by1 = ''
        if sort == 'Price: High to Low':
            order_by1 = 'ORDER BY p.price DESC'
        if sort == 'Price: Low to High':
            order_by1 = 'ORDER BY p.price ASC'
        if sort == 'Average Rating: High to Low':
            order_by1 = 'ORDER BY avg_rating DESC'
        if sort == 'Average Rating: Low to High':
            order_by1 = 'ORDER BY avg_rating ASC'  


        SQL_str ='''SELECT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, AVG(pr.rating) as avg_rating, pr.review, s.seller
                    FROM Products as p, Product_Reviews as pr, Sellers as s
                    WHERE p.description LIKE CONCAT('%', :search_key, '%') 
                        AND p.product_id = pr.product_id
                        AND p.category = :cat
                        AND p.seller_id = s.uid
                        AND p.available = :available
                    GROUP BY p.product_id, pr.review, s.seller
                    '''
        SQL_str = SQL_str + '\n' + order_by1
        rows = app.db.execute(SQL_str,
                              search_key = search_key,
                              available=available,
                              sort = sort,
                              cat = cat
                              )
        return [P2(*row) for row in rows]

    @staticmethod
    def search_name_filter_category_range_price(search_key, cat, sort, low, high, available=True):
        order_by1 = ''
        if sort == 'Price: High to Low':
            order_by1 = 'ORDER BY p.price DESC'
        if sort == 'Price: Low to High':
            order_by1 = 'ORDER BY p.price ASC'
        if sort == 'Average Rating: High to Low':
            order_by1 = 'ORDER BY avg_rating DESC'
        if sort == 'Average Rating: Low to High':
            order_by1 = 'ORDER BY avg_rating ASC'  


        SQL_str ='''SELECT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, AVG(pr.rating) as avg_rating, pr.review, s.seller
                    FROM Products as p, Product_Reviews as pr, Sellers as s
                    WHERE p.product_name LIKE CONCAT('%', :search_key, '%')
                        AND p.price BETWEEN :low AND :high
                        AND p.product_id = pr.product_id
                        AND p.category = :cat
                        AND p.seller_id = s.uid
                        AND p.available = :available
                    GROUP BY p.product_id, pr.review, s.seller
                    '''
        SQL_str = SQL_str + '\n' + order_by1
        rows = app.db.execute(SQL_str,
                              search_key = search_key,
                              available=available,
                              sort = sort,
                              cat = cat,
                              low = low,
                              high = high
                              )
        return [P2(*row) for row in rows]

    @staticmethod
    def search_desc_filter_category_range_price(search_key, cat, sort, low, high, available=True):
        order_by1 = ''
        if sort == 'Price: High to Low':
            order_by1 = 'ORDER BY p.price DESC'
        if sort == 'Price: Low to High':
            order_by1 = 'ORDER BY p.price ASC'
        if sort == 'Average Rating: High to Low':
            order_by1 = 'ORDER BY avg_rating DESC'
        if sort == 'Average Rating: Low to High':
            order_by1 = 'ORDER BY avg_rating ASC' 

        SQL_str ='''SELECT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, AVG(pr.rating) as avg_rating, pr.review, s.seller
                    FROM Products as p, Product_Reviews as pr, Sellers as s
                    WHERE p.decription LIKE CONCAT('%', :search_key, '%')
                        AND p.price BETWEEN :low AND :high
                        AND p.product_id = pr.product_id
                        AND p.category = :cat
                        AND p.seller_id = s.uid
                        AND p.available = :available
                    GROUP BY p.product_id, pr.review, s.seller
                    '''
        SQL_str = SQL_str + '\n' + order_by1
        rows = app.db.execute(SQL_str,
                              search_key = search_key,
                              available=available,
                              sort = sort,
                              cat = cat,
                              low = low,
                              high = high
                              )
        return [P2(*row) for row in rows]