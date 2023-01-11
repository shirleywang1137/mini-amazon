This is the README.txt for Milestone 3. This summarizes who our team members are, their roles, and what we have done since the last checkpoint.

Team members: Jerry Xin, Shirley Wang, Henry Huynh, Jachin Friday, Chris Cameron

Jerry Xin - Users Guru: responsible for Account / Purchases
Shirley Wang - Products Guru: responsible for Products
Chris Cameron - Carts Guru: responsible for Cart / Order
Jachin Friday - Sellers Guru: responsible for Inventory / Order Fulfillment
Henry Huynh - Social Guru: responsible for Feedback / Messaging

Updates this week:
Jerry Xin - Worked on User Guru Requirements for Mini Amazon Project(Login, Change balance/name/address, etc)
Shirley Wang - Worked on Product Guru Requirements for Mini Amazon Project
Chris Cameron - Worked on Carts Guru Requirements for Mini Amazon Project (Carts & Orders Pages), Updated gen.py
Jachin Friday - Worked on Sellers Guru Requirements for Mini Amazon Project
Henry Huynh - Worked on Social Guru Requirements for Mini Amazon Project

Link to access github Repository, with all code: https://gitlab.oit.duke.edu/mx47/mini-amazon-skeleton

The code to populate the sample database is found under mx47/mini-amazon-skeleton/db/data.

The three files used to generate the sample data are:
mx47/mini-amazon-skeleton/db/create.sql
mx47/mini-amazon-skeleton/db/load.sql
mx47/mini-amazon-skeleton/db/generated/gen.py

We have a data generator in these files that is capaable of creating a much larger dataset(100 users, or more even). The size of the generated dataset can be changed by changing a variable. This is able to create a large scale dataset but we kept the value for generated users at 100 for the time being so our project runs quicker. Additionally, we can create larger values for the other tables, including Products, Reviews, etc. by changing a variable.

These is all to create a more comprehensive database that can catch more edge cases and provide an
overall more reliable set of test cases.
