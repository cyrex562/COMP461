/**
 * Created by root on 10/28/14.
 */

/**
 * On completion, update the cart item count badge
 * @param data
 */
function add_to_cart_cb(data) {
    $("#cart_badge").text(data.total_cart_items);
    $('#catalog_form_action').val('get_app_details');
}

/**
 * add an item to the cart
 */
function add_to_cart(event) {
    event.preventDefault();
    $('#catalog_form_action').val('add_to_cart');
    var in_data = {
        app_id : $(this).val(),
        quantity : $('[name=quantity]').val()
    };

    $.ajax({
        url: 'catalog_action',
        contentType: "application/json; charset=utf-8",
        data: in_data,
        type: 'POST',
        success: function (response) {
            add_to_cart_cb(response);
        },
        error: function (error) {
            console.log(error);
        }
    });
}

$(document).ready(function() {
    $('.add_to_cart_btn').click(add_to_cart);
});