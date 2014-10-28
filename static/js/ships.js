var selected_ship_ids = [];

/**************************************
 *//**
 * @brief save existing row behavior callback
 *************************************/
function save_ship_row_cb(response)
{
    process_response(response);
    update_ship_list();
    set_ships_status_bar(response.msg);
}

/**************************************
 *//**
 * @brief save existing row behavior
 *************************************/
function save_ship_row()
{
    var ship_id = $(this).val();
    console.log('save row button clicked: ' + ship_id);
    // get form data
    var updated_ship_id = ship_id;
    var updated_ship_name = $('#ship-name-' + ship_id).val();
    var updated_ship_notes = $('#ship-notes-' + ship_id).val();
    var updated_ship_captain = $('#ship-captain-' + ship_id).val();
    var updated_ship_flag = $('#ship-flag-' + ship_id).val();
    var data = { updated_ship_id: updated_ship_id,
        updated_ship_name: updated_ship_name,
        updated_ship_notes: updated_ship_notes,
        updated_ship_captain: updated_ship_captain,
        updated_ship_flag: updated_ship_flag};
    send_request('update_ship', data, save_ship_row_cb);
}

/**************************************
 *//**
 * @brief Check if ship id is in the list of selected ids.
 *************************************/
function ship_id_in_sel_ids(ship_id)
{
    var result = -1;
    for (var i = 0; i < selected_ship_ids.length; i++) {
        if (selected_ship_ids[i] === ship_id) {
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
function ship_select_change()
{
//    var raw_id = $(this).id;
    var ship_id = $(this).val();
    console.log('ship select toggled');
    console.log('selected ship ids before: "%s"', selected_ship_ids);
    var idx = ship_id_in_sel_ids(ship_id);
    if (idx > -1) {
        selected_ship_ids.splice(idx, 1);
        console.log('removing');
    } else {
        selected_ship_ids.push(ship_id);
        console.log('pushing');
    }
    console.log('selected ship ids after: "%s"', selected_ship_ids);
}

/**************************************
 *//**
 * @brief generate a row for a ship
 *************************************/
function gen_ship_row(ship)
{
    var row = '<tr><td><input type="checkbox" id="select-row-[SHIP_ID]" ' +
        'value="[SHIP_ID]" class="select-ship-row"></td>' +
        '<td><input type="text" id="ship-name-[SHIP_ID]" value="[SHIP_NAME]" ' +
        'placeholder="ship name"></td>' +
        '<td><input type="text" id="ship-captain-[SHIP_ID]" ' +
        'value="[SHIP_CAPTAIN]" ' +
        'placeholder="ship captain"></td>' +
        '<td><input type="text" id="ship-flag-[SHIP_ID]" value="[SHIP_FLAG]" ' +
        'placeholder="ship flag"></td>' +
        '<td><textarea id="ship-notes-[SHIP_ID]">[SHIP_NOTES]</textarea></td>' +
        '<td>[VOYAGE]</td>' +
        '<td><button id="expand-row-btn-[SHIP_ID]" class="btn">' +
        '<span class="glyphicon glyphicon-collapse-down"></span></button>' +
        '<button id="save-row-btn-[SHIP_ID]" value="[SHIP_ID]" class="btn">' +
        '<span class="glyphicon glyphicon-floppy-save"></span></button></td>' +
        '</tr>';

    row = row.replace(/\[SHIP_ID\]/g, ship.ship_id);
    row = row.replace(/\[SHIP_NAME\]/g, ship.ship_name);
    row = row.replace(/\[SHIP_CAPTAIN\]/g, ship.ship_captain);
    row = row.replace(/\[SHIP_FLAG\]/g, ship.ship_flag);
    row = row.replace(/\[SHIP_NOTES]/g, ship.ship_notes);
    // TODO: handle Voyages
    return row;
}

/**************************************
 *//**
 * @brief process response from server containing ship ids. add them all to the selection list and then toggle the state of all checkboxes to checked.
 *************************************/
function select_all_ships_cb(response)
{
    process_response(response);
    var msg = response.message;
    set_ships_status_bar(msg);
    selected_ship_ids = response.data.ship_ids;
    for (var i = 0; i < selected_ship_ids.length; i++) {
       $('#select-row-'+selected_ship_ids[i]).prop('checked', true);
    }
}

/**************************************
 *//**
 * @brief select all ships; send a request for all ship ids to the server.
 *************************************/
function select_all_ships()
{
    send_request('get_all_ship_ids', {}, select_all_ships_cb);
}

/**************************************
 *//**
 * @brief save new row behavior
 *************************************/
function save_new_ship_row_cb(response)
{
    process_response(response);
    update_ship_list();
}

/**************************************
 *//**
 * @brief save new row behavior
 *************************************/
function save_new_ship_row()
{
    console.log('save new row button clicked');
    // get form fields
    var new_ship_name = $('#ship-name-new').val();
    var new_ship_captain = $('#ship-captain-new').val();
    var new_ship_flag = $('#ship-flag-new').val();
    var new_ship_notes = $('#ship-notes-new').val();
    var data = {
        ship_name: new_ship_name,
        ship_notes: new_ship_notes,
        ship_flag: new_ship_flag,
        ship_captain: new_ship_captain
    };
    send_request('create_ship', data, save_new_ship_row_cb);
}

/**************************************
 *//**
 * @brief generate a row for creating ships
 *************************************/
function gen_new_ship_row()
{
    return '<tr><td></td>' +
        '<td><input type="text" ' +
        'id="ship-name-new" value="" placeholder="ship name"></td>' +
        '<td><input type="text" id="ship-captain-new" value="" ' +
        'placeholder="ship captain"></td>' +
        '<td><input type="text" id="ship-flag-new" value="" placeholder="ship flag"></td>' +
        '<td><textarea id="ship-notes-new"></textarea></td>' +
        '<td>[VOYAGE]</td>' +
        '<td><button id="expand-row-btn-new" class="btn">' +
        '<span class="glyphicon glyphicon-collapse-down"></span></button>' +
        '<button id="save-row-new-btn" class="btn">' +
        '<span class="glyphicon glyphicon-floppy-save"></span></button></td>' +
        '</tr>';
}

/**************************************
 *//**
 * @brief callback for update ships list request
 * expects ships list in the format
 * { message: "", data: { ships: [ { ship_id: 'ship_id',
 *  ship_name: 'ship_name' } ] }
 *************************************/
function update_ships_list_cb(response)
{
    process_response();
    console.log("update_ships_list_cb()");
    var ships = response.data.ships;
    var ships_list = $("#ship-list");
    var hdr_row = $('#ship-list-hdr-row');
    hdr_row.nextAll().remove();
    for (var i = 0; i < ships.length; i++) {
        var ship_row = (gen_ship_row(ships[i]));
        ships_list.append(ship_row);
        var ship_id = ships[i].ship_id;
        $('#save-row-btn-'+ship_id).click(save_ship_row);
        $('#select-row-'+ship_id).click(ship_select_change);
    }
    var new_ship_row = gen_new_ship_row();
    ships_list.append(new_ship_row);
    $('#save-row-new-btn').click(save_new_ship_row);
}

/**************************************
 *//**
 * @brief request update to ships list
 *************************************/
function update_ship_list()
{
    console.log("update_ship_list()");
    send_request("get_ships", {}, update_ships_list_cb);
}

/**************************************
 *//**
 * @brief set the status bar text field.
 *************************************/
function set_ships_status_bar(msg)
{
    var status_bar = $("#status-bar");
    status_bar.empty();
    status_bar.append('<span>' + msg + '</span');
}

/**************************************
 *//**
 * @brief deselect all selected ships
 *************************************/
function deselect_all_ships()
{
    console.log('deselect_all_ships');
    console.log('selected ships ids before: "%s"', selected_ship_ids);
    selected_ship_ids = [];
    $('.select-ship-row').prop('checked', false);
    console.log('selected ship ids after: "%s"', selected_ship_ids);
}

/**************************************
 *//**
 * @brief confirm deleting ships
 *************************************/
function confirm_delete_ships()
{
    $('#confirm-delete-ship-modal').modal();
}

/**************************************
 *//**
 * @brief delete ships callback
 *************************************/
function delete_ships_cb(response)
{
    process_response(response);
    update_ship_list();
    deselect_all_ships();
}

/**************************************
 *//**
 * @brief delete selected ships
 *************************************/
function delete_ships()
{
    var in_data = {ships_to_delete_ids: selected_ship_ids};
    send_request('delete_ships_by_id', in_data, delete_ships_cb);
}

/**************************************
 *//**
 * @brief set up the client-side UI and other freatures.
 *************************************/
$(document).ready(function()
{
    update_ship_list();
    $('#select-all-ships-btn').click(select_all_ships);
    $('#deselect-all-ships-btn').click(deselect_all_ships);
    $('#delete-ship-btn').click(confirm_delete_ships);
    $('#confirm-delete-ship-btn').click(delete_ships);
});