################################################################################
# @file model_ops.py
# @brief data model operations
# @author Josh Madden
# @copyright Fifth Column Group 2014
################################################################################
################################################################################
# IMPORTS
################################################################################
from data_gateway import get_table, load_data_handlers, add_table_row, \
    store_data
from model_objects import User, Customer


################################################################################
# FUNCTIONS
################################################################################
def get_all_users():
    user_table = get_table('users')
    return user_table


def get_all_customers():
    customer_table = get_table('customers')
    return customer_table


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


def user_data_loader(soup):
    users = soup.data.users
    for user_child_xml in users.children:
        if user_child_xml.string != '\n':
            user_to_add = User()
            user_to_add.id = user_child_xml['id']
            user_to_add.username = \
                unicode(user_child_xml.username.contents[0].string.strip())
            user_to_add.password = \
                unicode(user_child_xml.password.contents[0].string.strip())
            add_table_row('users', user_to_add)


def customer_data_loader(soup):
    customers = soup.data.customers
    for customer_xml in customers.children:
        if customer_xml.string != '\n':
            customer_to_add = Customer()
            customer_to_add.id = customer_xml['id']
            customer_to_add.user_id = unicode(customer_xml.user_id.contents[
                                                  0].string.strip())
            customer_to_add.billing_address = unicode(
                customer_xml.billing_address.contents[
                    0].string.strip())
            customer_to_add.shipping_address = unicode(
                customer_xml.shipping_address.contents[
                    0].string.strip())
            customer_to_add.email_address = unicode(
                customer_xml.email_address.contents[
                                                  0].string.strip())
            customer_to_add.person_name = unicode(
                customer_xml.person_name.contents[
                                                  0].string.strip())
            customer_to_add.rating = unicode(customer_xml.rating.contents[
                                                  0].string.strip())
            add_table_row('customers', customer_to_add)


def user_data_storage_handler(soup):
    users = get_all_users()
    for u in users:
        soup.data.users.append(soup.new_tag('user', id=u.id))
        user_xml = soup.data.users.find_all(id=u.id)[0]
        user_xml.append(soup.new_tag('username'))
        user_xml.username.append(u.username)
        user_xml.append(soup.new_tag('password'))
        user_xml.password.append(u.password)


def customer_data_storage_handler(soup):
    customers = get_all_customers()
    for c in customers:
        soup.data.customers.append(soup.new_tag('customer', id=c.id))
        customer_xml = soup.data.customers.find_all(id=c.id)[0]
        customer_xml.append(soup.new_tag('user_id'))
        customer_xml.user_id.append(c.user_id)
        customer_xml.append(soup.new_tag('billing_address'))
        customer_xml.billing_address.append(c.billing_address)
        customer_xml.append(soup.new_tag('shipping_address'))
        customer_xml.shipping_address.append(c.shipping_address)
        customer_xml.append(soup.new_tag('email_address'))
        customer_xml.email_address.append(c.email_address)
        customer_xml.append(soup.new_tag('person_name'))
        customer_xml.person_name.append(c.person_name)
        customer_xml.append(soup.new_tag('rating'))
        customer_xml.rating.append(c.rating)


def add_user(new_user):
    add_table_row('users', new_user)
    store_data()


def add_customer(new_customer):
    add_table_row('customers', new_customer)
    store_data()


################################################################################
# END OF FILE
################################################################################