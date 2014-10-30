"""
@file model_xml.py
@brief model xml operations
@author Josh Madden <cyrex562@gmail.com>
"""
################################################################################
# IMPORTS
################################################################################
import os
from bs4 import BeautifulSoup
from data_gateway import add_table_row
from model_objects import User, App, Customer, Order, CartItem
from model_ops import get_all_users, get_all_customers, get_all_apps, \
    get_all_orders
import utils

################################################################################
# DEFINES
################################################################################
XML_FILE = 'data.xml'

load_data_handlers = []
store_data_handlers = []


################################################################################
# FUNCTIONS
################################################################################
def get_xml_tag_string(soup_ele):
    """
    Get the string contents of an XML tag from the DOM
    :param soup_ele:
    :return:
    """
    return unicode(soup_ele.contents[0].string.strip())


def user_data_loader(soup):
    """
    load user data from XML DOM
    :param soup:
    :return:
    """
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
    """
    Load app data from the XML DOM
    :param soup:
    :return:
    """
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
            app_to_add.license_count = int(get_xml_tag_string(app_xml.license_count))
            app_to_add.app_image = get_xml_tag_string(app_xml.app_image)
            app_to_add.price = float(get_xml_tag_string(app_xml.price))
            add_table_row('apps', app_to_add)


def customer_data_loader(soup):
    """
    Load customer data from the XML DOM
    :param soup:
    :return:
    """
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
            customer_to_add.email_address = get_xml_tag_string(customer_xml.email_address)
            customer_to_add.person_name = get_xml_tag_string(customer_xml.person_name)
            customer_to_add.rating = get_xml_tag_string(customer_xml.rating)
            add_table_row('customers', customer_to_add)


def order_data_loader(soup):
    """
    Load order data from the XML document
    :param soup:
    :return:
    """
    orders = soup.data.orders
    for order_xml in orders.children:
        if order_xml.string != '\n':
            order_to_add = Order()
            order_to_add.id = order_xml['id']
            order_to_add.handling_fee = float(get_xml_tag_string(
                order_xml.handling_fee))
            order_to_add.tax_amount = float(get_xml_tag_string(
                order_xml.tax_amount))
            order_to_add.total_cost = float(get_xml_tag_string(
                order_xml.total_cost))
            order_to_add.subtotal = float(get_xml_tag_string(
                order_xml.subtotal))
            order_to_add.customer_id = int(get_xml_tag_string(
                order_xml.customer_id))
            for item_xml in order_xml.items.children:
                if item_xml.string != '\n':
                    item_to_add = CartItem()
                    item_to_add.app_id = int(get_xml_tag_string(
                        item_xml.app_id))
                    item_to_add.quantity = int(get_xml_tag_string(
                        item_xml.quantity
                    ))
                    item_to_add.subtotal = int(get_xml_tag_string(
                        item_xml.subtotal))
                    order_to_add.items.append(item_to_add)
            add_table_row('orders', order_to_add)


def append_xml_tag(soup, tag_parent, tag_name, tag_val):
    """
    Append an xml tag and its value to a DOM
    :param soup:
    :param tag_parent:
    :param tag_name:
    :param tag_val:
    :return:
    """
    new_tag = soup.new_tag(tag_name)
    new_tag.string = tag_val
    tag_parent.append(new_tag)


def user_data_storage_handler(soup):
    """
    Store users from redis store into xml file
    :param soup:
    :return:
    """
    users = get_all_users()
    for u in users:
        new_user_tag = soup.new_tag('user', id=u.id)
        append_xml_tag(soup, new_user_tag, 'username', u.username)
        append_xml_tag(soup, new_user_tag, 'password', u.password)
        soup.data.users.append(new_user_tag)


def customer_data_storage_handler(soup):
    """
    Store customers from redis store into xml file
    :param soup:
    :return:
    """
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
    """
    Store apps from redis store into xml file
    :param soup:
    :return:
    """
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
        append_xml_tag(soup, new_app_tag, 'license_count', str(a.license_count))
        append_xml_tag(soup, new_app_tag, 'app_image', a.app_image)
        append_xml_tag(soup, new_app_tag, 'price', str(a.price))
        soup.data.apps.append(new_app_tag)


def order_data_storage_handler(soup):
    """
    Store orders from redis store into xml file
    :param soup:
    :return:
    """
    orders = get_all_orders()
    for o in orders:
        new_order_tag = soup.new_tag('order', id=o.id)
        append_xml_tag(soup, new_order_tag, 'order_handling_fee',
                       o.handling_fee)
        append_xml_tag(soup, new_order_tag, 'order_tax_amount', o.tax_amount)
        append_xml_tag(soup, new_order_tag, 'order_total_cost', o.total_cost)
        append_xml_tag(soup, new_order_tag, 'order_subtotal', o.subtotal)
        append_xml_tag(soup, new_order_tag, 'order_customer_id', o.customer_id)
        items_tag = soup.new_tag('items')
        new_order_tag.append(items_tag)
        for i in o.items:
            new_item_tag = soup.new_tag('order_item')
            append_xml_tag(soup, new_item_tag, 'app_id', i.app_id)
            append_xml_tag(soup, new_item_tag, 'quantity', i.quantity)
            append_xml_tag(soup, new_item_tag, 'subtotal', i.subtotal)
            new_order_tag.items.append(new_item_tag)
        soup.data.orders.append(new_order_tag)


def load_data():
    """
    Load the persistent data from the data xml file.
    :return: void
    """
    path = os.path.dirname(utils.__file__)
    soup = BeautifulSoup(open(path + '/' + XML_FILE), "xml")
    for f in load_data_handlers:
        f(soup)


def store_data():
    """
    Store in-memory data to the data xml file
    :return:
    """
    # create a new xml document
    soup = BeautifulSoup()
    soup.append(soup.new_tag('data'))
    soup.data.append(soup.new_tag('users'))
    soup.data.append(soup.new_tag('customers'))
    soup.data.append(soup.new_tag('products'))
    for f in store_data_handlers:
        f(soup)
    out_xml = soup.prettify()
    xml_file = open(os.getcwd() + '/enterprise_app_project/' +
                    XML_FILE, 'wb')
    xml_file.write(out_xml)
    xml_file.close()


################################################################################
# END OF FILE
################################################################################
