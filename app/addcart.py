from pickle import FALSE, TRUE

from importlib_metadata import email
from app.models.product_review import Product_Review
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User
from .models.cart import Cart
from .models.cart import UserCart
from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('addcart', __name__)

class SearchForItemsByUIDForm(FlaskForm):
    id = StringField('User ID')
    submit = SubmitField('Get Cart')

class AddQuantityToCartForm(FlaskForm):
    quantity = IntegerField('Quantity')
    submit = SubmitField('Add To Cart')

@bp.route('/addcart', methods=['GET','POST'])
def addcart():
    product_id = request.args.get('pid')
    form = AddQuantityToCartForm()
    #If form already filled out
    if form.validate_on_submit():
        #Can't add more products than exist
        if Product.get(product_id).quantity > form.quantity.data:
            quantity = form.quantity.data
            if quantity > 0:
                UserCart.add_item_to_cart(current_user.uid, product_id, quantity)
            #Load Carts Page
            id = current_user.uid
            items_in_cart = UserCart.get_items_in_cart_by_uid(id)
            total = 0
            for item in items_in_cart:
                item.product_name = item.product_name[0]
                total += item.price*item.quantity
            return render_template('cart.html',
                                items = items_in_cart,
                                total = total)
        #Show error message
        else:
            flash("There are not enough available!")
    #Else Load Quantity Selection
    return render_template('addcart.html',
                            product_id = product_id,
                            form = form)

class UpdateQuantityInCartForm(FlaskForm):
    quantity = IntegerField('Quantity')
    submit = SubmitField('Update Amount')

@bp.route('/updatecart', methods=['GET','POST'])
def updatecart():
    product_id = request.args.get('pid')
    form = UpdateQuantityInCartForm()
    #If form already filled out
    if form.validate_on_submit():
        quantity = form.quantity.data
        if quantity > 0:
            UserCart.update_amount_in_cart(current_user.uid, product_id, quantity)
         #Load Carts Page
        id = current_user.uid
        items_in_cart = UserCart.get_items_in_cart_by_uid(id)
        total = 0
        for item in items_in_cart:
            item.product_name = item.product_name[0]
            total += item.price*item.quantity
        return render_template('cart.html',
                            items = items_in_cart,
                            total = total)
    #Else Load Quantity Selection
    return render_template('updateQuantity.html',
                            product_id = product_id,
                            form = form)
    

    
                           
@bp.route('/deletecart', methods=['GET','POST'])
def deletecart():
    #Remove From Cart
    product_id = request.args.get('pid')
    UserCart.remove_item_from_cart(current_user.uid, product_id) 
    #Load Carts Page
    id = current_user.uid
    items_in_cart = UserCart.get_items_in_cart_by_uid(id)
    total = 0
    for item in items_in_cart:
        item.product_name = item.product_name[0]
        total += item.price
    return render_template('cart.html',
                           items = items_in_cart,
                           total = total)
