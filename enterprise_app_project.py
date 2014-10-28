"""
@file enterprise_app_project.py
@brief main source file for web app
@author Josh Madden <madden07@email.franklin.edu>
@license MIT license
"""
################################################################################
# IMPORTS
################################################################################
import os
import datetime
from flask import Flask, url_for, redirect, request, render_template

################################################################################
# DEFINES
################################################################################
from flask.ext.login import LoginManager, AnonymousUserMixin, UserMixin, \
    login_required
from flask.ext.sqlalchemy import SQLAlchemy
from config import SECRET_KEY


class AnonymousUser(AnonymousUserMixin):
    def is_admin(self):
        return False

    def is_eng_admin(self):
        return False

    def is_user(self):
        return False


class User(UserMixin):
    def __init__(self):
        self.username = ''
        self.auth_token = ''
        self.session_id = ''
        self.is_auth = False
        self.is_anon = False
        self.login_time = datetime.now()

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.session_id)

    def is_authenticated(self):
        return self.is_auth

    def is_user(self):
        return True

    def is_admin(self):
        return True


app = Flask(__name__)
app.debug = True
app.secret_key = SECRET_KEY
login_manager = LoginManager()
login_manager.anonymous_user = AnonymousUser
login_manager.login_view = 'login'
login_manager.init_app(app)
db = SQLAlchemy(app)

################################################################################
# FUNCTIONS
################################################################################
def pop_user(username='', user_id=''):
    print 'not implemented'


@login_manager.user_loader
def load_user(user_id):
    user_result = None
    print 'not implemented'
    return user_result


@app.route('/')
def default_page_controller():
    """
    page controller for default application route
    :return:
    """
    return redirect(url_for('catalog_page_controller'))


@app.route('/catalog', methods=['GET', 'POST'])
def catalog_page_controller():
    """
    catalog view page controller
    :return:
    """
    template_values = {}
    if request.method == 'GET':
        return render_template('catalog.html', **template_values)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account_page_controller():
    """
    account view page controller
    :return:
    """
    template_values = {}
    if request.method == 'GET':
        return render_template('account.html', **template_values)


@app.route('/cart', methods=['GET', 'POST'])
def cart_page_controller():
    """
    shopping cart page controller
    :return:
    """
    template_values = {}
    if request.method == 'GET':
        return render_template('cart.html', **template_values)


@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout_page_controller():
    """
    checkout view page controller
    :return:
    """
    template_values = {}
    if request.method == 'GET':
        return render_template('checkout.html', **template_values)


@app.route('/item_details', methods=['GET', 'POST'])
def item_details_page_controller():
    """
    item details view page controller
    :return:
    """
    template_values = {}
    if request.method == 'GET':
        return render_template('item_details.html', **template_values)


@app.route('/landing', methods=['GET'])
def landing_page_controller():
    """
    landing view page controller
    :return:
    """
    template_values = {}
    return render_template('landing.html', **template_values)


@app.route('/order_details', methods=['GET', 'POST'])
@login_required
def order_details_page_controller():
    """
    order details page controller
    :return:
    """
    template_values = {}
    if request.method == 'GET':
        return render_template('order_details.html', **template_values)


@app.route('/register', methods=['GET', 'POST'])
def register_page_controller():
    """
    register view page controller
    :return:
    """
    template_values = {}
    if request.method == 'GET':
        return render_template('register.html', **template_values)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password_page_controller():
    """
    reset password view page controller
    :return:
    """
    template_values = {}
    if request.method == 'GET':
        return render_template('reset_password.html', **template_values)


@app.route('/login', methods=['GET', 'POST'])
def login_page_controller():
    """
    login view page controller
    :return:
    """
    template_values = {}
    if request.method == 'GET':
        return render_template('login.html', **template_values)


################################################################################
# ENTRY POINT
################################################################################
if __name__ == '__main__':
    app.run()

################################################################################
# END OF FILE
################################################################################
