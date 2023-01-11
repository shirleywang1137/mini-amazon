-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:

\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.users_uid_seq',
                         (SELECT MAX(uid)+1 FROM Users),
                         false);

                      
\COPY Sellers FROM 'Sellers.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Carts FROM 'Carts.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Wishlist FROM 'Wishlist.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Orders FROM 'Orders.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Product_Reviews FROM 'Product_Reviews.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Seller_Reviews FROM 'Seller_Reviews.csv' WITH DELIMITER ',' NULL '' CSV


