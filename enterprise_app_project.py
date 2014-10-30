"""
@file enterprise_app_project.py
@brief main source file for web app
@author Josh Madden <madden07@email.franklin.edu>
@license MIT license
"""
import atexit
import os
import pickle
from uuid import uuid4
from datetime import timedelta
from flask import Flask, url_for, redirect, request, render_template, session
from flask.ext.login import LoginManager, login_required, login_user, \
    logout_user, current_user
import signal
from flask.sessions import SessionMixin, SessionInterface
import jsonpickle
from redis import Redis
from werkzeug.datastructures import CallbackDict
import data_gateway
from model_objects import Customer, Cart, CartItem
from model_ops import get_user_by_id, get_user_by_username, \
    get_customer_by_username, get_all_apps, get_app_by_id, \
    get_apps_for_cart_items, update_item_subtotals, update_cart_total, \
    register_user, adjust_inventory
import model_ops
from model_xml import user_data_loader, customer_data_loader, app_data_loader, \
    order_data_loader, \
    load_data_handlers, store_data_handlers, load_data
from model_persistence import user_data_storage_handler, \
    customer_data_storage_handler, app_data_storage_handler, \
    order_data_storage_handler
import model_xml


class RedisSession(CallbackDict, SessionMixin):
    """
    Redis Session object
    """
    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True

        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False


class RedisSessionInterface(SessionInterface):
    """
    Redis Session Interface Object
    """
    serializer = pickle
    session_class = RedisSession

    def __init__(self, redis=None, prefix='session:'):
        if redis is None:
            redis = Redis()
        self.redis = redis
        self.prefix = prefix

    @staticmethod
    def generate_sid():
        """
        Generate the SID
        """
        return str(uuid4())

    @staticmethod
    def get_redis_expiration_time(in_app, in_session):
        """
        Get the expiration time from redis
        """
        if in_session.permanent:
            return in_app.permanent_session_lifetime
        return timedelta(days=1)

    def open_session(self, in_app, in_request):
        """
        Open a session
        """
        sid = in_request.cookies.get(in_app.session_cookie_name)
        if not sid:
            sid = self.generate_sid()
            return self.session_class(sid=sid, new=True)
        val = self.redis.get(self.prefix + sid)
        if val is not None:
            data = self.serializer.loads(val)
            return self.session_class(data, sid=sid)
        return self.session_class(sid=sid, new=True)

    def save_session(self, in_app, in_session, response):
        """
        Save a session
        """
        domain = self.get_cookie_domain(in_app)
        if not in_session:
            self.redis.delete(self.prefix + in_session.sid)
            if in_session.modified:
                response.delete_cookie(in_app.session_cookie_name,
                                       domain=domain)
            return
        redis_exp = self.get_redis_expiration_time(in_app, in_session)
        cookie_exp = self.get_expiration_time(in_app, in_session)
        val = self.serializer.dumps(dict(in_session))
        self.redis.setex(self.prefix + in_session.sid, val,
                         int(redis_exp.total_seconds()))
        response.set_cookie(in_app.session_cookie_name, in_session.sid,
                            expires=cookie_exp, httponly=True, domain=domain)

# * app initialization
app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)
app.session_interface = RedisSessionInterface()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# * model initialization
# ** configure loaders for the data loader
load_data_handlers.append(user_data_loader)
load_data_handlers.append(customer_data_loader)
load_data_handlers.append(app_data_loader)
load_data_handlers.append(order_data_loader)

# ** configure table names
data_gateway.table_names.append('users')
data_gateway.table_names.append('customers')
data_gateway.table_names.append('apps')
data_gateway.table_names.append('orders')

# ** configure storage handlers
store_data_handlers.append(user_data_storage_handler)
store_data_handlers.append(customer_data_storage_handler)
store_data_handlers.append(app_data_storage_handler)
store_data_handlers.append(order_data_storage_handler)

# ** run tdg initializer
data_gateway.init_data_gateway()
load_data()


@login_manager.user_loader
def load_user(user_id):
    """
    Load a user
    :param user_id:
    :return:
    """
    user_result = get_user_by_id(user_id)
    return user_result


def get_template_values(page_name):
    """
    Get the template values to populate pages with.
    :param page_name:
    :return:
    """
    template_values = {'current_user': current_user, 'page': page_name}
    return template_values


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
    template_values = get_template_values('catalog')
    template_values['apps'] = get_all_apps()
    app.logger.debug('current_user, is_auth" {0}, is_anonymous: {1}'.format(
        current_user.is_authenticated(), current_user.is_anonymous()))
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        pass
    return render_template('catalog.html', **template_values)


@app.route('/account', methods=['GET'])
@login_required
def account_page_controller():
    """
    account view page controller
    :return:
    """
    template_values = get_template_values('account')
    if current_user.user_type == 'admin':
        customer = Customer()
    else:
        customer = get_customer_by_username(current_user.username)
    template_values['person_name'] = customer.person_name
    template_values['billing_address'] = customer.billing_address
    template_values['shipping_address'] = customer.shipping_address
    template_values['email'] = customer.email_address
    template_values['rating'] = customer.rating
    template_values['username'] = current_user.username
    template_values['orders'] = model_ops.get_orders_by_customer_id(customer.id)

    return render_template('account.html', **template_values)


@app.route('/app', methods=['POST'])
def get_app_details():
    """

    :return:
    """
    app_id = int(request.json['app_id'])
    sel_app = get_app_by_id(app_id)
    return jsonpickle.encode({'message': 'success', 'data': {'app': sel_app}},
                             unpicklable=False)


@app.route('/landing', methods=['GET'])
def landing_page_controller():
    """
    landing view page controller
    :return:
    """
    template_values = get_template_values('landing')
    return render_template('landing.html', **template_values)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = Cart()
    cart_item = CartItem()
    cart_item.quantity = int(request.json['quantity'])
    cart_item.app_id = int(request.json['app_id'])
    session['cart'].items.append(cart_item)
    session.modified = True
    total_cart_items = 0
    for item in session['cart'].items:
        total_cart_items += item.quantity
    return jsonpickle.encode(
        {'message': 'success', 'data': {'total_cart_items': total_cart_items}})


@app.route('/change_cart_item_quantity', methods=['POST'])
def change_cart_item_quantity():
    if 'cart' not in session:
        session['cart'] = Cart()
    cart = session['cart']
    cart = \
        model_ops.change_cart_item_quantity(cart,
                                            int(request.json['app_id']),
                                            int(request.json['new_quantity']))
    cart = update_item_subtotals(cart)
    cart = update_cart_total(cart)
    session['cart'] = cart
    session.modified = True
    response = {'message': 'success',
                'data': {'cart': cart, 'app_id': request.json['app_id']}}
    return jsonpickle.encode(response)


@app.route('/change_checkout_item_quantity', methods=['POST'])
@login_required
def change_order_item_quantity():
    if 'cart' not in session:
        session['cart'] = Cart()
    cart = session['cart']
    cart = \
        model_ops.change_cart_item_quantity(cart,
                                            int(request.json['app_id']),
                                            int(request.json['new_quantity']))
    cart = update_item_subtotals(cart)
    cart = update_cart_total(cart)
    session.modified = True
    customer = get_customer_by_username(current_user.username)
    handling_fee = model_ops.get_handling_fee(cart)
    tax = model_ops.calc_order_tax(cart, handling_fee)
    order_total = model_ops.calc_order_total(cart, tax, handling_fee)
    result = {'message': 'success',
              'data': {
                  'customer': customer,
                  'cart': cart,
                  'handling_fee': handling_fee,
                  'order_total': order_total,
                  'tax': tax,
                  'app_id': request.json['app_id']}}
    return jsonpickle.encode(result, unpicklable=False)


@app.route('/remove_item_from_cart', methods=['POST'])
def remove_item_from_cart():
    if 'cart' not in session:
        session['cart'] = Cart()
    cart = session['cart']
    cart = model_ops.remove_item_from_cart(cart, int(request.json['app_id']))
    cart = update_item_subtotals(cart)
    cart = update_cart_total(cart)
    session['cart'] = cart
    session.modified = True
    result = {'message': 'success',
              'data': {
                  'cart': cart,
                  'app_id': request.json['app_id']}}
    return jsonpickle.encode(result)


@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    if 'cart' not in session:
        session['cart'] = Cart()
    cart = session['cart']
    cart = model_ops.clear_cart(cart)
    cart = update_item_subtotals(cart)
    cart = update_cart_total(cart)
    session['cart'] = cart
    session.modified = True
    result = {'message': 'success', 'data': {'cart': cart}}
    return jsonpickle.encode(result)


@app.route('/remove_item_from_checkout', methods=['POST'])
@login_required
def remove_item_from_checkout():
    if 'cart' not in session:
        session['cart'] = Cart()
    cart = session['cart']
    cart = model_ops.remove_item_from_cart(cart, int(request.json['app_id']))
    cart = update_item_subtotals(cart)
    cart = update_cart_total(cart)
    session['cart'] = cart
    session.modified = True
    customer = get_customer_by_username(current_user.username)
    handling_fee = model_ops.get_handling_fee(cart)
    tax = model_ops.calc_order_tax(cart, handling_fee)
    order_total = model_ops.calc_order_total(cart, tax, handling_fee)
    result = {'message': 'success',
              'data': {
                  'customer': customer,
                  'cart': cart,
                  'handling_fee': handling_fee,
                  'order_total': order_total,
                  'tax': tax,
                  'app_id': request.json['app_id']}}
    return jsonpickle.encode(result, unpicklable=False)


@app.route('/cart_items_count', methods=['POST'])
def get_cart_items_count():
    if 'cart' not in session:
        session['cart'] = Cart()
    total_cart_items = 0
    for item in session['cart'].items:
        total_cart_items += item.quantity
    return jsonpickle.encode(
        {'message': 'success', 'data': {'total_cart_items': total_cart_items}})


@app.route('/cart', methods=['POST'])
def get_cart():
    if 'cart' not in session:
        session['cart'] = Cart()
    cart = session['cart']
    cart = get_apps_for_cart_items(cart)
    cart = update_item_subtotals(cart)
    cart = update_cart_total(cart)
    return jsonpickle.encode({'message': 'success', 'data': {'cart': cart}},
                             unpicklable=False)


@app.route('/get_checkout_data', methods=['POST'])
@login_required
def get_checkout_data():
    if 'cart' not in session:
        session['cart'] = Cart()
    cart = session['cart']
    customer = get_customer_by_username(current_user.username)
    handling_fee = model_ops.get_handling_fee(cart)
    tax = model_ops.calc_order_tax(cart, handling_fee)
    order_total = model_ops.calc_order_total(cart, tax, handling_fee)
    result = {'message': 'success', 'data': {'customer': customer, 'cart': cart,
                                             'handling_fee': handling_fee,
                                             'order_total': order_total,
                                             'tax': tax}}
    return jsonpickle.encode(result, unpicklable=False)


@app.route('/place_order', methods=['POST'])
@login_required
def place_order():
    if 'cart' not in session:
        session['cart'] = Cart()
    cart = session['cart']
    customer = get_customer_by_username(current_user.username)
    handling_fee = model_ops.get_handling_fee(cart)
    tax = model_ops.calc_order_tax(cart, handling_fee)
    order_total = model_ops.calc_order_total(cart, tax, handling_fee)
    stock_result = model_ops.check_stock(cart)
    billing_address = request.json['billing_address']
    shipping_address = request.json['shipping_address']
    if len(stock_result) > 0:
        result = {'message': 'failure, invalid app quantity', 'data': {
            'invalid_items': stock_result}}
    else:
        order = model_ops.place_order(customer, cart, handling_fee, tax,
                    order_total, shipping_address, billing_address)
        adjust_inventory(cart)
        result = {'message': 'success', 'data': {'order': order, 'customer':
            customer, 'cart': cart}}
        cart = model_ops.clear_cart(cart)
        session['cart'] = cart
        session.modified = True

    return jsonpickle.encode(result, unpicklable=False)


@app.route('/register', methods=['GET', 'POST'])
def register_page_controller():
    """
    register view page controller
    :return:
    """
    template_values = get_template_values('register')
    if request.method == 'GET':
        return render_template('register.html', **template_values)
    elif request.method == 'POST':
        success = register_user(request)
        if success:
            # TODO: redirect user to catalog page and prompt them to log in
            return redirect(url_for('catalog_page_controller'))
        else:
            # TODO: indicate an error occurred
            return render_template('register.html', **template_values)


@app.route('/reset_password', methods=['POST'])
def reset_password_page_controller():
    """
    reset password view page controller
    :return:
    """
    pass


@app.route('/login', methods=['GET', 'POST'])
def login_page_controller():
    """
    login view page controller
    :return:
    """
    template_values = get_template_values('login')
    if request.method == 'GET':
        return render_template('login.html', **template_values)
    elif request.method == 'POST':
        if request.form['submit'] == 'login':
            # TODO use hash and salt
            username_try = request.form['username']
            password_try = request.form['password']

            matching_user = get_user_by_username(username_try)
            if matching_user is not None:
                if password_try == matching_user.password:
                    success = login_user(matching_user)
                    if not success:
                        app.logger.error('login_page_controller, failed to '
                                         'login user')
                        return render_template('login.html', **template_values)
                    else:
                        app.logger.debug('login_page_controller, login success')
                        return redirect(url_for('catalog_page_controller'))
                else:
                    app.logger.warn('login_page_controller, password did not '
                                    'match')
                    return render_template('login.html', **template_values)
                    # TODO: handle non-matching password
            else:
                return render_template('login.html', **template_values)
                # TODO: handle non-matching user

        elif request.form['submit'] == 'register':
            return redirect(url_for('register_page_controller'))


@app.route('/logout', methods=['GET', 'POST'])
def logout_page_controller():
    """
    logout page controller
    :return: void
    """
    logout_user()
    return redirect(url_for('catalog_page_controller'))


@app.route('/user_logged_in', methods=['POST'])
def user_logged_in():
    is_user_logged_in = 0
    if current_user.is_authenticated():
        is_user_logged_in = 1
    result = {'message': 'success',
              'data': {'user_logged_in': is_user_logged_in}}
    return jsonpickle.encode(result)


def exit_handler():
    """
    a program exit handler to facilitate cleanup and persisting data to the
    xml object store
    :return:
    """
    model_xml.store_data()


def sigterm_handler(signum, frame):
    del signum
    del frame
    model_xml.store_data()


if __name__ == '__main__':
    atexit.register(exit_handler)
    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGINT, sigterm_handler)
    app.run()