"""
@file enterprise_app_project.py
@brief main source file for web app
@author Josh Madden <madden07@email.franklin.edu>
@license MIT license
"""
# ###############################################################################
# IMPORTS
# ###############################################################################
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
from config import SECRET_KEY
from data_gateway import load_data_handlers, table_names, store_data, \
    init_data_gateway, load_data, store_data_handlers
from model_objects import Customer, Cart, CartItem
from model_ops import get_user_by_id, user_data_loader, get_user_by_username, \
    customer_data_loader, user_data_storage_handler, \
    customer_data_storage_handler, get_customer_by_username, app_data_loader, \
    app_data_storage_handler, get_all_apps, get_app_by_id, \
    get_apps_for_cart_items, update_item_subtotals, update_cart_total
from controller_ops import register_user
# ###############################################################################
# DEFINES
################################################################################
import model_ops


class RedisSession(CallbackDict, SessionMixin):
    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True

        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False


class RedisSessionInterface(SessionInterface):
    serializer = pickle
    session_class = RedisSession

    def __init__(self, redis=None, prefix='session:'):
        if redis is None:
            redis = Redis()
        self.redis = redis
        self.prefix = prefix

    def generate_sid(self):
        return str(uuid4())

    def get_redis_expiration_time(self, app, session):
        if session.permanent:
            return app.permanent_session_lifetime
        return timedelta(days=1)

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = self.generate_sid()
            return self.session_class(sid=sid, new=True)
        val = self.redis.get(self.prefix + sid)
        if val is not None:
            data = self.serializer.loads(val)
            return self.session_class(data, sid=sid)
        return self.session_class(sid=sid, new=True)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            self.redis.delete(self.prefix + session.sid)
            if session.modified:
                response.delete_cookie(app.session_cookie_name, domain=domain)
            return
        redis_exp = self.get_redis_expiration_time(app, session)
        cookie_exp = self.get_expiration_time(app, session)
        val = self.serializer.dumps(dict(session))
        self.redis.setex(self.prefix + session.sid, val,
                         int(redis_exp.total_seconds()))
        response.set_cookie(app.session_cookie_name, session.sid,
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

# ** configure table names
table_names.append('users')
table_names.append('customers')
table_names.append('apps')

# ** configure storage handlers
store_data_handlers.append(user_data_storage_handler)
store_data_handlers.append(customer_data_storage_handler)
store_data_handlers.append(app_data_storage_handler)

# ** run tdg initializer
init_data_gateway()
load_data()


################################################################################
# FUNCTIONS
################################################################################
@login_manager.user_loader
def load_user(user_id):
    user_result = get_user_by_id(user_id)
    return user_result


def get_template_values(page_name):
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


@app.route('/account', methods=['GET', 'POST'])
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

    if request.method == 'GET':
        return render_template('account.html', **template_values)


# @app.route('/cart', methods=['GET', 'POST'])
# def cart_page_controller():
#     """
#     shopping cart page controller
#     :return:
#     """
#     template_values = get_template_values('cart')
#     if request.method == 'GET':
#         return render_template('cart.html', **template_values)


@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout_page_controller():
    """
    checkout view page controller
    :return:
    """
    template_values = get_template_values('checkout')
    if request.method == 'GET':
        return render_template('checkout.html', **template_values)


@app.route('/catalog_action', methods=['GET', 'POST'])
def item_details_page_controller():
    """
    item details view page controller
    :return:
    """
    template_values = get_template_values('item_details')
    if request.method == 'GET':
        return render_template('app_details.html', **template_values)
    elif request.method == 'POST':
        json = request.json
        if request.form['form_action'] == 'add_to_cart':
            cart = session.get('cart', Cart())
            cart_item = CartItem()
            cart_item.quantity = int(request.form['quantity'])
            cart_item.app_id = request.form['app_id']
            cart.items.append(cart_item)
            total_cart_items = 0
            for item in cart.items:
                total_cart_items += item.quantity
            return jsonpickle.encode({'total_cart_items': total_cart_items})
        elif request.form['form_action'] == 'get_app_detils':
            app_id = int(request.form['app_id'])
            sel_app = get_app_by_id(app_id)
            template_values['app'] = sel_app
            return render_template('app_details.html', **template_values)


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


@app.route('/order_details', methods=['GET', 'POST'])
@login_required
def order_details_page_controller():
    """
    order details page controller
    :return:
    """
    template_values = get_template_values('order_details')
    if request.method == 'GET':
        return render_template('order_details.html', **template_values)


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
    cart = model_ops.change_cart_item_quantity(cart,
                                               int(request.json['app_id']), int(
            request.json['new_quantity']))
    cart = update_item_subtotals(cart)
    cart = update_cart_total(cart)
    session['cart'] = cart
    session.modified = True
    return jsonpickle.encode({'message': 'success', 'data': {'cart': cart,
                                                             'app_id':
                                                                 request.json[
                                                                     'app_id']}})


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
    return jsonpickle.encode({'message': 'success',
                              'data': {'cart': cart,
                                       'app_id': request.json['app_id']}})


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


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password_page_controller():
    """
    reset password view page controller
    :return:
    """
    template_values = get_template_values('reset_password')
    if request.method == 'GET':
        return render_template('reset_password.html', **template_values)


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


def exit_handler():
    """
    a program exit handler to facilitate cleanup and persisting data to the
    xml object store
    :return:
    """
    store_data()


def sigterm_handler(signum, frame):
    store_data()


atexit.register(exit_handler)
signal.signal(signal.SIGTERM, sigterm_handler)
signal.signal(signal.SIGINT, sigterm_handler)

################################################################################
# ENTRY POINT
################################################################################
if __name__ == '__main__':
    app.run()

################################################################################
# END OF FILE
################################################################################
