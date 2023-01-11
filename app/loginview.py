from pickle import FALSE, TRUE

from importlib_metadata import email
from app.models.product_review import Product_Review
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, DecimalField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User
from .models.cart import Cart
from .models.cart import UserCart
from .models.product import Product
from .models.purchase import Purchase
from .models.seller import Seller
from .models.product_review import Product_Review
from .models.seller_review import Seller_Review

from flask import Blueprint
bp = Blueprint('loginview', __name__)

@bp.route('/loginview', methods=['GET','POST'])
def loginview():
    return render_template('loginview.html', title='loginview')

class AddBalanceForm(FlaskForm):
    neg = 0
    add = DecimalField('Additional Balance', validators=[DataRequired()])
    submit = SubmitField('Add Balance to Account')

@bp.route('/addBalance', methods = ["GET", "POST"])
def addBalance():
    form = AddBalanceForm()
    if form.validate_on_submit():
        additional = form.add.data
        if(additional < 0):
            form.neg = 1
            return render_template('addBalance.html',
                           form=form)
        else:
            ret = User.addBal(current_user.uid, additional)
            return render_template('addBalance.html',
                           form=form)
    return render_template('addBalance.html', form=form)

class SetBalanceForm(FlaskForm):
    negbal = 0
    set = DecimalField('Set Balance to this number', validators=[DataRequired()])
    submit = SubmitField('Set Balance')

@bp.route('/setBalance', methods = ["GET", "POST"])
def setBalance():
    form = SetBalanceForm()
    if form.validate_on_submit():
        set = form.set.data
        if set < 0:
            form.negbal = 1
            return render_template('setBalance.html',
                           form=form)
        else:
            ret = User.setBal(current_user.uid, set)
            return render_template('setBalance.html',
                           form=form)
    return render_template('setBalance.html', form=form)

class GiftBalanceForm(FlaskForm):
    neggift = 0
    overdrawn = 0
    userid = IntegerField('User ID of Gift', validators=[DataRequired()])
    gift = DecimalField('Amount to Gift', validators=[DataRequired()])
    submit = SubmitField('Send Gift')

@bp.route('/giftBalance', methods = ["GET", "POST"])
def giftBalance():
    form = GiftBalanceForm()
    if form.validate_on_submit():
        giftid = form.userid.data
        gift = form.gift.data
        if gift < 0:
            form.neggift = 1
            return render_template('giftBalance.html',
                           form=form)
        elif current_user.balance < gift:
            form.overdrawn = 1
            return render_template('giftBalance.html',
                           form=form)
        else:
            User.addBal(giftid, gift)
            User.withdrawBal(current_user.uid, gift)
            return render_template('giftBalance.html',
                           form=form)
    return render_template('giftBalance.html', form=form)

class WithdrawBalanceForm(FlaskForm):
    overdrawn = 0
    neg = 0
    withdraw = DecimalField('Withdraw Balance', validators=[DataRequired()])
    submit = SubmitField('Withdraw Balance From Account')

@bp.route('/withdrawBalance', methods = ["GET", "POST"])
def withdrawBalance():
    form = WithdrawBalanceForm()
    if form.validate_on_submit():
        less = form.withdraw.data
        if current_user.balance < less:
            form.overdrawn = 1
            return render_template('withdrawBalance.html',
                           form=form)
        if less < 0:
            form.neg = 1
            return render_template('withdrawBalance.html',
                           form=form)
        else:
            ret = User.withdrawBal(current_user.uid, less)
            return render_template('withdrawBalance.html',
                           form=form)
    return render_template('withdrawBalance.html', form=form)

class NameForm(FlaskForm):
    firstname = StringField('New first name', validators=[DataRequired()])
    lastname = StringField('New last name', validators=[DataRequired()])
    submit = SubmitField('Set New Account Name')

@bp.route('/changeName', methods = ["GET", "POST"])
def changeName():
    form = NameForm()
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        ret = User.changeName(current_user.uid, firstname, lastname)
        return render_template('changeName.html',
                           form=form)
    return render_template('changeName.html', form=form)

class EmailForm(FlaskForm):
    email = StringField('New Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Set New Email')
    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')

@bp.route('/changeEmail', methods = ["GET", "POST"])
def changeEmail():
    form = EmailForm()
    if form.validate_on_submit():
        email = form.email.data
        ret = User.changeEmail(current_user.uid, email)
        return render_template('changeEmail.html',
                           form=form)
    return render_template('changeEmail.html', form=form)

class PasswordForm(FlaskForm):
    passw = StringField('New Password', validators=[DataRequired()])
    submit = SubmitField('Set New Password')

@bp.route('/changePassword', methods = ["GET", "POST"])
def changePassword():
    form = PasswordForm()
    if form.validate_on_submit():
        passw = form.passw.data
        ret = User.changePassword(current_user.uid, passw)
        return render_template('changePassword.html',
                           form=form)
    return render_template('changePassword.html', form=form)

class AddressForm(FlaskForm):
    address = StringField('New Address', validators=[DataRequired()])
    submit = SubmitField('Set New Address')

@bp.route('/changeAddress', methods = ["GET", "POST"])
def changeAddress():
    form = AddressForm()
    if form.validate_on_submit():
        address = form.address.data
        ret = User.changeAddress(current_user.uid, address)
        return render_template('changeAddress.html',
                           form=form)
    return render_template('changeAddress.html', form=form)

class SellerForm(FlaskForm):
    name = StringField('Seller Name', validators=[DataRequired()])
    submit = SubmitField('Set New Seller')

@bp.route('/registerSeller', methods = ["GET", "POST"])
def registerSeller():
    form = SellerForm()
    if form.validate_on_submit():
        name = form.name.data
        ret = Seller.registerSeller(current_user.uid, name)
        return render_template('registerSeller.html',
                           form=form)
    return render_template('registerSeller.html', form=form)

class purchaseHistoryForm(FlaskForm):
    myChoices1 = ['None', 'Most Recent', 'Price Ascend','Price Descend']
    myField1 = SelectField(choices = myChoices1, validators = None, default = 'None',label = 'Filter')
    myChoices = ['None','Search by Name','Search by Description']
    myField = SelectField(choices = myChoices, validators = None, default = 'None',label = 'Section Select')
    search_key = StringField('Key Word')
    submit = SubmitField('Update Search')

@bp.route('/purchaseHistory', methods = ["GET", "POST"])
def purchaseHistory():
    uid = current_user.uid
    purchases = Purchase.get_all_by_uid(uid)
    form = purchaseHistoryForm()
    search_key = form.search_key.data
    if form.myField1.data == 'None':
        purchases = Purchase.get_all_by_uid_search(uid,search_key)
    if form.myField1.data == 'Price Ascend':
        purchases = Purchase.get_all_by_uid_price_asc(uid,search_key) 
    if form.myField1.data == 'Price Descend':
        purchases = Purchase.get_all_by_uid_price_desc(uid,search_key) 
    if form.myField1.data == 'Most Recent':
        purchases = Purchase.get_all_by_uid_most_recent(uid,search_key)
    return render_template('purchaseHistory.html',
                           purchase_history=purchases, form = form)

@bp.route('/seeUser', methods = ["GET", "POST"])
def seeUser():
    uid = request.args.get('uid')
    user = User.getUser(uid)
    rating = Seller_Review.get_average_seller_product_rating(uid)
    rating = str(rating)[11:-5]
    if rating == '':
        rating = 0.0
    rating = float(rating)
    reviews = Seller_Review.getAllUserReview(uid)
    reviews2 = Product_Review.getAllUserReview(uid)
    seller = Seller.checkSeller(uid)
    return render_template('userPage.html', uid = user, avail_reviews = reviews2, avail_reviews2 = reviews, seller = seller, rating=rating)

