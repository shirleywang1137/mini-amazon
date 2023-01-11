from app.models.product_review import Product_Review
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User
from .models.cart import Cart
from .models.cart import UserCart
from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('api', __name__)

@bp.route('/api', methods=['GET','POST'])
def api():
    return render_template('api.html', title='api')


class purchaseHistoryForm(FlaskForm):
    myChoices1 = ['Most Recent', 'Price Ascend','Price Descend']
    myField1 = SelectField(choices = myChoices1, validators = None, default = 'None',label = 'Filter')
    myChoices = ['Search by Name','Search by Description']
    myField = SelectField(choices = myChoices, validators = None, default = 'None',label = 'Section Select')
    search_key = StringField('Key Word')
    submit = SubmitField('Update Search')

@bp.route('/users', methods = ["GET", "POST"])
def users():
    form = purchaseHistoryForm()
    search_key = form.search_key.data
    uid = current_user.uid
    purchases = Purchase.get_all_by_uid(uid)
    if form.myField1.data == 'Price Ascend':
        purchases = Purchase.get_all_by_uid_price_asc(uid,search_key) 
    if form.myField1.data == 'Price Descend':
        purchases = Purchase.get_all_by_uid_price_desc(uid,search_key) 
    if form.myField1.data == 'Most Recent':
        purchases = Purchase.get_all_by_uid_most_recent(uid,search_key)
    for purchase in purchases:
        print(purchase.order_fulfilled)
        if(purchase.fulfillment):
            for purchase2 in purchases:
                if(purchase.superorder_id == purchase2.superorder_id and purchase2.fulfillment == False):
                    purchase.order_fulfilled = False
    return render_template('purchase.html',
                           purchase_history=purchases,
                           form=form)


class k_HighestPrice_Products(FlaskForm):
    k = IntegerField('Number of Products (please enter only positive integer values)')
    submit = SubmitField('Get Products')

@bp.route('/products', methods = ["GET", "POST"])
def products():
    form = k_HighestPrice_Products()
    k = form.k.data
    products = Product.get_k_products(k)
    return render_template('product.html',
                           avail_products = products,
                           form = form)

class UpdateCartQuantityForm(FlaskForm):
    quantity = StringField('')
    submit = SubmitField('Update')

@bp.route('/carts', methods = ["GET", "POST"])
def carts():
    form = UpdateCartQuantityForm()
    # given a user id, find the items in the cart for that user.
    id = current_user.uid
    items_in_cart = UserCart.get_items_in_cart_by_uid(id)
    total = 0
    for item in items_in_cart:
        item.product_name = item.product_name[0]
        total += item.price*item.quantity
    return render_template('cart.html',
                           items = items_in_cart,
                           total = total,
                           form = form)
    
class SearchForInventory(FlaskForm):
    seller_id = StringField('Seller ID')
    submit = SubmitField('Get Products')

@bp.route('/sellers', methods = ["GET", "POST"])
def sellers():
    form = SearchForInventory()
    seller_id = form.seller_id.data
    inventory = Product.get_all_by_seller(seller_id)
    return render_template('inventory.html',
                           avail_products = inventory,
                           form = form)



class RecentReviewsForm(FlaskForm):
    uid = StringField('User ID')
    submit = SubmitField('Get 5 Most Recent Reviews')

@bp.route('/social', methods = ["GET", "POST"])
def social():
    form = RecentReviewsForm()
    uid = form.uid.data
    reviews = Product_Review.get_recent_reviews(uid)
    return render_template('review.html',
                           reviews= reviews,
                           form= form)


