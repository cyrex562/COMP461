################################################################################
##
# @file views.py
# @brief flask web app main script file for Janes Voyages Web App (JVAP)
# @author Josh Madden <cyrex562@gmail.com>
# copyright Josh Madden 2014
################################################################################
################################################################################
# IMPORTS
################################################################################
import uuid
from flask import jsonify, render_template, request, session, redirect, url_for

from app import app
import models
import model_ops


################################################################################
# GLOBAL
################################################################################
################################################################################
# FUNCTIONS
################################################################################
#######################################
##
# @brief set the session id
#######################################
def set_session_id(in_session):
    if 'session_id' in in_session:
        result = in_session['session_id']
    else:
        result = uuid.uuid4().hex
        in_session['session_id'] = result
    return result


#######################################
##
# @brief handle a general server request
#######################################
@app.route('/server_request', methods=['POST'])
def handle_server_request():
    result_msg = 'success'
    result_data = 'no data'
    session_id = set_session_id(session)
    request_obj = request.get_json()
    request_obj['session_id'] = session_id
    return jsonify(message=result_msg, data=result_data)


#######################################
##
# @brief get a list of voyages
#######################################
@app.route('/get_voyages', methods=['POST'])
def retrieve_voyages_list():
    result_msg = 'success'
    voyage_query = model_ops.get_all_voyages()
    voyages = []
    for v in voyage_query:
        waypoints = []
        for w in v.waypoints:
            trades = []
            for t in w.trades:
                items = []
                for i in t.items:
                    items.append({'item_id': i.item_id,
                                  'item_description': i.item_description,
                                  'item_quantity': i.item_quantity,
                                  'bought_sold': i.bought_sold})
                trades.append({'trade_id': t.trade_id,
                               'trade_name': t.trade_name,
                               'trade_notes': t.trade_notes,
                               'items': items})
            waypoints.append({'waypoint_id': w.waypoint_id,
                              'waypoint_name': w.waypoint_name,
                              'waypoint_type': w.waypoint_type,
                              'waypoint_location': w.waypoint_location,
                              'waypoint_notes': w.waypoint_notes,
                              'start_date': w.start_date,
                              'end_date': w.end_date,
                              'trades': trades})
        voyages.append({'voyage_id': v.voyage_id,
                        'voyage_name': v.voyage_name,
                        'voyage_notes': v.voyage_notes,
                        'waypoints': waypoints})
    return jsonify(message=result_msg, data={'voyages': voyages})


#######################################
##
# @brief get a list of ships
#######################################
@app.route('/get_ships', methods=['POST'])
def retreive_ships():
    result_msg = 'success'
    ships_query = model_ops.get_all_ships()
    ships = []
    for s in ships_query:
        ships.append({'ship_id': s.ship_id,
                      'ship_name': s.ship_name,
                      'ship_captain': s.ship_captain,
                      'ship_flag': s.ship_flag,
                      'ship_voyage_id': s.ship_voyage_id,
                      'ship_notes': s.ship_notes})
    return jsonify(message=result_msg, data={'ships': ships})


#######################################
##
# @brief get a list of waypoints
#######################################
@app.route('/get_waypoints', methods=['POST'])
def retrieve_waypoints():
    result_msg = 'success'
    waypoints_query = model_ops.get_all_waypoints()
    waypoints = []
    for w in waypoints_query:
        waypoints.append({
            'waypoint_id': w.waypoint_id,
            'waypoint_name': w.waypoint_name,
            'waypoint_type': w.waypoint_type,
            'waypoint_location': w.waypoint_location,
            'start_date': w.start_date,
            'end_date': w.end_date,
            'waypoint_notes': w.waypoint_notes,
            'waypoint_voyage_id': w.waypoint_voyage_id
        })
    return jsonify(message=result_msg, data={'waypoints': waypoints})

# TODO: create a method to get a list of trades
# TODO: create a method to get a list of items


#######################################
##
# @brief create a new voyage row
#######################################
@app.route('/create_voyage', methods=['POST'])
def create_voyage():
    request_json = request.get_json()
    print "request_obj: {0}".format(request_json)
    json_params = request_json['params']
    voyage = models.Voyage(voyage_name=json_params['new_voyage_name'],
                           voyage_notes=json_params['new_voyage_notes'])
    model_ops.add_voyage(voyage)
    return jsonify(message="success", data="")


#######################################
##
# @brief create a new ship row
#######################################
@app.route('/create_ship', methods=['POST'])
def create_ship():
    request_json = request.get_json()
    print "request obj {0}".format(request_json)
    json_params = request_json['params']
    ship = models.Ship(ship_name=json_params['ship_name'],
                       ship_captain=json_params['ship_captain'],
                       ship_flag=json_params['ship_flag'],
                       ship_notes=json_params['ship_notes'])
    model_ops.add_ship(ship)
    response = jsonify(message="succes", data="")
    return response


#######################################
##
# @brief create a new waypoint row
#######################################
@app.route('/create_waypoint', methods=['POST'])
def create_waypoint():
    request_json = request.get_json()
    print "request obj {0}".format(request_json)
    json_params = request_json['params']
    waypoint = models.Waypoint(waypoint_name=json_params['waypoint_name'],
                               waypoint_type=json_params['waypoint_type'],
                               waypoint_location=json_params[
                                   'waypoint_location'],
                               waypoint_notes=json_params['waypoint_notes'],
                               start_date=json_params['waypoint_start_date'],
                               end_date=json_params['waypoint_end_date'])
    model_ops.add_waypoint(waypoint)
    return jsonify(message="success", data="")


#######################################
##
# @brief update a voyage
#######################################
@app.route('/update_voyage', methods=['POST'])
def update_voyage():
    request_json = request.get_json()
    json_params = request_json['params']
    voyage = models.Voyage(voyage_id=json_params['updated_voyage_id'],
                           voyage_name=json_params['updated_voyage_name'],
                           voyage_notes=json_params['updated_voyage_notes'])
    model_ops.update_voyage(voyage)
    response = jsonify(message="success", data="")
    return response


#######################################
##
# @brief update a ship
#######################################
@app.route('/update_ship', methods=['POST'])
def update_ship():
    request_json = request.get_json()
    json_params = request_json['params']
    ship = models.Ship(ship_id=json_params['updated_ship_id'],
                       ship_name=json_params['updated_ship_name'],
                       ship_captain=json_params['updated_ship_captain'],
                       ship_flag=json_params['updated_ship_flag'],
                       ship_notes=json_params['updated_ship_notes'])
    model_ops.update_ship(ship)
    return jsonify(message="success", data="")


#######################################
##
# @brief update a waypoint
#######################################
@app.route('/update_waypoint', methods=['POST'])
def update_waypoint():
    request_json = request.get_json()
    json_params = request_json['params']
    waypoint = models.Waypoint(waypoint_id=json_params['updated_waypoint_id'],
        waypoint_name=json_params['updated_waypoint_name'],
        waypoint_type=json_params['updated_waypoint_type'],
        waypoint_location=json_params['updated_waypoint_location'],
        waypoint_notes=json_params['updated_waypoint_notes'],
        start_date=json_params['updated_waypoint_start_date'],
        end_date=json_params['updated_waypoint_end_date'])
    model_ops.update_waypoint(waypoint)
    return jsonify(message="success", data='')

# TODO: write method to handle updating trades
# TODO: write method to handle updating items


#######################################
##
# @brief delete voyages by id
#######################################
@app.route('/delete_voyages_by_id', methods=['POST'])
def delete_voyages_by_id():
    request_json = request.get_json()
    json_params = request_json['params']
    voyages_to_delete_ids = json_params['voyages_to_delete_ids']
    model_ops.delete_voyages_by_id(voyages_to_delete_ids)
    return jsonify(message="success", data='')


#######################################
##
# @brief delete ships by id
#######################################
@app.route('/delete_ships_by_id', methods=['POST'])
def delete_ships_by_id():
    request_json = request.get_json()
    json_params = request_json['params']
    ships_to_delete_ids = json_params['ships_to_delete_ids']
    model_ops.delete_ships_by_id(ships_to_delete_ids)
    return jsonify(message="success", data="")


#######################################
##
# @brief delete waypoints by id
#######################################
@app.route('/delete_waypoints_by_id', methods=['POST'])
def delete_waypoints_by_id():
    json_params = request.get_json()['params']
    waypoints_to_delete_ids = json_params['waypoints_to_delete_ids']
    model_ops.delete_waypoints_by_id(waypoints_to_delete_ids)
    return jsonify(message="succes", data="")

# TODO: write method to handle deleting trades
# TODO: write method to handle deleting items


#######################################
##
# @brief create a new voyage row
#######################################
@app.route('/get_all_voyage_ids', methods=['POST'])
def get_all_voyage_ids():
    voyage_ids = model_ops.get_all_voyage_ids()
    return jsonify(message="success", data={'voyage_ids': voyage_ids})


#######################################
##
# @brief get all ship ids
#######################################
@app.route('/get_all_ship_ids', methods=['POST'])
def get_all_ship_ids():
    ship_ids = model_ops.get_all_ship_ids()
    return jsonify(message="succes", data={'ship_ids': ship_ids})


#######################################
##
# @brief get all waypoint ids
#######################################
@app.route('/get_all_waypoint_ids', methods=['POST'])
def get_all_waypoint_ids():
    waypoint_ids = model_ops.get_all_waypoint_ids()
    return jsonify(message="success", data={'waypoint_ids': waypoint_ids})

# TODO: write method to handle retrieving all trade ids
# TODO: write method to handle retireiving all item ids


#######################################
##
# @brief route handler for voyages page
#######################################
@app.route('/voyages')
def route_voyages():
    return render_template('voyages.html')


#######################################
##
# @brief route handler for ships page
#######################################
@app.route('/ships')
def route_ships():
    return render_template('ships.html')


#######################################
##
# @brief route handler for ships page
#######################################
@app.route('/waypoints')
def route_waypoints():
    return render_template('waypoints.html')


#######################################
##
# @brief default route handler
#######################################
@app.route('/')
def route_default():
    return redirect(url_for('route_voyages'))

################################################################################
# END OF FILE
################################################################################