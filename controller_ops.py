from model_objects import User, Customer
from model_ops import get_next_user_id, add_user, add_customer, \
    get_next_customer_id


def register_user(request):
    # TODO validate
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

    return success




