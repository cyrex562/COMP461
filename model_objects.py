"""
@file models.py
@brief data model objects definition
@author Josh Madden
@copyright Fifth Column Group 2014
"""
###############################################################################
# IMPORTS
###############################################################################
import datetime
from flask.ext.login import UserMixin, AnonymousUserMixin


################################################################################
# DEFINES
################################################################################
class ShoppingCart():
    """
    Shopping Cart object
    """

    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)


class CartItem():
    """
    An item in the shopping cart
    """

    def __init__(self):
        self.product = None
        self.quantity = 0


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
        return True

    def get_id(self):
        return unicode(self.id)

    def is_authenticated(self):
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


###############################################################################
# END OF FILE
###############################################################################