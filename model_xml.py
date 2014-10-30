"""
@file model_xml.py
@brief model xml operations
@author Josh Madden <cyrex562@gmail.com>
"""
import os

from bs4 import BeautifulSoup

from data_gateway import add_table_row
from model_objects import User, App, Customer, Order, CartItem
import utils

XML_FILE = 'data.xml'

load_data_handlers = []
store_data_handlers = []


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
            user_to_add.user_type = get_xml_tag_string(user_child_xml.user_type)
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
            app_to_add.license_count = \
                int(get_xml_tag_string(app_xml.license_count))
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
            customer_to_add.email_address = \
                get_xml_tag_string(customer_xml.email_address)
            customer_to_add.person_name = \
                get_xml_tag_string(customer_xml.person_name)
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
                order_xml.order_handling_fee))
            order_to_add.tax_amount = float(get_xml_tag_string(
                order_xml.order_tax_amount))
            order_to_add.total_cost = float(get_xml_tag_string(
                order_xml.order_total_cost))
            order_to_add.subtotal = float(get_xml_tag_string(
                order_xml.order_subtotal))
            order_to_add.customer_id = int(get_xml_tag_string(
                order_xml.order_customer_id))
            order_to_add.billing_address = get_xml_tag_string(
                order_xml.order_billing_address)
            order_to_add.shipping_address = get_xml_tag_string(
                order_xml.order_shipping_address)
            for item_xml in order_xml.items.children:
                if item_xml.string != '\n':
                    item_to_add = CartItem()
                    item_to_add.app_id = int(get_xml_tag_string(
                        item_xml.app_id))
                    item_to_add.quantity = int(get_xml_tag_string(
                        item_xml.quantity
                    ))
                    item_to_add.subtotal = float(get_xml_tag_string(
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
    soup.data.append(soup.new_tag('apps'))
    soup.data.append(soup.new_tag('orders'))
    for f in store_data_handlers:
        f(soup)
    out_xml = soup.prettify()
    path = os.path.dirname(utils.__file__)
    xml_file = open(path + '/' + XML_FILE, 'wb')
    xml_file.write(out_xml)
    xml_file.close()
