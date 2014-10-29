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
}

function show_app_details(event) {
    var button = $(event.target);
    var app_id = button.val();
    post_request('app', show_app_details_cb, {app_id: app_id});
}

function add_to_cart_cb(result) {
    if (result.message === 'success') {
        $('#cart_badge').text(result.data.total_cart_items);
    } else {
        console.log('failed to add item to cart');
    }
}

function add_to_cart(event) {
    var app_id = $(this).val();
    var in_data = {
        app_id: app_id,
        quantity: $('#app_row_' + app_id + ' .add_to_cart_quantity').val()
    };
    post_request('add_to_cart', add_to_cart_cb, in_data);
}

function modal_add_to_cart_cb(result) {
    $('#app_details_modal').modal('hide');
    add_to_cart_cb(result);
}

function modal_add_to_cart(event) {
    var in_data = { app_id: $('#app_id').val(),
        quantity: $('#app_details_modal_quantity').val()};
    post_request('add_to_cart', modal_add_to_cart_cb, in_data);
}

function modal_add_to_cart_and_checkout_cb(result) {
    $('#app_details_modal').modal('hide');
    add_to_cart_cb(result);

}

function modal_add_to_cart_and_checkout(event) {
    post_request('add_to_cart',
        modal_add_to_cart_and_checkout_cb,
        {app_id: $('#app_id').val(), quantity: qty});
}

function show_check_out(event) {
    $('#checkout_modal').modal('show');
    // TODO: populate addresss, customer info, order info, etc.'
}

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
        '<span class="glyphicon glyphicon-remove"></span></button>' +
        '</tr>';
    return row;
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

        $('.remove_item_btn').click(function(event) {
            remove_item_from_cart(parseInt($(this).val()));
        })

        $('#cart_total').text('$' + cart.total);
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


function remove_item_from_cart_cb(result) {
    if (result.message === 'success') {
        var cart_table_body = $('#cart_table_body');
        cart_table_body.empty();
        var cart = result.data.cart;
        for (var i = 0; i < cart.items.length; i++) {
            var cart_item = cart.items[i];
            cart_table_body.append(gen_cart_row(cart_item));
        }
        $('#cart_total').text('$' + cart.total);
    }
}

function remove_item_from_cart(app_id) {
    post_request('remove_item_from_cart', remove_item_from_cart_cb, {app_id: app_id});
}


$(document).ready(function () {
    $('.add_to_cart_btn').click(add_to_cart);
    $('.app_details_btn').click(show_app_details);
    $('#modal_add_to_cart_btn').click(modal_add_to_cart);
    $('#modal_add_to_cart_and_checkbout_btn').click(modal_add_to_cart_and_checkout);
    $('#cart_btn').click(get_cart);
    $('#continue_shopping_btn').click(function () {
        $('#cart_modal').modal('hide');
    });

//    $('.app_quantity').on('input', function () {
//        var app_id = $(this).data("app_id");
//        var new_quantity = parseInt($(this).val());
//        change_cart_item_quantity(app_id, new_quantity);
//    });

    $('.remove_item_btn').click(function () {
        var app_id = parseInt($(this).val());
        remove_item_from_cart(app_id);
    });
    update_cart_items_count();
});