"""
@file model_ops.py
@brief data model operations, rules, and logic
@author Josh Madden <cyrex562@gmail.com>
"""
from data_gateway import get_table, add_table_row, set_table
from model_objects import User, Order, Customer
from model_xml import store_data


def get_all_users():
    user_table = get_table('users')
    return user_table


def get_all_customers():
    customer_table = get_table('customers')
    return customer_table


def get_all_apps():
    app_table = get_table('apps')
    return app_table


def get_all_orders():
    order_table = get_table('orders')
    return order_table


def get_user_by_id(in_id):
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
    found_customer = None
    customers = get_all_customers()
    for c in customers:
        if c.user_id == in_user_id:
            found_customer = c
            break

    return found_customer


def get_app_by_id(in_app_id):
    found_app = None
    apps = get_all_apps()
    for a in apps:
        if a.id == in_app_id:
            found_app = a
            break
    return found_app


def get_next_user_id():
    users = get_all_users()
    next_user_id = 0
    for u in users:
        if int(u.get_id()) > next_user_id:
            next_user_id = int(u.get_id()) + 1
    return next_user_id


def get_next_customer_id():
    customers = get_all_customers()
    next_customer_id = 0
    for c in customers:
        if int(c.id) > next_customer_id:
            next_customer_id = int(c.id) + 1
    return next_customer_id


def get_next_order_id():
    orders = get_all_orders()
    next_order_id = 0
    for o in orders:
        if int(o.id) > next_order_id:
            next_order_id = int(o.id) + 1
    return next_order_id


def get_user_by_username(in_username):
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
    add_table_row('users', new_user)


def add_customer(new_customer):
    add_table_row('customers', new_customer)


def add_order(new_order):
    add_table_row('orders', new_order)


def add_item_to_cart(item, cart):
    cart.items.append(item)
    return cart


def remove_item_from_cart(cart, app_id):
    item_to_remove = None
    for item in cart.items:
        if int(item.app_id) == app_id:
            item_to_remove = item
            break
    if item_to_remove is not None:
        cart.items.remove(item_to_remove)
    return cart


def clear_cart(cart):
    cart.items = []
    return cart


def get_apps_for_cart_items(cart):
    for item in cart.items:
        if item.app is None:
            app = get_app_by_id(int(item.app_id))
            item.app = app
    return cart


def update_item_subtotals(cart):
    for item in cart.items:
        item.subtotal = round(item.app.price * item.quantity, 2)
    return cart


def update_cart_total(cart):
    cart.total = 0.0
    for item in cart.items:
        cart.total += item.subtotal
    cart.total = round(cart.total, 2)
    return cart


def change_cart_item_quantity(cart, app_id, new_quantity):
    for item in cart.items:
        if int(item.app_id) == app_id:
            item.quantity = new_quantity
            break
    return cart


def get_handling_fee(cart):
    return round(cart.total * 0.2, 2)


def calc_order_tax(cart, handling_fee):
    return round((cart.total + handling_fee) * 0.07, 2)


def calc_order_total(cart, tax, handling_fee):
    return round(cart.total + tax + handling_fee, 2)


def check_stock(cart):
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


def update_app_license_count(app, new_license_count):
    apps = get_all_apps()
    for i in range(0, len(apps) - 1):
        if str(apps[i].id) == str(app.id):
            apps[i].license_count = new_license_count
    set_table('apps', apps)


def register_user(request):
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
    for item in cart.items:
        app = get_app_by_id(item.app_id)
        new_license_count = app.license_count - item.quantity
        update_app_license_count(app, new_license_count)
    store_data()


def get_orders_by_customer_id(customer_id):
    result = []
    orders = get_all_orders()
    for order in orders:
        if str(order.customer_id) == str(customer_id):
            result.append(order)
    return result