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
from model_objects import User, Customer, App


################################################################################
# FUNCTIONS
################################################################################
def get_all_users():
    user_table = get_table('users')
    return user_table


def get_all_customers():
    customer_table = get_table('customers')
    return customer_table


def get_all_apps():
    app_table = get_table('apps')
    return app_table


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


def get_xml_tag_string(soup_ele):
    return unicode(soup_ele.contents[0].string.strip())


def user_data_loader(soup):
    users = soup.data.users
    for user_child_xml in users.children:
        if user_child_xml.string != '\n':
            user_to_add = User()
            user_to_add.id = user_child_xml['id']
            user_to_add.user_type = user_child_xml['user_type']
            user_to_add.username = get_xml_tag_string(user_child_xml.username)
            user_to_add.password = get_xml_tag_string(user_child_xml.password)
            add_table_row('users', user_to_add)


def app_data_loader(soup):
    apps_xml = soup.data.apps
    for app_xml in apps_xml.children:
        if app_xml.string != '\n':
            app_to_add = App()
            app_to_add.id = int(app_xml['id'])
            app_to_add.app_name = get_xml_tag_string(app_xml.app_name)
            app_to_add.download_link = get_xml_tag_string(app_xml.download_link)
            app_to_add.platform = get_xml_tag_string(app_xml.platform)
            app_to_add.platform_requirements = get_xml_tag_string(
                app_xml.platform_requirements)
            app_to_add.app_publisher = get_xml_tag_string(app_xml.app_publisher)
            app_to_add.app_description = get_xml_tag_string(
                app_xml.app_description)
            app_to_add.license_count = int(get_xml_tag_string(
                app_xml.license_count))
            app_to_add.app_image = get_xml_tag_string(app_xml.app_image)
            app_to_add.price = float(get_xml_tag_string(app_xml.price))
            add_table_row('apps', app_to_add)


def customer_data_loader(soup):
    customers = soup.data.customers
    for customer_xml in customers.children:
        if customer_xml.string != '\n':
            customer_to_add = Customer()
            customer_to_add.id = customer_xml['id']
            customer_to_add.user_id = get_xml_tag_string(customer_xml.user_id)
            customer_to_add.billing_address = get_xml_tag_string(
                customer_xml.billing_address)
            customer_to_add.shipping_address = get_xml_tag_string(
                customer_xml.shipping_address)
            customer_to_add.email_address = \
                get_xml_tag_string(customer_xml.email_address)
            customer_to_add.person_name = \
                get_xml_tag_string(customer_xml.person_name)
            customer_to_add.rating = get_xml_tag_string(customer_xml.rating)
            add_table_row('customers', customer_to_add)


def append_xml_tag(soup, tag_parent, tag_name, tag_val):
    new_tag = soup.new_tag(tag_name)
    new_tag.string = tag_val
    tag_parent.append(new_tag)


def user_data_storage_handler(soup):
    users = get_all_users()
    for u in users:
        new_user_tag = soup.new_tag('user', id=u.id)
        append_xml_tag(soup, new_user_tag, 'username', u.username)
        append_xml_tag(soup, new_user_tag, 'password', u.password)
        soup.data.users.append(new_user_tag)


def customer_data_storage_handler(soup):
    customers = get_all_customers()
    for c in customers:
        new_customer_tag = soup.new_tag('customer', id=c.id)
        append_xml_tag(soup, new_customer_tag, 'user_id', c.user_id)
        append_xml_tag(soup, new_customer_tag, 'billing_address',
                       c.billing_address)
        append_xml_tag(soup, new_customer_tag, 'shipping_address',
                       c.shipping_address)
        append_xml_tag(soup, new_customer_tag, 'email_address', c.email_address)
        append_xml_tag(soup, new_customer_tag, 'person_name', c.person_name)
        append_xml_tag(soup, new_customer_tag, 'rating', c.rating)
        soup.data.customers.append(new_customer_tag)


def app_data_storage_handler(soup):
    apps = get_all_apps()
    for a in apps:
        new_app_tag = soup.new_tag('app', id=a.id)
        append_xml_tag(soup, new_app_tag, 'app_name', a.app_name)
        append_xml_tag(soup, new_app_tag, 'download_link', a.download_link)
        append_xml_tag(soup, new_app_tag, 'platform', a.platform)
        append_xml_tag(soup, new_app_tag, 'platform_requirements',
                       a.platform_requirements)
        append_xml_tag(soup, new_app_tag, 'app_publisher', a.app_publisher)
        append_xml_tag(soup, new_app_tag, 'app_description', a.app_description)
        append_xml_tag(soup, new_app_tag, 'license_count',
                       str(a.license_count))
        append_xml_tag(soup, new_app_tag, 'app_image', a.app_image)
        append_xml_tag(soup, new_app_tag, 'price', str(a.price))
        soup.data.apps.append(new_app_tag)


def add_user(new_user):
    add_table_row('users', new_user)
    store_data()


def add_customer(new_customer):
    add_table_row('customers', new_customer)
    store_data()


################################################################################
# END OF FILE
################################################################################