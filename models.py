###############################################################################
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
from app import db
from sqlalchemy.dialects.postgresql import *


################################################################################
# CLASSES
################################################################################
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