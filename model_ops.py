################################################################################
# @file model_ops.py
# @brief data model operations
# @author Josh Madden
# @copyright Fifth Column Group 2014
################################################################################
################################################################################
# IMPORTS
################################################################################
from app import db, models


################################################################################
# DEFINES
################################################################################


################################################################################
# CLASSES
################################################################################


################################################################################
# GLOBALS
################################################################################


################################################################################
# FUNCTIONS
################################################################################
def add_voyage(voyage):
    db.session.add(voyage)
    db.session.commit()


def add_ship(ship):
    db.session.add(ship)
    db.session.commit()


def add_waypoint(waypoint):
    db.session.add(waypoint)
    db.session.commit()


def add_trade(trade):
    db.session.add(trade)
    db.session.commit()


def add_item(item):
    db.session.add(item)
    db.session.commit()


def update_voyage(in_voyage):
    voyage = models.Voyage.query.filter_by(voyage_id=in_voyage.voyage_id)\
        .first()
    voyage.voyage_name = in_voyage.voyage_name
    voyage.voyage_notes = in_voyage.voyage_notes
    db.session.commit()


def update_ship(in_ship):
    ship = models.Ship.query.filter_by(ship_id=in_ship.ship_id).first()
    ship.ship_name = in_ship.ship_name
    ship.ship_captain = in_ship.ship_captain
    ship.ship_flag = in_ship.ship_flag
    ship.ship_notes = in_ship.ship_notes
    db.session.commit()


def update_waypoint(in_waypoint):
    waypoint = models.Waypoint.query.filter_by(
        waypoint_id=in_waypoint.waypoint_id).first()
    waypoint.waypoint_name = in_waypoint.waypoint_name
    waypoint.waypoint_type = in_waypoint.waypoint_type
    waypoint.waypoint_location = in_waypoint.waypoint_location
    waypoint.waypoint_notes = in_waypoint.waypoint_notes
    waypoint.start_date = in_waypoint.start_date
    waypoint.end_date = in_waypoint.end_date
    db.session.commit()


# FIXME: update this method
def update_item(item):
    db.session.add(item)
    db.session.commit()


# FIXME: update this method
def update_trade(trade):
    db.session.add(trade)
    db.session.commit()


def delete_voyage(voyage):
    db.session.delete(voyage)
    db.session.commit()


def delete_ship(ship):
    db.session.delete(ship)
    db.session.commit()


def delete_waypoint(waypoint):
    db.session.delete(waypoint)
    db.session.commit()


def delete_trade(trade):
    db.session.delete(trade)
    db.session.commit()


def delete_item(item):
    db.session.delete(item)
    db.session.commit()


def delete_voyages_by_id(voyage_ids):
    for v in voyage_ids:
        voyage = models.Voyage.query.filter_by(voyage_id=v).first()
        db.session.delete(voyage)
    db.session.commit()


def delete_ships_by_id(ship_ids):
    for s in ship_ids:
        ship = models.Ship.query.filter_by(ship_id=s).first()
        db.session.delete(ship)
    db.session.commit()


def delete_waypoints_by_id(waypoint_ids):
    for w in waypoint_ids:
        waypoint = models.Waypoint.query.filter_by(waypoint_id=w).first()
        db.session.delete(waypoint)
    db.session.commit()


# TODO: create delete trade by id method
# TODO: create delete item by id method


def get_all_voyages():
    return models.Voyage.query.all()


def get_all_ships():
    return db.session.query(models.Ship)


def get_all_waypoints():
    return db.session.query(models.Waypoint)


def get_all_trades():
    return db.session.query(models.Trade)


def get_all_items():
    return db.session.query(models.Item)


def get_all_voyage_ids():
    voyages = models.Voyage.query.all()
    result = []
    for v in voyages:
        result.append(v.voyage_id)
    return result


def get_all_ship_ids():
    ships = models.Ship.query.all()
    result = []
    for s in ships:
        result.append(s.ship_id)
    return result


def get_all_waypoint_ids():
    result = []
    for w in models.Waypoint.query.all():
        result.append(w.waypoint_id)
    return result


# TODO: create get_all_trade_ids
# TODO: create get_all_item_ids













































################################################################################
# ENTRY POINT
################################################################################


################################################################################
# END OF FILE
################################################################################