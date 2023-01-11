This is the README.txt for the Final Report. This summarizes who our team members are, their roles, and what we have done since the last checkpoint.

Team members: Jerry Xin, Shirley Wang, Henry Huynh, Jachin Friday, Chris Cameron

Jerry Xin - Users Guru: responsible for Account / Purchases
Shirley Wang - Products Guru: responsible for Products
Chris Cameron - Carts Guru: responsible for Cart / Order
Jachin Friday - Sellers Guru: responsible for Inventory / Order Fulfillment
Henry Huynh - Social Guru: responsible for Feedback / Messaging

Updates this week:
Jerry Xin - Finished User Guru Requirements, added/tested/implemented additonal bonus features, helped other teammates integrate features. Added user public view and seller public view page. Seller public view is connect to search products, and user public view is connected to all user reviews
Shirley Wang - Finished Product Guru Requirements for Mini Amazon Project, created product search, specific product, and wishlist pages, added/tested/implemented additonal bonus features, connected products to user and cart functions
Chris Cameron - Finished Carts Guru Requirements for Mini Amazon Project (Carts & Orders Pages), added/tested/implemented additonal bonus features including sorting and searching past orders and the ability to re-buy past orders. Helped teammates debug. Updated gen.py and the database schema
Jachin Friday - Finished Sellers Guru Requirements for Mini Amazon Project, added additonal bonus features including searching  seller inventory and search by price ascending,
Henry Huynh - Finished Social Guru Requirements for Mini Amazon Project, added/tested/implemented additional bonus features including seller product ratings page, helped modify database schema / gen for user and product reviews

Link to access github Repository, with all code: https://gitlab.oit.duke.edu/mx47/mini-amazon-skeleton

We would like to enter our project for an Audience Choice Award for Extra Credit.

The code to populate the sample database is found under mx47/mini-amazon-skeleton/db/data.

The three files used to generate the sample data are:
mx47/mini-amazon-skeleton/db/create.sql
mx47/mini-amazon-skeleton/db/load.sql
mx47/mini-amazon-skeleton/db/generated/gen.py

We have a data generator in these files that is capable of creating a much larger dataset(200 users, or more even). The size of the generated dataset can be changed by changing a variable. This is able to create a large scale dataset but we kept the value for generated users at 200 for the time being so our project runs quicker. Additionally, we can create larger values for the other tables, including Products, Reviews, etc. by changing a variable.

Here are the variables in gen.py that can be changed to increase the size of our generated data.
num_users = 200
num_sellers = 50
num_products = 20000
num_carts = num_users
num_orders = 25000
num_product_reviews  = 5000
num_seller_reviews = 2000

In order, we generated:
200 Users
50 Sellers
20000 Products
200 Carts
25000 Orders
5000 Product Reviews
2000 Seller Reviews

These is all to create a more comprehensive database that can catch more edge cases and provide an
overall more reliable set of test cases. Again, these numbers can be increased to have more data, but we thought that our values at the moment provide a comprehensive database.
