from pickle import FALSE, TRUE
from random import randint

from importlib_metadata import email
from app.models.product_review import Product_Review
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FileField, DecimalField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Regexp

from .models.user import User
from .models.cart import Cart
from .models.cart import UserCart
from .models.product import Product
from .models.purchase import Purchase
from .models.seller import Seller
from .models.product_review import Product_Review
from .models.seller_review import Seller_Review
from datetime import datetime

from flask import Blueprint
bp = Blueprint('sellerview', __name__)

def getTime():
    now = datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
    return dt_string

@bp.route('/sellerview', methods=['GET','POST'])
def sellerview():
    return render_template('sellerview.html', title='sellerview')


class addProductsForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    myChoices2 = ['None','tools','clothing','furniture',
'electronics','food','medicine',
'cleaning','appliances','home',
'toys','automotive','education','beauty']
    category = SelectField(choices = myChoices2, validators = None, default = 'None',label = 'Category Select')
    description = StringField('Product Description', validators=[DataRequired()])
    image = StringField('URL for Image', validators=[DataRequired()])
    price = DecimalField('Product Price', validators=[DataRequired()])
    quantity = IntegerField('Product Quantity', validators=[DataRequired()])
    available = BooleanField('Availability')
    submit = SubmitField('Add Product(s) to Inventory')

@bp.route('/addProducts', methods=['GET','POST'])
def addProducts():
    form = addProductsForm()
    if form.validate_on_submit():
        prod_id = randint(20000,24000000)
        dt_string = getTime()
        ret = Product.addProducts(prod_id, current_user.uid, form.product_name.data, form.category.data, form.description.data, form.image.data, form.price.data, form.available.data, form.quantity.data)
        Product_Review.addProductReview(prod_id,current_user.uid, "placeholder review", dt_string,5)
        return render_template('addProducts.html', form=form)
    return render_template('addProducts.html', form=form)

class removeProductsForm(FlaskForm):
    remove = StringField('Product Name', validators=[DataRequired()])
    submit = SubmitField('Remove Product')

@bp.route('/removeProducts', methods=['GET','POST'])
def removeProducts():
    form = removeProductsForm()
    if form.validate_on_submit():
        ret = Product.removeProducts(current_user.uid, form.remove.data)
        return render_template('removeProducts.html', form=form)
    return render_template('removeProducts.html', form=form)

@bp.route('/removeProducts2', methods=['GET','POST'])
def removeProducts2():
    form = inventoryHistoryForm()
    pid = request.args.get('uid')
    ret = Product.removeProducts2(pid)
    inventory = Product.get_all_by_seller_id(current_user.uid)
    return render_template('sellerInventory.html', inventory1 = inventory, form = form)

class editProductsForm(FlaskForm):
    old_product_name = StringField('Old Product Name', validators=[DataRequired()])
    product_name = StringField('New Product Name', validators=[DataRequired()])
    myChoices2 = ['None','tools','clothing','furniture',
'electronics','food','medicine',
'cleaning','appliances','home',
'toys','automotive','education','beauty']
    category = SelectField(choices = myChoices2, validators = None, default = 'None',label = 'Category Select')
    description = StringField('New Product Description', validators=[DataRequired()])
    image = StringField('URL for Image', validators=[DataRequired()])
    price = DecimalField('New Product Price', validators=[DataRequired()])
    quantity = IntegerField('New Product Quantity', validators=[DataRequired()])
    available = BooleanField('New Availability')
    submit = SubmitField('Edit Current Product in Inventory')

@bp.route('/editProducts', methods=['GET','POST'])
def editProducts():
    form = editProductsForm()
    if form.validate_on_submit():
        ret = Product.editProducts(current_user.uid, form.old_product_name.data, form.product_name.data, form.category.data, form.description.data, form.image.data, form.price.data, form.available.data, form.quantity.data)
        return render_template('editProducts.html', form=form)
    return render_template('editProducts.html', form=form)


class inventoryHistoryForm(FlaskForm):
    myChoices1 = ['None', 'Price Ascend','Price Descend']
    myField1 = SelectField(choices = myChoices1, validators = None, default = 'None',label = 'Filter')
    myChoices = ['Search by Name','Search by Description']
    myField = SelectField(choices = myChoices, validators = None, default = 'None',label = 'Section Select')
    search_key = StringField('Key Word')
    submit = SubmitField('Update Search')


@bp.route('/inventory', methods=['GET', 'POST'])
def inventory():
    uid = current_user.uid
    inventory = Product.get_all_by_seller(uid)
    form = inventoryHistoryForm()
    search_key = form.search_key.data
    if form.myField1.data == 'None':
        inventory = Product.get_all_by_seller_search(uid,search_key) 
    if form.myField1.data == 'Price Ascend':
        inventory = Product.get_all_by_seller_sort_price_asc(uid,search_key) 
    if form.myField1.data == 'Price Descend':
        inventory = Product.get_all_by_seller_sort_price_desc(uid,search_key) 
    return render_template('sellerInventory.html', inventory1 = inventory, form = form)

@bp.route('/fulfillment', methods=['GET', 'POST'])
def fulfillment():
    if current_user.is_authenticated: 
        inventory = Purchase.get_all_by_fulfillment_status(current_user.uid)
    else:
        inventory = None
    return render_template('sellerFulfilled.html', inventory1 = inventory)

@bp.route('/allOrders', methods=['GET', 'POST'])
def allOrders():
    if current_user.is_authenticated: 
        inventory = Purchase.get_all_by_seller_id(current_user.uid)
    else:
        inventory = None
    return render_template('sellerAllOrders.html', inventory1 = inventory)

class addQuantityForm(FlaskForm):
    neg = 0
    name = StringField('Name of Product', validators=[DataRequired()])
    quantity = IntegerField('Product Quantity', validators=[DataRequired()])
    submit = SubmitField('Add Quantity to Inventory')

@bp.route('/setQuantity', methods = ["GET", "POST"])
def setQuantity():
    form = addQuantityForm()
    if form.validate_on_submit():
        quantity = form.quantity.data
        name = form.name.data
        if form.quantity.data < 0 :
            form.neg = 1
            return render_template('setquantity.html',
                           form=form)
        else:
            ret = Product.setquantity(current_user.uid, quantity, name)
            return render_template('setquantity.html',
                           form=form)
    return render_template('setquantity.html', form=form)

@bp.route('/fulfill', methods=['GET','POST'])
def fulfill():
    order_id = int(request.args.get('order_id'))
    Purchase.removeProductsbyFulfillmentStatus(current_user.uid, order_id) 
    inventory = Purchase.get_all_by_fulfillment_status(current_user.uid)
    return render_template('sellerFulfilled.html',
                           inventory1 = inventory)

@bp.route('/productRating', methods = ['GET', 'POST'])
def getProductRatings():
    if current_user.is_authenticated:
        rating = Seller_Review.get_average_seller_product_rating(current_user.uid)
        rating = str(rating)[11:-5]
        if rating == '':
            rating = 0.0
        rating = float(rating)
        
        
    else: 
        rating = 0.0
    return render_template('sellerProductRating.html', rating = rating)
