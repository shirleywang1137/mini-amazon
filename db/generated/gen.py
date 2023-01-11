from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random

num_users = 200
num_sellers = 50
num_products = 20000
num_carts = num_users
num_wish = num_users
num_orders = 25000
num_product_reviews  = 5000
num_seller_reviews = 2000

Faker.seed(1)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    available_uids = []
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            available_uids.append(uid)
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            balance = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            firstname = profile['name'].split(" ")[0]
            lastname = profile['name'].split(" ")[1]
            address = profile['address']
            writer.writerow([uid, email, firstname, lastname, address, password, balance])
        print(f'{num_users} generated')
    return available_uids

def gen_sellers(num_sellers, available_uids):
    available_sids = []
    with open('Sellers.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Sellers...', end=' ', flush=True)
        for i in range(num_sellers):
            if i % 10 == 0:
                print(f'{i}', end=' ', flush=True)
            profile = fake.profile()
            uid = i #avoid overlaps
            available_sids.append(uid)
            seller = profile['company']
            writer.writerow([uid, seller])
        print(f'{num_sellers} generated')
    return available_sids

def gen_products(num_products, available_sids):
    my_word_list = [
'tools','clothing','furniture',
'electronics','food','medicine',
'cleaning','appliances','home',
'toys','automotive','education','beauty' ]

    available_pids = []
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for product_id in range(num_products):
            if product_id % 100 == 0:
                print(f'{product_id}', end=' ', flush=True)
            seller_id = fake.random_element(elements = available_sids)
            product_name = fake.sentence(nb_words=4)[:-1]
            category = fake.word(ext_word_list=my_word_list)
            description = fake.sentence(nb_words = 20) [:-1]
            image = fake.image_url()
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            available = fake.random_element(elements=('true', 'false'))
            if available == 'true':
                available_pids.append(product_id)
            quantity = fake.random_int(min = 1, max = 999)
            writer.writerow([product_id, seller_id, product_name, category, description, image, price, available, quantity])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids

def gen_carts(num_carts):
    with open('Carts.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Carts...', end=' ', flush=True)
        set = []
        for i in range(num_carts):
            if i % 10 == 0:
                print(f'{i}', end=' ', flush=True)
            uid = i 
            for i in range(random.randint(0,9)):
                product_id = fake.random_element(elements = available_pids) 
                quantity = fake.random_int(min = 1, max = 9)
                pair = (uid, product_id)
                if pair not in set:
                    set.append(pair)
                    writer.writerow([uid, product_id, quantity])
        print(f'{num_users} generated')
    return
    
def gen_wishlist(num_wish):
    with open('Wishlist.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Wishlist...', end=' ', flush=True)
        set = []
        for i in range(num_wish):
            if i % 10 == 0:
                print(f'{i}', end=' ', flush=True)
            uid = i 
            for i in range(random.randint(0,9)):
                product_id = fake.random_element(elements = available_pids) 
                pair = (uid, product_id)
                if pair not in set:
                    set.append(pair)
                    writer.writerow([uid, product_id])
        print(f'{num_wish} generated')
    return

def gen_orders(num_orders, available_uids, available_pids, available_sids):
    with open('Orders.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Orders...', end=' ', flush = True)
        for id in range(num_orders):
            order_id = id
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            superorder_id = fake.random_int(min = 1, max = 9)
            product_id = fake.random_element(elements = available_pids)
            seller_id = fake.random_element(elements = available_sids)
            uid = fake.random_element(elements = available_uids)
            address = fake.address()
            order_time = fake.date_time()    
            quantity = fake.random_int(min = 1, max = 9)
            fulfillment = fake.random_element(elements=('true', 'false'))
            fulfillment_time = fake.date_time_between(start_date = order_time)
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            writer.writerow([order_id, superorder_id, product_id, seller_id, uid, address, order_time, quantity, fulfillment, fulfillment_time, price])
        print(f'{num_orders} generated')
    return
    
def gen_product_reviews(num_product_reviews, available_pids, available_uids):
    with open ('Product_Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Product Reviews...', end=' ', flush = True)
        set = []
        for id in range(num_product_reviews):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            product_id = fake.random_element(elements = available_pids)
            uid = fake.random_element(elements = available_uids)
            pair = (product_id, uid)
            if pair not in set:
                set.append(pair)
                review = fake.sentence(nb_words = 20) [:-1]
                review_time = fake.date_time()
                rating = random.randint(1, 5)
                writer.writerow([product_id, uid, review, review_time, rating])
            else:
                continue
        print(f'{num_product_reviews} generated')
    return
    
def gen_seller_reviews(num_seller_reviews, available_sids, available_uids):
    with open ('Seller_Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Seller Reviews...', end=' ', flush = True)
        set = []
        for id in range(num_seller_reviews):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            seller_id = fake.random_element(elements = available_sids)
            reviewer_id = fake.random_element(elements = available_uids)
            pair = (seller_id, reviewer_id)
            if pair not in set:
                set.append(pair)
                review = fake.sentence(nb_words = 20) [:-1]
                review_time = fake.date_time()
                rating = random.randint(1, 5)
                writer.writerow([seller_id, reviewer_id, review, review_time, rating])
            else:
                continue
        print(f'{num_product_reviews} generated')
    return



available_uids = gen_users(num_users)
available_sids = gen_sellers(num_sellers, available_uids)
available_pids = gen_products(num_products, available_sids)
gen_carts(num_carts)
gen_orders(num_orders, available_uids, available_pids, available_sids)
gen_product_reviews(num_product_reviews, available_pids, available_uids)
gen_seller_reviews(num_seller_reviews, available_sids, available_uids)
gen_wishlist(num_wish)
