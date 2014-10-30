/**
 * Perform a POST request, on success call the callback and pass the response
 * rom the server
 * @param action the server-side API action
 * @param callback the callback to call on success
 * @param in_data data to pass to the server
 */
function post_request(action, callback, in_data) {
    $.ajax({
        type: "POST",
        url: $SCRIPT_ROOT + "/" + action,
        dataType: "json",
        data: JSON.stringify(in_data),
        contentType: "application/json; charset=utf-8",
        cache: false})
        .done(function (data) {
            callback(data)
        })
        .fail(function (xhlr, status_txt, err_thrown) {
            console.log('error, status: %s, err: %s', status_txt, err_thrown);
        });
}

/**
 *
 * @param response
 */
function app_details_get_user_logged_in_cb(response) {
    if (!response.data.user_logged_in) {
        $('#modal_add_to_cart_and_checkout_btn').prop('disabled', true);
    } else {
        $('#modal_add_to_cart_and_checkout_btn').prop('disabled', false);
    }
}

/**
 *
 * @param result
 */
function show_app_details_cb(result) {
    $('#app_details_modal').modal('show');
    var app = result.data.app;
    $('#app_img').attr('src', '/static/img/' + app.app_image);
    $('#app_id').text(app.id);
    $('#app_name').text(app.app_name);
    $('#app_platform').text(app.platform);
    $('#app_platform_requirements').text(app.platform_requirements);
    $('#app_plublisher').text(app.app_publisher);
    $('#app_description').text(app.app_description);
    $('#app_license_count').text(app.license_count);
    $('#app_price').text('$' + app.price);
    post_request('user_logged_in', app_details_get_user_logged_in_cb, {});
}

/**
 *
 * @param event
 */
function show_app_details(event) {
    var button = $(event.target);
    var app_id = button.val();
    post_request('app', show_app_details_cb, {app_id: app_id});
}

/**
 *
 * @param result
 */
function add_to_cart_cb(result) {
    if (result.message === 'success') {
        $('#cart_badge').text(result.data.total_cart_items);
    } else {
        console.log('failed to add item to cart');
    }
}

/**
 *
 * @param event
 */
function add_to_cart(event) {
    var app_id = $(this).val();
    var in_data = {
        app_id: app_id,
        quantity: $('#app_row_' + app_id + ' .add_to_cart_quantity').val()
    };
    post_request('add_to_cart', add_to_cart_cb, in_data);
}

/**
 *
 * @param result
 */
function modal_add_to_cart_cb(result) {
    $('#app_details_modal').modal('hide');
    add_to_cart_cb(result);
}

/**
 *
 * @param event
 */
function modal_add_to_cart(event) {
    var in_data = { app_id: $('#app_id').val(),
        quantity: $('#app_details_modal_quantity').val()};
    post_request('add_to_cart', modal_add_to_cart_cb, in_data);
}

/**
 *
 * @param result
 */
function modal_add_to_cart_and_checkout_cb(result) {
    $('#app_details_modal').modal('hide');
    add_to_cart_cb(result);
    show_check_out()
}

/**
 *
 * @param event
 */
function modal_add_to_cart_and_checkout(event) {
    var in_data = { app_id: $('#app_id').val(),
        quantity: $('#app_details_modal_quantity').val()};
    post_request('add_to_cart', modal_add_to_cart_and_checkout_cb, in_data);
}

/**
 *
 * @param cart_item
 * @returns {string}
 */
function gen_cart_row(cart_item) {
    var row = '' +
        '<tr id="' + cart_item.app.id + '">' +
        '<td>' + cart_item.app.app_name + '</td>' +
        '<td><div class="container-fluid"><div class="row"><div class="col-xs-7">' +
        '<input type="number" min="1" class="form-control app_quantity" value="'
        + cart_item.quantity + '" data-options=\'{"app_id": ' + cart_item.app.id + '}\'></div></div></div></td>' +
        '<td>$' + cart_item.app.price + '</td>' +
        '<td class="cart_item_subtotal">$' + cart_item.subtotal + '</td>' +
        '<td><button class="btn btn-xs remove_item_btn" value="' + cart_item.app.id + '">' +
        '<span class="glyphicon glyphicon-remove"></span></button></td>' +
        '</tr>';
    return row;
}

/**
 * Refresh the cart table and re-bind events.
 * @param result data returned by the server.
 */
function remove_item_from_checkout_cb(result) {
    if (result.message === 'success') {
        var order_table_body = $('#order_table_body');
        order_table_body.empty();

        var cart = result.data.cart;
        for (var i = 0; i < cart.items.length; i++) {
            var cart_item = cart.items[i];
            order_table_body.append(gen_cart_row(cart_item));
        }

        $('.app_quantity').bind('keyup change click', function (e) {
            if (!$(this).data("previousValue") ||
                $(this).data("previousValue") != $(this).val()) {
                $(this).data("previousValue", $(this).val());
                var app_id = $(this).data("options").app_id;
                var new_quantity = parseInt($(this).val());
                change_checkout_item_quantity(app_id, new_quantity);
            }
        });

        $('.remove_item_btn').click(function (event) {
            remove_item_from_checkout(parseInt($(this).val()));
        });

        $('#order_subtotal').text('$' + result.data.cart.total);
        $('#order_handling_fee').text('$' + result.data.handling_fee);
        $('#order_tax').text('$' + result.data.tax);
        $('#order_total').text('$' + result.data.order_total) ;
    }
}

/**
 *
 * @param app_id
 */
function remove_item_from_checkout(app_id) {
    post_request('remove_item_from_cart', remove_item_from_checkout_cb, {app_id: app_id});
}

/**
 *
 * @param result
 */
function change_checkout_item_quantity_cb(result) {
    if (result.message === 'success') {
        var cart_item = undefined;
        for (var i = 0; i < result.data.cart.items.length; i++) {
            if (result.data.cart.items[i].app_id === result.data.app_id) {
                cart_item = result.data.cart.items[i];
                break;
            }
        }
        $('#' + result.data.app_id + ' .cart_item_subtotal')
            .text(cart_item.subtotal);
        //$('#cart_total').text('$' + result.data.cart.total);
        $('#order_subtotal').text('$' + result.data.cart.total);
        $('#order_handling_fee').text('$' + result.data.handling_fee);
        $('#order_tax').text('$' + result.data.tax);
        $('#order_total').text('$' + result.data.order_total) ;
    }
}

/**
 *
 * @param app_id
 * @param new_quantity
 */
function change_checkout_item_quantity(app_id, new_quantity) {
    if (new_quantity > 0) {
        post_request('change_checkout_item_quantity',
            change_checkout_item_quantity_cb,
            {app_id: app_id, new_quantity: new_quantity});
    } else {
        remove_item_from_cart(app_id);
    }
}

/**
 *
 * @param result a JSON object {
 *  'message' : TEXT,
 *  'data' : {
 *      'customer': customer object JSON,
 *      'cart': cart object JSON,
 *      'handling_fee': DECIMAL,
 *      'order_total': DECIMAL,
 *     'tax': DECIMAL }}
 */
function show_check_out_cb(result) {
    if (result.message === 'success') {
        $('#order_customer_name').val(result.data.customer.person_name);
        $('#order_customer_email').val(result.data.customer.email_address);
        $('#order_shipping_address').val(result.data.customer.shipping_address);
        $('#order_billing_address').val(result.data.customer.billing_address);
        $('#order_subtotal').text('$' + result.data.cart.total);
        $('#order_handling_fee').text('$' + result.data.handling_fee);
        $('#order_tax').text('$' + result.data.tax);
        $('#order_total').text('$' + result.data.order_total);
        $('#order_customer_id').val(result.data.customer.id);
        var order_table_body = $('#order_table_body');
        order_table_body.empty();

        var cart = result.data.cart;
        for (var i = 0; i < cart.items.length; i++) {
            var cart_item = cart.items[i];
            order_table_body.append(gen_cart_row(cart_item));
        }

        $('.app_quantity').bind('keyup change click', function (e) {
            if (!$(this).data("previousValue") ||
                $(this).data("previousValue") != $(this).val()) {
                $(this).data("previousValue", $(this).val());
                var app_id = $(this).data("options").app_id;
                var new_quantity = parseInt($(this).val());
                change_checkout_item_quantity(app_id, new_quantity);
            }
        });

        $('.remove_item_btn').click(function (event) {
            remove_item_from_checkout(parseInt($(this).val()));
        });


    } else {
        console.log('failed to get checkout data');
    }
 }


function show_check_out() {
    $('#cart_modal').modal('hide');
    $('#checkout_modal').modal('show');
    post_request('get_checkout_data', show_check_out_cb, {});
}


function change_cart_item_quantity_cb(result) {
    if (result.message === 'success') {
        var cart_item = undefined;
        for (var i = 0; i < result.data.cart.items.length; i++) {
            if (result.data.cart.items[i].app_id === result.data.app_id) {
                cart_item = result.data.cart.items[i];
                break;
            }
        }
        $('#' + result.data.app_id + ' .cart_item_subtotal').text(cart_item.subtotal);
        $('#cart_total').text('$' + result.data.cart.total);
    }
}

function change_cart_item_quantity(app_id, new_quantity) {
    if (new_quantity > 0) {
        post_request('change_cart_item_quantity', change_cart_item_quantity_cb,
            {app_id: app_id, new_quantity: new_quantity});
    } else {
        remove_item_from_cart(app_id);
    }
}

/**
 *
 * @param response JSON {
 *  'message': TEXT,
 *  'data': {
 *      'user_logged_in': BOOL
 *  }}
 */
function cart_user_logged_in_cb(response) {
    if (!response.data.user_logged_in)  {
        $('#check_out_btn').prop('disabled', true);
    } else {
        $('#check_out_btn').prop('disabled', false);
    }
}

function get_cart_cb(result) {
    $('#cart_modal').modal('show');

    if (result.message === 'success') {
        var cart_table_body = $('#cart_table_body');
        cart_table_body.empty();
        var cart = result.data.cart;
        for (var i = 0; i < cart.items.length; i++) {
            var cart_item = cart.items[i];
            cart_table_body.append(gen_cart_row(cart_item));
        }

        $('.app_quantity').bind('keyup change click', function (e) {
            if (!$(this).data("previousValue") ||
                $(this).data("previousValue") != $(this).val()) {
                $(this).data("previousValue", $(this).val());
                var app_id = $(this).data("options").app_id;
                var new_quantity = parseInt($(this).val());
                change_cart_item_quantity(app_id, new_quantity);
            }
        });

        $('.remove_item_btn').click(function (event) {
            remove_item_from_cart(parseInt($(this).val()));
        });

        $('#cart_total').text('$' + cart.total);

        post_request('user_logged_in', cart_user_logged_in_cb, {});
    } else {
        console.log('failed to get cart');
    }
}


function get_cart(event) {
    event.preventDefault();
    post_request('cart', get_cart_cb, {});
}

function update_cart_items_count_cb(result) {
    if (result.message === 'success') {
        $('#cart_badge').text(result.data.total_cart_items);
    }
}

function update_cart_items_count() {
    post_request('cart_items_count', update_cart_items_count_cb, {});
}

/**
 * Refresh the cart table and re-bind events.
 * @param result data returned by the server.
 */
function remove_item_from_cart_cb(result) {
    if (result.message === 'success') {
        var cart_table_body = $('#cart_table_body');
        cart_table_body.empty();
        var cart = result.data.cart;
        for (var i = 0; i < cart.items.length; i++) {
            var cart_item = cart.items[i];
            cart_table_body.append(gen_cart_row(cart_item));
        }
        $('.app_quantity').bind('keyup change click', function (e) {
            if (!$(this).data("previousValue") ||
                $(this).data("previousValue") != $(this).val()) {
                $(this).data("previousValue", $(this).val());
                var app_id = $(this).data("options").app_id;
                var new_quantity = parseInt($(this).val());
                change_cart_item_quantity(app_id, new_quantity);
            }
        });

        $('.remove_item_btn').click(function(event) {
            remove_item_from_cart(parseInt($(this).val()));
        });

        $('#cart_total').text('$' + cart.total);
    }
}

function remove_item_from_cart(app_id) {
    post_request('remove_item_from_cart', remove_item_from_cart_cb, {app_id: app_id});
}

function clear_shopping_cart_cb(result) {
    if (result.message === 'success') {
        var cart_table_body = $('#cart_table_body');
        cart_table_body.empty();
        var cart = result.data.cart;
        for (var i = 0; i < cart.items.length; i++) {
            var cart_item = cart.items[i];
            cart_table_body.append(gen_cart_row(cart_item));
        }
        $('.app_quantity').bind('keyup change click', function (e) {
            if (!$(this).data("previousValue") ||
                $(this).data("previousValue") != $(this).val()) {
                $(this).data("previousValue", $(this).val());
                var app_id = $(this).data("options").app_id;
                var new_quantity = parseInt($(this).val());
                change_cart_item_quantity(app_id, new_quantity);
            }
        });

        $('.remove_item_btn').click(function(event) {
            remove_item_from_cart(parseInt($(this).val()));
        });

        $('#cart_total').text('$' + cart.total);
    }
}

function clear_shopping_cart() {
    post_request('clear_cart', clear_shopping_cart_cb, {});
}

function same_address_cbx_change(event) {
    if ($(this).is(':checked')) {
        $('#order_shipping_address').prop('disabled', true);
    } else {
        $('#order_shipping_address').prop('disabled', false);
    }
}

function gen_order_details_row(item) {
    var row = '' +
        '<tr>' +
        '<td>' + item.app.app_name + '</td>' +
        '<td>'+ item.app.quantity + '</td>' +
        '<td>$' + item.app.price + '</td>' +
        '<td>$' + item.subtotal + '</td>' +
        '</tr>';
    return row;
}

function place_order_cb(result) {
    if (result.message === 'success') {
        $('#checkout_modal').modal('hide');
        $('#order_details_modal').modal('show');
        $('#order_details_customer_name').text(result.data.customer.person_name);
        $('#order_details_customer_email').text(result.data.customer.email_address);
        $('#order_details_billing_address').text(result.data.order.billing_address);
        $('#order_details_shipping_address').text(result.data.order.shipping_address);
        $('#order_details_handling_fee').text(result.data.order.handling_fee);
        $('#order_details_tax').text(result.data.order.tax_amount);
        $('#order_details_total').text(result.data.order.total_cost);
        $('#order_details_subtotal').text(result.data.order.subtotal);
        $('#order_details_table_body').empty();
        for (var i=0; i < result.data.cart.items.length; i++) {
            $('#order_details_table_body').append(
                gen_order_details_row(result.data.cart.items[i]));
        }
    } else if (result.message === 'failure, invalid app quantity') {
        $('#order_errors').empty();
        for (var j = 0; j < result.data.invalid_items.length; j++) {
            var invalid_item = result.data.invalid_items[j];
            var order_error = "";
            if (invalid_item.available == 0) {
                order_error = '<div class="alert alert-warning ' +
                'alert-dismissible" role="alert"><button type="button" ' +
                'class="close" data-dismiss="alert"><span aria-hidden="true">' +
                '&times;</span><span class="sr-only">Close</span></button>' +
                'no licenses available for ' + invalid_item.name +
                '</div>';
            } else if (invalid_item.available > 0) {
                order_error = '<div class="alert alert-warning ' +
                'alert-dismissible" role="alert"><button type="button" ' +
                'class="close" data-dismiss="alert"><span aria-hidden="true">' +
                '&times;</span><span class="sr-only">Close</span></button>' +
                'requested licenses (' + invalid_item.requested  + ') for ' +
                invalid_item.name +  ' exceeds available (' +
                invalid_item.available + ')' + '</div>';
            }

            $('#order_errors').append(order_error);
        }
    } else {
        console.log('error occurred placing order ' + result);
    }
}

function place_order() {
    var in_data = {
        customer_id: $('#order_customer_id').val()
    };

    var order_billing_address = $('#order_billing_address');

    if ($('#same_address_cbx').is(':checked')) {
        in_data.shipping_address = order_billing_address.val();
        in_data.billing_address = order_billing_address.val();
    } else {
        in_data.shipping_address = $('#order_shipping_address').val();
        in_data.billing_address = order_billing_address.val();
    }

    post_request('place_order', place_order_cb, in_data);
}


$(document).ready(function () {
    $('.add_to_cart_btn').click(add_to_cart);
    $('.app_details_btn').click(show_app_details);
    $('#modal_add_to_cart_btn').click(modal_add_to_cart);
    $('#modal_add_to_cart_and_checkout_btn').click(modal_add_to_cart_and_checkout);
    $('#cart_btn').click(get_cart);
    $('#continue_shopping_btn').click(function () {
        $('#cart_modal').modal('hide');
    });

    $('.remove_item_btn').click(function () {
        var app_id = parseInt($(this).val());
        remove_item_from_cart(app_id);
    });

    $('#check_out_btn').click(show_check_out);
    $('#cancel_checkout_btn').click(function() {
       $('#checkout_modal').modal('hide');
    });
    $('#clear_cart_btn').click(clear_shopping_cart);
    update_cart_items_count();
    $('#same_address_cbx').change(same_address_cbx_change);
    $('#place_order_btn').click(place_order);
    $('#confirm_order_placed_btn').click(function() {
        $('#order_details_modal').modal('hide');
        location.reload();
    })
});