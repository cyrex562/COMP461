"""
@file enterprise_app_project.py
@brief main source file for web app
@author Josh Madden <madden07@email.franklin.edu>
@license MIT license
"""
################################################################################
# IMPORTS
################################################################################
import atexit
from flask import Flask, url_for, redirect, request, render_template
from flask.ext.login import LoginManager, login_required, login_user, \
    logout_user, current_user
import signal
from config import SECRET_KEY
from data_gateway import load_data_handlers, table_names, store_data, \
    init_data_gateway, load_data, store_data_handlers
from model_ops import get_user_by_id, user_data_loader, get_user_by_username, \
    customer_data_loader, user_data_storage_handler, \
    customer_data_storage_handler

################################################################################
# DEFINES
################################################################################
# * app initialization
from controller_ops import register_user

app = Flask(__name__)
app.debug = True
app.secret_key = SECRET_KEY
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# * model initialization
# ** configure loaders for the data loader
load_data_handlers.append(user_data_loader)
load_data_handlers.append(customer_data_loader)

# ** configure table names
table_names.append('users')
table_names.append('customers')

# ** configure storage handlers
store_data_handlers.append(user_data_storage_handler)
store_data_handlers.append(customer_data_storage_handler)

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
    template_values = {
        'current_user': current_user,
        'page': page_name
    }
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
    if request.method == 'GET':
        return render_template('account.html', **template_values)


@app.route('/cart', methods=['GET', 'POST'])
def cart_page_controller():
    """
    shopping cart page controller
    :return:
    """
    template_values = get_template_values('cart')
    if request.method == 'GET':
        return render_template('cart.html', **template_values)


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


@app.route('/item_details', methods=['GET', 'POST'])
def item_details_page_controller():
    """
    item details view page controller
    :return:
    """
    template_values = get_template_values('item_details')
    if request.method == 'GET':
        return render_template('item_details.html', **template_values)


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
