"""
@file model_persistence.py
@author Josh Madden <cyrex562@gmail.com>
@copyright Perfecta Federal 2014
"""
from model_ops import get_all_users, get_all_customers, get_all_apps, \
    get_all_orders
from model_xml import append_xml_tag


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
        append_xml_tag(soup, new_user_tag, 'user_type', u.user_type)
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
                       str(o.handling_fee))
        append_xml_tag(soup, new_order_tag, 'order_tax_amount',
                       str(o.tax_amount))
        append_xml_tag(soup, new_order_tag, 'order_total_cost',
                       str(o.total_cost))
        append_xml_tag(soup, new_order_tag, 'order_subtotal', str(o.subtotal))
        append_xml_tag(soup, new_order_tag, 'order_customer_id',
                       str(o.customer_id))
        append_xml_tag(soup, new_order_tag, 'order_shipping_address',
                       o.shipping_address)
        append_xml_tag(soup, new_order_tag, 'order_billing_address',
                       o.billing_address)
        items_tag = soup.new_tag('items')
        new_order_tag.append(items_tag)
        for i in o.items:
            new_item_tag = soup.new_tag('order_item')
            append_xml_tag(soup, new_item_tag, 'app_id', str(i.app_id))
            append_xml_tag(soup, new_item_tag, 'quantity', str(i.quantity))
            append_xml_tag(soup, new_item_tag, 'subtotal', str(i.subtotal))
            new_order_tag.items.append(new_item_tag)
        soup.data.orders.append(new_order_tag)