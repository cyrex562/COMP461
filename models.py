"""
@file models.py
@brief data model objects definition
@author Josh Madden
@copyright Fifth Column Group 2014
"""
###############################################################################
###############################################################################
# IMPORTS
###############################################################################
from sqlalchemy import BLOB
from enterprise_app_project import db
from sqlalchemy.dialects.postgresql import *


################################################################################
# DEFINES
################################################################################
class ShoppingCart(db.Model):
    items = db.relationship('CartItem', lazy='dynamic')

    def add_item(self, item):
        pass

    def remove_item(self, item):
        pass


class CartItem(db.Model):
    product = db.relationship('Product', lazy='dynamic')
    quantity = db.Column(INTEGER)


class Customer(db.Model):
    user_name = db.Column(TEXT)
    pass_hash = db.Column(TEXT)
    pass_salt = db.Column(TEXT)
    billing_address = db.Column(TEXT)
    shipping_address = db.Column(TEXT)
    email_address = db.Column(TEXT)
    person_name = db.Column(TEXT)
    rating = db.Column(TEXT)


class Voyage(db.Model):
    """
    Voyage DL object
    """
    voyage_id = db.Column(INTEGER, primary_key=True)
    voyage_name = db.Column(VARCHAR(255), index=True)
    voyage_notes = db.Column(TEXT)
    waypoints = db.relationship('Waypoint', lazy='dynamic')
    ships = db.relationship('Ship', lazy='dynamic')





class Ship(db.Model):
    """
    Ship DL object
    """
    ship_id = db.Column(INTEGER, primary_key=True)
    ship_name = db.Column(VARCHAR(255), index=True)
    ship_captain = db.Column(VARCHAR(255), index=True)
    ship_flag = db.Column(VARCHAR(255), index=True)
    ship_notes = db.Column(TEXT)
    ship_voyage_id = db.Column(db.Integer, db.ForeignKey('voyage.voyage_id'))


class Waypoint(db.Model):
    """
    Waypoint DL object
    """
    waypoint_id = db.Column(INTEGER, primary_key=True)
    waypoint_name = db.Column(VARCHAR(255), index=True)
    waypoint_type = db.Column(VARCHAR(255), index=True)
    waypoint_location = db.Column(VARCHAR(255), index=True)
    waypoint_notes = db.Column(TEXT)
    start_date = db.Column(TEXT, index=True)
    end_date = db.Column(TEXT, index=True)
    waypoint_voyage_id = db.Column(INTEGER, db.ForeignKey('voyage.voyage_id'))
    trades = db.relationship('Trade', lazy='dynamic')


class Trade(db.Model):
    """
    Trade DL object
    """
    trade_id = db.Column(INTEGER, primary_key=True)
    trade_notes = db.Column(TEXT)
    bought_sold = db.Column(BOOLEAN)
    trade_quantity = db.Column(INTEGER)
    trade_item = db.Column(TEXT)
    trade_waypoint_id = db.Column(db.Integer,
                                  db.ForeignKey('waypoint.waypoint_id'))


waypoint_types = [
    'start',
    'stop',
    'end'
]


trade_items = \
    [
        "male slave",
        "female slave",
        "child slave",
        "guns",
        "cookware",
        "livestock",
        "wild game",
        "fish",
        "seafood",
        "foodstuffs",
        "grain",
        "timber",
        "minerals",
        "metals",
        "tea",
        "coffee",
        "tobacco",
        "cocoa",
        "sugar",
        "spices",
        "alcohol",
        "textiles",
        "medicine",
        "jewelry",
        "furs",
        "leather",
        "paper",
        "manufactured goods",
        "luxury items",
        "dyes",
        "plants",
        "cotton",
        "wool",
        "other"
    ]


###############################################################################
# END OF FILE
###############################################################################