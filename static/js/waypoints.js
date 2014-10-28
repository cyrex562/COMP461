/**
 * @file waypoints.js
 * @brief javascript source file for
 */
/*******************************************************************************
 * GLOBALS
 ******************************************************************************/
var selected_waypoint_ids = [];
var waypoint_types = [];
var trade_items = [];


/*******************************************************************************
 * FUNCTIONS
 ******************************************************************************/
/**
 * @brief save existing row behavior callback
 */
function save_waypoint_row_cb(response) {
    process_response(response);
    update_waypoint_list();
    set_waypoints_status_bar(response.msg);
}

/**
 * @brief save existing row behavior
 */
function save_waypoint_row() {
    var waypoint_id = $(this).val();
    console.log('save row button clicked: ' + waypoint_id);
    // get form data
    var updated_waypoint_id = waypoint_id;
    var updated_waypoint_name = $('#waypoint-name-' + waypoint_id).val();
    var updated_waypoint_type = 'test';
    var updated_waypoint_location = $('#waypoint-location-' + waypoint_id).val();
    var updated_wayppoint_notes = $('#waypoint-notes-' + waypoint_id).val();
    var updated_start_date = $('#waypoint-start-date-' + waypoint_id).val();
    var updated_end_date = $('#waypoint-end-date-' + waypoint_id).val();
    var data = { updated_waypoint_id: updated_waypoint_id,
        updated_waypoint_name: updated_waypoint_name,
        updated_waypoint_type: updated_waypoint_type,
        updated_waypoint_location: updated_waypoint_location,
        updated_waypoint_notes: updated_wayppoint_notes,
        updated_waypoint_start_date: updated_start_date,
        updated_waypoint_end_date: updated_end_date };
    send_request('update_waypoint', data, save_waypoint_row_cb);
}

/**
 * @brief Check if waypoint id is in the list of selected ids.
 */
function waypoint_id_in_sel_ids(waypoint_id) {
    var result = -1;
    for (var i = 0; i < selected_waypoint_ids.length; i++) {
        if (selected_waypoint_ids[i] === waypoint_id) {
            result = i;
            break;
        }
    }
    return result;
}

/**
 * @brief selection toggle for checkbox
 */
function waypoint_select_change() {
    var waypoint_id = $(this).val();
    console.log('waypoint select toggled');
    console.log('selected waypoint ids before: "%s"', selected_waypoint_ids);
    var idx = waypoint_id_in_sel_ids(waypoint_id);
    if (idx > -1) {
        selected_waypoint_ids.splice(idx, 1);
        console.log('removing');
    } else {
        selected_waypoint_ids.push(waypoint_id);
        console.log('pushing');
    }
    console.log('selected waypoint ids after: "%s"', selected_waypoint_ids);
}

/**
 * @brief generate a row for a waypoint
 */
function gen_waypoint_row(waypoint) {
    var row = '<tr>' +
        '<td></td>' +
        '<td>[VOYAGE]</td>' +
        '<td><input type="text" id="waypoint-name-[WAYPOINT_ID]" ' +
            'value="[WAYPOINT_NAME]"></td>' +
        '<td><select id="waypoint-type-[WAYPOINT_ID]"></select></td>' +
        '<td><input type="text" id="waypoint-location-[WAYPOINT_ID]" ' +
        'value="[WAYPOINT_LOCATION]" placeholder="waypoint location"></td>' +
        '<td><input type="text" id="waypoint-start-date-[WAYPOINT_ID]" ' +
        'value="[WAYPOINT_START_DATE]" placeholder="waypoint start date">' +
        '</td>' +
        '<td><input type="text" id="waypoint-end-date-[WAYPOINT_ID]" ' +
        'value="[WAYPOINT_END_DATE]" placeholder="waypoint end date"></td>' +
        '<td>[TRADES]</td>' +
        '<td><textarea id="waypoint-notes-[WAYPOINT_ID]">' +
        '[WAYPOINT_NOTES]</textarea></td>' +
        '<td><button id="expand-row-btn-[WAYPOINT_ID]" class="btn">' +
        '<span class="glyphicon glyphicon-collapse-down"></span></button>' +
        '<button id="save-row-btn-[WAYPOINT_ID]" value="[WAYPOINT_ID]" ' +
        'class="btn">' +
        '<span class="glyphicon glyphicon-floppy-save"></span></button></td>' +
        '</tr>';

    row = row.replace(/\[WAYPOINT_ID\]/g, waypoint.waypoint_id);
    row = row.replace(/\[WAYPOINT_LOCATION\]/g, waypoint.waypoint_location);
    row = row.replace(/\[WAYPOINT_START_DATE\]/g, waypoint.start_date);
    row = row.replace(/\[WAYPOINT_END_DATE\]/g, waypoint.end_date);
    row = row.replace(/\[WAYPOINT_NOTES]/g, waypoint.waypoint_notes);
    row = row.replace(/\[WAYPOINT_NAME]/g, waypoint.waypoint_name);
    // waypoint type

    // trade
    return row;
}

/**
 * @brief process response from server containing waypoint ids. add them all to the selection list and then toggle the state of all checkboxes to checked.
 */
function select_all_waypoints_cb(response) {
    process_response(response);
    var msg = response.message;
    set_waypoints_status_bar(msg);
    selected_waypoint_ids = response.data.waypoint_ids;
    for (var i = 0; i < selected_waypoint_ids.length; i++) {
        $('#select-row-' + selected_waypoint_ids[i]).prop('checked', true);
    }
}

/**
 * @brief select all waypoints; send a request for all waypoint ids to the server.
 */
function select_all_waypoints() {
    send_request('get_all_waypoint_ids', {}, select_all_waypoints_cb);
}

/**
 * @brief save new row behavior
 */
function save_new_waypoint_row_cb(response) {
    process_response(response);
    update_waypoint_list();
}

/**
 * @brief save new row behavior
 */
function save_new_waypoint_row() {
    console.log('save new row button clicked');
    // get form fields
    var waypoint_id = $(this).val();
    console.log('save row button clicked: ' + waypoint_id);
    // get form data
    var new_waypoint_name = $('#waypoint-name-new').val();
    var new_waypoint_type = 'test';
    var new_waypoint_location = $('#waypoint-location-new').val();
    var new_wayppoint_notes = $('#waypoint-notes-new').val();
    var new_start_date = $('#waypoint-start-date-new').val();
    var new_end_date = $('#waypoint-end-date-new').val();
    var data = {
        waypoint_name: new_waypoint_name,
        waypoint_type: new_waypoint_type,
        waypoint_location: new_waypoint_location,
        waypoint_notes: new_wayppoint_notes,
        waypoint_start_date: new_start_date,
        waypoint_end_date: new_end_date
    };
    send_request('create_waypoint', data, save_new_waypoint_row_cb);
}

/**
 * @brief generate a row for creating waypoints
 */
function gen_new_waypoint_row() {
    return '<tr><td></td>' +
        '<td><input type="text" id="waypoint-name-new" ' +
        'value="" placeholder="waypoint name"></td>' +
        '<td><select id="waypoint-type-new"></select></td>' +
        '<td><input type="text" id="waypoint-location-new" ' +
        'value="" placeholder="waypoint location"></td>' +
        '<td><input type="text" id="waypoint-start-date-new" ' +
        'value="" placeholder="waypoint start date"></td>' +
        '<td><input type="text" id="waypoint-end-date-new" ' +
        'value="" placeholder="waypoint end date"></td>' +
        '<td><textarea id="waypoint-notes-new"></textarea></td>' +
        '<td>[TRADES]</td>' +
        '<td>[VOYAGE]</td>' +
        '<td><button id="expand-row-btn-new" class="btn">' +
        '<span class="glyphicon glyphicon-collapse-down"></span></button>' +
        '<button id="save-row-btn-new" value="new" class="btn">' +
        '<span class="glyphicon glyphicon-floppy-save"></span></button></td>' +
        '</tr>';
}

/**
 * @brief callback for update waypoints list request
 * expects waypoints list in the format
 * { message: "", data: { waypoints: [ { waypoint_id: 'waypoint_id',
 *  waypoint_name: 'waypoint_name' } ] }
 */
function update_waypoints_list_cb(response) {
    process_response();
    console.log("update_waypoints_list_cb()");
    var waypoints = response.data.waypoints;
    var waypoints_list = $("#waypoint-list");
    var hdr_row = $('#waypoint-list-hdr-row');
    hdr_row.nextAll().remove();
    for (var i = 0; i < waypoints.length; i++) {
        var waypoint_row = (gen_waypoint_row(waypoints[i]));
        waypoints_list.append(waypoint_row);
        var waypoint_id = waypoints[i].waypoint_id;
        $('#save-row-btn-' + waypoint_id).click(save_waypoint_row);
        $('#select-row-' + waypoint_id).click(waypoint_select_change);
    }
    var new_waypoint_row = gen_new_waypoint_row();
    waypoints_list.append(new_waypoint_row);
    $('#save-row-btn-new').click(save_new_waypoint_row);
}

/**
 * @brief request update to waypoints list
 */
function update_waypoint_list() {
    console.log("update_waypoint_list()");
    send_request("get_waypoints", {}, update_waypoints_list_cb);
}

/**
 * @brief set the status bar text field.
 */
function set_waypoints_status_bar(msg) {
    var status_bar = $("#status-bar");
    status_bar.empty();
    status_bar.append('<span>' + msg + '</span');
}

/**
 * @brief deselect all selected waypoints
 */
function deselect_all_waypoints() {
    console.log('deselect_all_waypoints');
    console.log('selected waypoints ids before: "%s"', selected_waypoint_ids);
    selected_waypoint_ids = [];
    $('.select-waypoint-row').prop('checked', false);
    console.log('selected waypoint ids after: "%s"', selected_waypoint_ids);
}

/**
 * @brief confirm deleting waypoints
 */
function confirm_delete_waypoints() {
    $('#confirm-delete-waypoint-modal').modal();
}

/**
 * @brief delete waypoints callback
 */
function delete_waypoints_cb(response) {
    process_response(response);
    update_waypoint_list();
    deselect_all_waypoints();
}

/**
 * @brief delete selected waypoints
 */
function delete_waypoints() {
    var in_data = {waypoints_to_delete_ids: selected_waypoint_ids};
    send_request('delete_waypoints_by_id', in_data, delete_waypoints_cb);
}

/**
 * @brief set up the client-side UI and other freatures.
 */
$(document).ready(function () {
    update_waypoint_list();
    $('#select-all-waypoints-btn').click(select_all_waypoints);
    $('#deselect-all-waypoints-btn').click(deselect_all_waypoints);
    $('#delete-waypoint-btn').click(confirm_delete_waypoints);
    $('#confirm-delete-waypoint-btn').click(delete_waypoints);
});

/*******************************************************************************
 * END OF FILE
 ******************************************************************************/