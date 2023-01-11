This is the README.txt. This summarizes who our team members are, their roles, and what we have done since the last checkpoint.

Team members: Jerry Xin, Shirley Wang, Henry Huynh, Jachin Friday, Chris Cameron

Jerry Xin - Users Guru: responsible for Account / Purchases
Shirley Wang - Products Guru: responsible for Products
Chris Cameron - Carts Guru: responsible for Cart / Order
Jachin Friday - Sellers Guru: responsible for Inventory / Order Fulfillment
Henry Huynh - Social Guru: responsible for Feedback / Messaging

Updates this week:
Jerry Xin - Worked on Database Design Schema with Chris
Shirley Wang - Worked on website Design Schema
Chris Cameron - Worked on Database population within create.sql, load.sql, and gen.py files.
Jachin Friday - Helped test Database
Henry Huynh - Helped Create E/R diagram.

Link to access github Repository, with all code: https://gitlab.oit.duke.edu/mx47/mini-amazon-skeleton
The code to populate the sample database is found under mx47/mini-amazon-skeleton/db/data.

The three files used to generate the sample data are:
mx47/mini-amazon-skeleton/db/create.sql
mx47/mini-amazon-skeleton/db/load.sql
mx47/mini-amazon-skeleton/db/generated/gen.py

These have been all edited to create a more comprehensive database that can catch more edge cases and provide an
overall more reliable set of test cases. 

Previously, we had:
num_users = 100
num_sellers = 20
num_products = 2000
num_carts = num_users
num_orders = 2500
num_product_reviews  = 500
num_seller_reviews = 200

Now, we have:
num_users = 200
num_sellers = 50
num_products = 20000
num_carts = num_users
num_orders = 25000
num_product_reviews  = 5000
num_seller_reviews = 2000

This represents a more comprehensive database that catches more edge cases and provides an overall more reliable set of test cases. We have increased the number of products, product reviews, and seller reviews 10 fold and increase the number of users from 100 to 200, and the number of sellers from 20 to 50.
