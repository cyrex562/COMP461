"""
@file model_ops.py
@brief data model operations, rules, and logic
@author Josh Madden <cyrex562@gmail.com>
"""
from data_gateway import get_table, add_table_row, set_table
from model_objects import User, Order, Customer
from model_xml import store_data


def get_all_users():
    """
    Get all the users
    :return:
    """
    user_table = get_table('users')
    return user_table


def get_all_customers():
    """
    Get all the customers
    :return:
    """
    customer_table = get_table('customers')
    return customer_table


def get_all_apps():
    """
    Get all the apps
    :return:
    """
    app_table = get_table('apps')
    return app_table


def get_all_orders():
    """
    Get all the orders
    :return:
    """
    order_table = get_table('orders')
    return order_table


def get_user_by_id(in_id):
    """
    Get a user by their ID
    :param in_id:
    :return:
    """
    found_user = None
    users = get_all_users()
    for u in users:
        if u.get_id() == in_id:
            found_user = u
            break

    out_user = None
    if found_user is not None:
        out_user = User()
        out_user.username = found_user.username
        out_user.id = found_user.id
        out_user.login_time = found_user.login_time
        out_user.password = found_user.password
        out_user.pass_hash = found_user.pass_hash
        out_user.salt = found_user.salt

    return out_user


def get_customer_by_user_id(in_user_id):
    """
    Get a customer by their user ID
    :param in_user_id:
    :return:
    """
    found_customer = None
    customers = get_all_customers()
    for c in customers:
        if c.user_id == in_user_id:
            found_customer = c
            break

    return found_customer


def get_app_by_id(in_app_id):
    """
    Get an app by its app ID
    :param in_app_id:
    :return:
    """
    found_app = None
    apps = get_all_apps()
    for a in apps:
        if a.id == in_app_id:
            found_app = a
            break
    return found_app


def get_next_user_id():
    """
    Get the next user ID
    :return:
    """
    users = get_all_users()
    next_user_id = 0
    for u in users:
        if int(u.get_id()) > next_user_id:
            next_user_id = int(u.get_id()) + 1
    return next_user_id


def get_next_customer_id():
    """
    Get the next customer ID
    :return:
    """
    customers = get_all_customers()
    next_customer_id = 0
    for c in customers:
        if int(c.id) > next_customer_id:
            next_customer_id = int(c.id) + 1
    return next_customer_id


def get_next_order_id():
    """
    Get the next order ID
    :return:
    """
    orders = get_all_orders()
    next_order_id = 0
    for o in orders:
        if int(o.id) > next_order_id:
            next_order_id = int(o.id) + 1
    return next_order_id


def get_user_by_username(in_username):
    """
    Get a user by their username
    :param in_username:
    :return:
    """
    found_user = None
    users = get_all_users()
    for u in users:
        if u.username == in_username:
            found_user = u
            break

    out_user = None
    if found_user is not None:
        out_user = User()
        out_user.username = found_user.username
        out_user.id = found_user.id
        out_user.login_time = found_user.login_time
        out_user.password = found_user.password
        out_user.pass_hash = found_user.pass_hash
        out_user.salt = found_user.salt

    return out_user


def get_customer_by_username(username):
    """
    Get a customer by their username
    :param username:
    :return:
    """
    found_customer = None
    user = get_user_by_username(username)
    if user is not None:
        customers = get_all_customers()
        for customer in customers:
            if user.id == customer.user_id:
                found_customer = customer
                break
    return found_customer


def add_user(new_user):
    """
    Add a user to the database
    :param new_user:
    :return:
    """
    add_table_row('users', new_user)


def add_customer(new_customer):
    """
    Add a customer to the database
    :param new_customer:
    :return:
    """
    add_table_row('customers', new_customer)


def add_order(new_order):
    """
    Add a order to the database
    :param new_order:
    :return:
    """
    add_table_row('orders', new_order)


def add_item_to_cart(item, cart):
    """
    Add an item to the cart
    :param item:
    :param cart:
    :return:
    """
    cart.items.append(item)
    return cart


def remove_item_from_cart(cart, app_id):
    """
    Remove an item from the cart
    :param cart:
    :param app_id:
    :return:
    """
    item_to_remove = None
    for item in cart.items:
        if int(item.app_id) == app_id:
            item_to_remove = item
            break
    if item_to_remove is not None:
        cart.items.remove(item_to_remove)
    return cart


def clear_cart(cart):
    """
    Clear the cart
    :param cart:
    :return:
    """
    cart.items = []
    return cart


def get_apps_for_cart_items(cart):
    """
    Get apps for items in the cart
    :param cart:
    :return:
    """
    for item in cart.items:
        if item.app is None:
            app = get_app_by_id(int(item.app_id))
            item.app = app
    return cart


def update_item_subtotals(cart):
    """
    Update item subtotals
    :param cart:
    :return:
    """
    for item in cart.items:
        item.subtotal = round(item.app.price * item.quantity, 2)
    return cart


def update_cart_total(cart):
    """
    UPdate the cart total
    :param cart:
    :return:
    """
    cart.total = 0.0
    for item in cart.items:
        cart.total += item.subtotal
    cart.total = round(cart.total, 2)
    return cart


def change_cart_item_quantity(cart, app_id, new_quantity):
    """
    Change the quantity of the items in the cart
    :param cart:
    :param app_id:
    :param new_quantity:
    :return:
    """
    for item in cart.items:
        if int(item.app_id) == app_id:
            item.quantity = new_quantity
            break
    return cart


def get_handling_fee(cart):
    """
    Get the handling fee
    :param cart:
    :return:
    """
    return round(cart.total * 0.2, 2)


def calc_order_tax(cart, handling_fee):
    """
    Calculate the order tax amount
    :param cart:
    :param handling_fee:
    :return:
    """
    return round((cart.total + handling_fee) * 0.07, 2)


def calc_order_total(cart, tax, handling_fee):
    """
    Calculate the order total
    :param cart:
    :param tax:
    :param handling_fee:
    :return:
    """
    return round(cart.total + tax + handling_fee, 2)


def check_stock(cart):
    """
    Check the availability of an item
    :param cart:
    :return:
    """
    result = []
    for item in cart.items:
        inventory_item = get_app_by_id(item.app_id)
        if item.quantity > inventory_item.license_count:
            result.append({'app_id': item.app_id,
                           'name': inventory_item.app_name,
                           'requested': item.quantity,
                           'available': inventory_item.license_count})
    return result


def place_order(customer, cart, handling_fee, tax, order_total,
                shipping_address, billing_address):
    """
    Process an order
    :param customer:
    :param cart:
    :param handling_fee:
    :param tax:
    :param order_total:
    :param shipping_address:
    :param billing_address:
    :return:
    """
    order = Order()
    order.id = get_next_order_id()
    order.items = cart.items
    order.handling_fee = handling_fee
    order.tax_amount = tax
    order.total_cost = order_total
    order.subtotal = cart.total
    order.customer_id = customer.id
    order.shipping_address = shipping_address
    order.billing_address = billing_address
    add_order(order)
    return order


def update_app_license_count(app, new_license_count):
    """
    Update the license count for the app.
    :param app:
    :param new_license_count:
    :return:
    """
    apps = get_all_apps()
    for i in range(0, len(apps) - 1):
        if str(apps[i].id) == str(app.id):
            apps[i].license_count = new_license_count
    set_table('apps', apps)


def register_user(request):
    """
    Register a user
    :param request:
    :return:
    """
    success = True
    new_user = User()
    new_user.id = unicode(get_next_user_id())
    new_user.username = request.form['username']
    new_user.password = request.form['password']
    add_user(new_user)

    new_customer = Customer()
    new_customer.id = unicode(get_next_customer_id())
    new_customer.user_id = new_user.id
    new_customer.billing_address = request.form['billing_address']
    new_customer.email_address = request.form['email_address']
    new_customer.shipping_address = request.form['shipping_address']
    new_customer.person_name = request.form['person_name']
    add_customer(new_customer)
    store_data()
    return success


def adjust_inventory(cart):
    """
    Adjsut license inventory
    :param cart:
    :return:
    """
    for item in cart.items:
        app = get_app_by_id(item.app_id)
        new_license_count = app.license_count - item.quantity
        update_app_license_count(app, new_license_count)
    store_data()


def get_orders_by_customer_id(customer_id):
    """
    Get a list of orders by the customer's ID
    :param customer_id:
    :return:
    """
    result = []
    orders = get_all_orders()
    for order in orders:
        if str(order.customer_id) == str(customer_id):
            result.append(order)
    return result