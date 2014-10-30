/**
 * @file account.js
 * @brief Account-related script
 * @author Josh Madden <cyrex562@gmail.com>
 */

/**
 * Render the order
 * @param result
 */
function show_order_cb(result) {
    if (result.message === 'success') {
        $('#order_details_customer_name').text(result.data.customer.person_name);
        $('#order_details_customer_email').text(result.data.customer.email_address);
        $('#order_details_billing_address').text(result.data.order.billing_address);
        $('#order_details_shipping_address').text(result.data.order.shipping_address);
        $('#order_details_handling_fee').text(result.data.order.handling_fee);
        /** @namespace result.data.order.tax_amount */
        $('#order_details_tax').text(result.data.order.tax_amount);
        /** @namespace result.data.order.total_cost */
        $('#order_details_total').text(result.data.order.total_cost);
        $('#order_details_subtotal').text(result.data.order.subtotal);
        var order_history_details_table = $('#order_history_details_table');
        order_history_details_table.find("tr:gt(0)").remove();
        for (var i = 0; i < result.data.order.items.length; i++) {
            order_history_details_table.append(
                gen_order_details_row(result.data.order.items[i]));
        }
        $('#order_history_modal').modal('show');
    } else {
        console.log('failed to get order details')
    }
}

/**
 * Show the order
 */
function show_order() {
    var in_data = {
      order_id: $(this).attr('id')
    };
    post_request('get_order', show_order_cb, in_data);
}

/**
 * Document Ready
 */
$(document).ready(function() {
   $('.order_row').click(show_order);
});