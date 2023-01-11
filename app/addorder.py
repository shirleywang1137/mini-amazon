from pickle import FALSE, TRUE

from random import randint

from importlib_metadata import email
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

from datetime import datetime

from flask import Blueprint
bp = Blueprint('addorder', __name__)

class PurchaseHistoryForm(FlaskForm):
    myChoices1 = ['Most Recent', 'Price Ascend','Price Descend']
    myField1 = SelectField(choices = myChoices1, validators = None, default = 'None',label = 'Filter')
    myChoices = ['Search by Name','Search by Description']
    myField = SelectField(choices = myChoices, validators = None, default = 'None',label = 'Section Select')
    search_key = StringField('Key Word')
    submit = SubmitField('Update Search')

@bp.route('/addorder', methods=['GET','POST'])
def addorder():
    #Get Cart Info
    id = current_user.uid
    items_in_cart = Cart.get(id)
    total = float(request.args.get('total'))
    ordernum = randint(0,240000000)

    #Make a new order
    for item in items_in_cart:
        #Check Inventory
        productInfo = Product.get(item.product_id)
        if(productInfo.quantity < item.quantity):
            flash("Not enough of " + productInfo.product_name + " available")
        elif(productInfo.available == False):
            flash(productInfo.product_name + "is not available at this time, sorry!")
        #Check Balance
        elif(current_user.balance < total):
            flash("Insufficient Funds")
        #Add order
        else:
            #Remove From Inventory
            Product.withdrawInv(item.product_id, item.quantity)
            #Get product info
            current_product = Product.get(item.product_id)
            #Move money
            User.addBal(current_product.seller_id, current_product.price*item.quantity)
            User.withdrawBal(current_user.uid, current_product.price*item.quantity)
            #Move item
            UserCart.remove_item_from_cart(current_user.uid, item.product_id) 
            Purchase.add_new_order(randint(0,240000000), ordernum, item.product_id, current_product.seller_id, id, current_user.address, datetime.now(), item.quantity, False, datetime.now(), current_product.price)
    #Reload Carts Page
    total = 0
    items_in_cart = UserCart.get_items_in_cart_by_uid(id)
    for item in items_in_cart:
        item.product_name = item.product_name[0]
        total += item.price*item.quantity
    return render_template('cart.html',
                           items = items_in_cart,
                           total = total)
    #Delete Current Cart Contents
    #UserCart.clear_cart(id)
    #Go to orders page (will likely change)
"""     purchases = Purchase.get_all_by_uid(id)
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
                           form=PurchaseHistoryForm()) """
