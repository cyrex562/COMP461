/**
 * Created by root on 8/9/14.
 */
var selected_trade_ids = [];

/**************************************
 *//**
 * @brief save existing row behavior callback
 *************************************/
function save_trade_row_cb(response)
{
    process_response(response);
    update_trade_list();
    set_trades_status_bar(response.msg);
}

/**************************************
 *//**
 * @brief save existing row behavior
 *************************************/
function save_trade_row()
{
    var trade_id = $(this).val();
    console.log('save row button clicked: ' + trade_id);
    // get form data
    var updated_trade_id = trade_id;
    var updated_trade_name = $('#trade-name-' + trade_id).val();
    //var updated_trade_type = $('#trade-type-' + trade_id).val();
    var updated_trade_type = 'test';
    var updated_trade_location = $('#trade-location-' + trade_id).val();
    var updated_wayppoint_notes = $('#trade-notes-' + trade_id).val();
    var updated_start_date = $('#trade-start-date-' + trade_id).val();
    var updated_end_date = $('#trade-end-date-' + trade_id).val();
    var data = { updated_trade_id: updated_trade_id,
        updated_trade_name: updated_trade_name,
        updated_trade_type: updated_trade_type,
        updated_trade_location: updated_trade_location,
        updated_trade_notes: updated_wayppoint_notes,
        updated_trade_start_date: updated_start_date,
        updated_trade_end_date: updated_end_date };
    send_request('update_trade', data, save_trade_row_cb);
}

/**************************************
 *//**
 * @brief Check if trade id is in the list of selected ids.
 *************************************/
function trade_id_in_sel_ids(trade_id)
{
    var result = -1;
    for (var i = 0; i < selected_trade_ids.length; i++) {
        if (selected_trade_ids[i] === trade_id) {
            result = i;
            break;
        }
    }
    return result;
}

/**************************************
 *//**
 * @brief selection toggle for checkbox
 *************************************/
function trade_select_change()
{
//    var raw_id = $(this).id;
    var trade_id = $(this).val();
    console.log('trade select toggled');
    console.log('selected trade ids before: "%s"', selected_trade_ids);
    var idx = trade_id_in_sel_ids(trade_id);
    if (idx > -1) {
        selected_trade_ids.splice(idx, 1);
        console.log('removing');
    } else {
        selected_trade_ids.push(trade_id);
        console.log('pushing');
    }
    console.log('selected trade ids after: "%s"', selected_trade_ids);
}

/**************************************
 *//**
 * @brief generate a row for a trade
 *************************************/
function gen_trade_row(trade)
{
    var row = '<tr><td><input type="checkbox" id="select-row-[trade_ID]" ' +
        'value="[trade_ID]" class="select-trade-row"></td>' +
        '<td><input type="text" id="trade-name-[trade_ID]" ' +
        'value="[trade_NAME]" placeholder="trade name"></td>' +
        '<td><select id="trade-type-[trade_ID]"></select></td>' +
        '<td><input type="text" id="trade-location-[trade_ID]" ' +
        'value="[trade_LOCATION]" placeholder="trade location"></td>' +
        '<td><input type="text" id="trade-start-date-[trade_ID]" ' +
        'value="[trade_START_DATE]" placeholder="trade start date">' +
        '</td>' +
        '<td><input type="text" id="trade-end-date-[trade_ID]" ' +
        'value="[trade_END_DATE]" placeholder="trade end date"></td>' +
        '<td><textarea id="trade-notes-[trade_ID]">' +
        '[trade_NOTES]</textarea></td>' +
        '<td>[TRADES]</td>' +
        '<td>[VOYAGE]</td>' +
        '<td><button id="expand-row-btn-[trade_ID]" class="btn">' +
        '<span class="glyphicon glyphicon-collapse-down"></span></button>' +
        '<button id="save-row-btn-[trade_ID]" value="[trade_ID]" ' +
        'class="btn">' +
        '<span class="glyphicon glyphicon-floppy-save"></span></button></td>' +
        '</tr>';

    row = row.replace(/\[trade_ID\]/g, trade.trade_id);
    row = row.replace(/\[trade_NAME\]/g, trade.trade_name);
    //row = row.replace(/\[trade_TYPE\]/g, trade.trade_type);
    row = row.replace(/\[trade_LOCATION\]/g, trade.trade_location);
    row = row.replace(/\[trade_START_DATE\]/g, trade.start_date);
    row = row.replace(/\[trade_END_DATE\]/g, trade.end_date);
    row = row.replace(/\[trade_NOTES]/g, trade.trade_notes);
    return row;
}

/**************************************
 *//**
 * @brief process response from server containing trade ids. add them all to the selection list and then toggle the state of all checkboxes to checked.
 *************************************/
function select_all_trades_cb(response)
{
    process_response(response);
    var msg = response.message;
    set_trades_status_bar(msg);
    selected_trade_ids = response.data.trade_ids;
    for (var i = 0; i < selected_trade_ids.length; i++) {
       $('#select-row-'+selected_trade_ids[i]).prop('checked', true);
    }
}

/**************************************
 *//**
 * @brief select all trades; send a request for all trade ids to the server.
 *************************************/
function select_all_trades()
{
    send_request('get_all_trade_ids', {}, select_all_trades_cb);
}

/**************************************
 *//**
 * @brief save new row behavior
 *************************************/
function save_new_trade_row_cb(response)
{
    process_response(response);
    update_trade_list();
}

/**************************************
 *//**
 * @brief save new row behavior
 *************************************/
function save_new_trade_row()
{
    console.log('save new row button clicked');
    // get form fields
   var trade_id = $(this).val();
    console.log('save row button clicked: ' + trade_id);
    // get form data
    var new_trade_name = $('#trade-name-new').val();
    var new_trade_type = 'test';
    var new_trade_location = $('#trade-location-new').val();
    var new_wayppoint_notes = $('#trade-notes-new').val();
    var new_start_date = $('#trade-start-date-new').val();
    var new_end_date = $('#trade-end-date-new').val();
    var data = {
        trade_name: new_trade_name,
        trade_type: new_trade_type,
        trade_location: new_trade_location,
        trade_notes: new_wayppoint_notes,
        trade_start_date: new_start_date,
        trade_end_date: new_end_date
    };
    send_request('create_trade', data, save_new_trade_row_cb);
}

/**************************************
 *//**
 * @brief generate a row for creating trades
 *************************************/
function gen_new_trade_row()
{
    return '<tr><td></td>' +
        '<td><input type="text" id="trade-name-new" ' +
        'value="" placeholder="trade name"></td>' +
        '<td><select id="trade-type-new"></select></td>' +
        '<td><input type="text" id="trade-location-new" ' +
        'value="" placeholder="trade location"></td>' +
        '<td><input type="text" id="trade-start-date-new" ' +
        'value="" placeholder="trade start date"></td>' +
        '<td><input type="text" id="trade-end-date-new" ' +
        'value="" placeholder="trade end date"></td>' +
        '<td><textarea id="trade-notes-new"></textarea></td>' +
        '<td>[TRADES]</td>' +
        '<td>[VOYAGE]</td>' +
        '<td><button id="expand-row-btn-new" class="btn">' +
        '<span class="glyphicon glyphicon-collapse-down"></span></button>' +
        '<button id="save-row-btn-new" value="new" class="btn">' +
        '<span class="glyphicon glyphicon-floppy-save"></span></button></td>' +
        '</tr>';
}

/**************************************
 *//**
 * @brief callback for update trades list request
 * expects trades list in the format
 * { message: "", data: { trades: [ { trade_id: 'trade_id',
 *  trade_name: 'trade_name' } ] }
 *************************************/
function update_trades_list_cb(response)
{
    process_response();
    console.log("update_trades_list_cb()");
    var trades = response.data.trades;
    var trades_list = $("#trade-list");
    var hdr_row = $('#trade-list-hdr-row');
    hdr_row.nextAll().remove();
    for (var i = 0; i < trades.length; i++) {
        var trade_row = (gen_trade_row(trades[i]));
        trades_list.append(trade_row);
        var trade_id = trades[i].trade_id;
        $('#save-row-btn-'+trade_id).click(save_trade_row);
        $('#select-row-'+trade_id).click(trade_select_change);
    }
    var new_trade_row = gen_new_trade_row();
    trades_list.append(new_trade_row);
    $('#save-row-btn-new').click(save_new_trade_row);
}

/**************************************
 *//**
 * @brief request update to trades list
 *************************************/
function update_trade_list()
{
    console.log("update_trade_list()");
    send_request("get_trades", {}, update_trades_list_cb);
}

/**************************************
 *//**
 * @brief set the status bar text field.
 *************************************/
function set_trades_status_bar(msg)
{
    var status_bar = $("#status-bar");
    status_bar.empty();
    status_bar.append('<span>' + msg + '</span');
}

/**************************************
 *//**
 * @brief deselect all selected trades
 *************************************/
function deselect_all_trades()
{
    console.log('deselect_all_trades');
    console.log('selected trades ids before: "%s"', selected_trade_ids);
    selected_trade_ids = [];
    $('.select-trade-row').prop('checked', false);
    console.log('selected trade ids after: "%s"', selected_trade_ids);
}

/**************************************
 *//**
 * @brief confirm deleting trades
 *************************************/
function confirm_delete_trades()
{
    $('#confirm-delete-trade-modal').modal();
}

/**************************************
 *//**
 * @brief delete trades callback
 *************************************/
function delete_trades_cb(response)
{
    process_response(response);
    update_trade_list();
    deselect_all_trades();
}

/**************************************
 *//**
 * @brief delete selected trades
 *************************************/
function delete_trades()
{
    var in_data = {trades_to_delete_ids: selected_trade_ids};
    send_request('delete_trades_by_id', in_data, delete_trades_cb);
}

/**************************************
 *//**
 * @brief set up the client-side UI and other freatures.
 *************************************/
$(document).ready(function()
{
    update_trade_list();
    $('#select-all-trades-btn').click(select_all_trades);
    $('#deselect-all-trades-btn').click(deselect_all_trades);
    $('#delete-trade-btn').click(confirm_delete_trades);
    $('#confirm-delete-trade-btn').click(delete_trades);
});