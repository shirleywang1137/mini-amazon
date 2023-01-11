
from pickle import FALSE, TRUE

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
from .models.product import Product, P1, P2
from .models.purchase import Purchase
from .models.wishlist import Wishlist, Wishlistitem

from flask import Blueprint
bp = Blueprint('wishlistitem', __name__)


@bp.route('/wishlist', methods=['GET','POST'])
def wishlist():
    items = Wishlistitem.get_items_in_wishlist_by_uid(current_user.uid)
    return render_template('wishlist.html', items = items)

@bp.route('/addWishlist', methods=['GET','POST'])
def addWishlist():
    product_id = request.args.get('pid')
    id = current_user.uid
    Wishlistitem.add_item_to_wishlist(id,product_id)
    items_in_cart = Wishlistitem.get_items_in_wishlist_by_uid(id)
    return render_template('wishlist.html',
                            items = items_in_cart)
    
                           
@bp.route('/deleteWishlist', methods=['GET','POST'])
def deleteWishlist():
    #Remove From Cart
    product_id = request.args.get('pid')
    id = current_user.uid
    Wishlistitem.remove_item_from_wishlist(id, product_id) 
    #Load Carts Page
    items_in_wishlist = Wishlistitem.get_items_in_wishlist_by_uid(id)
    return render_template('wishlist.html',
                           items = items_in_wishlist)