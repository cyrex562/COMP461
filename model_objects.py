"""
@file models.py
@brief data model objects definition
@author Josh Madden
@copyright Fifth Column Group 2014
"""
from flask.ext.login import UserMixin

import datetime


class Cart():
    """
    Shopping Cart object
    """
    def __init__(self):
        self.items = []
        self.total = 0.0


class CartItem():
    """
    An item in the shopping cart
    """

    def __init__(self):
        self.app_id = 0
        self.app = None
        self.quantity = 0
        self.subtotal = 0.0


class Customer():
    """
    A customer
    """
    def __init__(self):
        self.id = '0'
        self.user_id = '0'
        self.billing_address = ''
        self.shipping_address = ''
        self.email_address = ''
        self.person_name = ''
        self.rating = '0'


class User(UserMixin):
    """
    User Account
    """
    def __init__(self):
        self.username = ''
        self.id = ''
        self.login_time = datetime.datetime.now()
        self.password = ''
        self.pass_hash = ''
        self.salt = ''
        self.user_type = 'user'

    def is_active(self):
        """
        return if its active
        """
        return True

    def get_id(self):
        """
        Get the account ID
        """
        return unicode(self.id)

    def is_authenticated(self):
        """
        Return if authenticated
        """
        return True

    def __repr__(self):
        return 'User, username: {0}, '


class App(object):
    """
    Product
    """
    def __init__(self):
        self.id = 0
        self.app_name = ""
        self.download_link = ""
        self.platform = ""
        self.platform_requirements = {}
        self.app_publisher = ""
        self.app_description = ""
        self.license_count = ""
        self.app_image = ""
        self.price = 0


class Order(object):
    """
    Customer order
    """
    def __init__(self):
        self.id = 0
        self.items = []
        self.handling_fee = 0.0
        self.tax_amount = 0.0
        self.total_cost = 0.0
        self.subtotal = 0.0
        self.customer_id = 0
        self.shipping_address = ''
        self.billing_address = ''
