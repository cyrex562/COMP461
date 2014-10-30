/**
 * @file common.js
 * @brief common functions for the application
 * @author Josh Madden <cyrex562@gmail.com>
 */

/**
 *
 * @param item
 * @returns {string}
 */
function gen_order_details_row(item) {
    return '' +
        '<tr>' +
        '<td>' + item.app.app_name + '</td>' +
        '<td>' + item.quantity + '</td>' +
        '<td>$' + item.app.price + '</td>' +
        '<td>$' + item.subtotal + '</td>' +
        '</tr>';
}

/**
 * Perform a POST request, on success call the callback and pass the response
 * rom the server
 * @param action the server-side API action
 * @param callback the callback to call on success
 * @param in_data data to pass to the server
 */
function post_request(action, callback, in_data) {
    console.log('sending request: ' + action + ', in_data: ' + in_data);
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

















