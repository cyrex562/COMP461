/*******************************************************************************
 *//**
 * @file voyages.js
 * @brief primary client-side javascript script file for JVWA
 * @author Josh Madden <cyrex562@gmail.com>
 * @copyright Josh Madden 2014
 ******************************************************************************/
/*******************************************************************************
 * GLOBALS
 ******************************************************************************/
var selected_voyage_ids = [];

/*******************************************************************************
 * FUNCTIONS
 ******************************************************************************/
/**************************************
 *//**
 * @brief save existing row behavior callback
 *************************************/
function save_voyage_row_cb(response)
{
    process_response(response);
    update_voyage_list();
    set_status_bar(response.msg);
}

/**************************************
 *//**
 * @brief save existing row behavior
 *************************************/
function save_voyage_row()
{
    var voyage_id = $(this).val();
    console.log('save row button clicked: ' + voyage_id);
    // get form data
    var updated_voyage_id = voyage_id;
    var updated_voyage_name = $('#voyage-name-' + voyage_id).val();
    var updated_voyage_notes = $('#voyage-notes-' + voyage_id).val();
    var data = { updated_voyage_id: updated_voyage_id,
        updated_voyage_name: updated_voyage_name,
        updated_voyage_notes: updated_voyage_notes};
    send_request('update_voyage', data, save_voyage_row_cb);
}

/**************************************
 *//**
 * @brief Check if voyage id is in the list of selected ids.
 *************************************/
function voy_id_in_sel_ids(voy_id)
{
    var result = -1;
    for (var i = 0; i < selected_voyage_ids.length; i++) {
        if (selected_voyage_ids[i] === voy_id) {
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
function voyage_select_change()
{
//    var raw_id = $(this).id;
    var voyage_id = $(this).val();
    console.log('voyage select toggled');
    console.log('selected voyage ids before: "%s"', selected_voyage_ids);
    var idx = voy_id_in_sel_ids(voyage_id);
    if (idx > -1) {
        selected_voyage_ids.splice(idx, 1);
        console.log('removing');
    } else {
        selected_voyage_ids.push(voyage_id);
        console.log('pushing');
    }
    console.log('selected voyage ids after: "%s"', selected_voyage_ids);
}

//function clear_ship_form() {
//    $('#ship-name-input').val('');
//    $('#ship-flag-input').val('');
//    $('#ship-captain-input').val('');
//    $('#ship-notes-textarea').val('');
//}
//
//function get_ship_by_id() {
//    var ship = '';
//    send_request('get_ship_by_id', {}, function() {
//       process_response(response);
//       set_status_bar(response.msg);
//       ship = response.data.ship;
//    });
//    return ship;
//}

//function edit_ship() {
//    $('#ship-form-action').val('edit');
//    // populate ship form
//    var ship_id = $(this).val();
//    var ship = get_ship_by_id();
//    $('#ship-name-input').val(ship.ship_name);
//    $('#ship-flag-input').val(ship.ship_flag);
//    $('#ship-captain-input').val(ship.ship_captain);
//    $('#ship-notes-textarea').val(ship.ship_notes);
//    $('#ship-id').val(ship_id);
//}
//
//function delete_ship() {
//
//}
//
//function create_ship() {
//    $('#ship-form-action').val('create');
//}
//
//function save_ship() {
//    var form_action = $('#ship-form-action').val();
//    var request_action =  '';
//    var in_data = {};
//    if (form_action === 'create') {
//
//    } else if (form_action === 'edit') {
//        in_data = {
//            ship_id: $('#ship-id').val(),
//            ship_name: $('#ship-name-input').val(),
//            ship_captain: $('#ship-captain-input').val(),
//            ship_notes: $('#ship-notes-textarea').val()
//        };
//        send_request(request_action, in_data)
//    }
//}


/**************************************
 *//**
 * @brief generate a row for a voyage
 *************************************/
function gen_voyage_row(voyage)
{
    var row = '<tr>' +
        '<td><input type="checkbox" ' +
        'id="select-row-[VOYAGE_ID]" value="[VOYAGE_ID]" ' +
        'class="select-voyage-row"></td>' +
        '<td><input type="text" ' +
        'id="voyage-name-[VOYAGE_ID]" value="[VOYAGE_NAME]"></td>' +
        '<td><textarea id="voyage-notes-[VOYAGE_ID]">[VOYAGE_NOTES]' +
        '</textarea></td>' +
        '<td>' +
        '<span>[SHIP_NAME]</span>' +
        '<button id="edit-ship-btn-[VOYAGE_ID]" value="[VOYAGE_ID]">' +
        '<span class="glyphicon glyphicon-pencil"></span>' +
        '</button>' +
        '</td>' +
        '<td>[VOYAGE_WAYPOINTS]</td>' +
        '<td>' +
            '<button id="expand-row-btn-[VOYAGE_ID]" class="btn">' +
        '<span class="glyphicon glyphicon-collapse-down"></span></button>' +
            '<button id="save-row-btn-[VOYAGE_ID]" ' +
        'class="btn" value="[VOYAGE_ID]"><span ' +
        'class="glyphicon glyphicon-floppy-save"></span></button>' +
        '</td>' +
        '</tr>';
    row = row.replace(/\[VOYAGE_ID\]/g, voyage.voyage_id);
    row = row.replace(/\[VOYAGE_NAME\]/g, voyage.voyage_name);
    row = row.replace(/\[VOYAGE_NOTES]/g, voyage.voyage_notes);
    // TODO: handle ship
    // TODO: handle waypoint
    return row;
}

/**************************************
 *//**
 * @brief process response from server containing voyage ids. add them all to the selection list and then toggle the state of all checkboxes to checked.
 *************************************/
function select_all_voyages_cb(response)
{
    process_response(response);
    var msg = response.message;
    set_status_bar(msg);
    selected_voyage_ids = response.data.voyage_ids;
    for (var i = 0; i < selected_voyage_ids.length; i++) {
       $('#select-row-'+selected_voyage_ids[i]).prop('checked', true);
    }
}

/**************************************
 *//**
 * @brief select all voyages; send a request for all voyage ids to the server.
 *************************************/
function select_all_voyages()
{
    send_request('get_all_voyage_ids', {}, select_all_voyages_cb);
}

/**************************************
 *//**
 * @brief save new row behavior
 *************************************/
function save_new_voyage_row_cb(response)
{
    process_response(response);
    update_voyage_list();
}

/**************************************
 *//**
 * @brief save new row behavior
 *************************************/
function save_new_voyage_row()
{
    console.log('save new row button clicked');
    // get form fields
    var new_voyage_name = $('#voyage-name-new').val();
    var new_voyage_notes = $('#voyage-notes-new').val();
    var data = {
        new_voyage_name: new_voyage_name,
        new_voyage_notes: new_voyage_notes
    };
    send_request('create_voyage', data, save_new_voyage_row_cb);
}

/**************************************
 *//**
 * @brief generate a row for creating voyages
 *************************************/
function gen_new_voyage_row()
{
    return '<tr>' +
        '<td></td>' +
        '<td><input type="text" ' +
        'id="voyage-name-new" value="" placeholder="voyage name"></td>' +
        '<td><textarea id="voyage-notes-new"></textarea></td>' +
        '<td><span>[VOYAGE_SHIP]</span></td>' +
        '<td>[VOYAGE_WAYPOINTS]</td>' +
        '<td>' +
        '<button id="expand-row-btn-new" class="btn"><span class="glyphicon ' +
        'glyphicon-collapse-down"></span></button>' +
        '<button id="save-row-new-btn" class="btn"><span class="glyphicon ' +
        'glyphicon-floppy-save"></span></button>' +
        '</td>' +
        '</tr>';
}

/**************************************
 *//**
 * @brief callback for update voyages list request
 * expects voyages list in the format
 * { message: "", data: { voyages: [ { voyage_id: 'voyage_id',
 *  voyage_name: 'voyage_name' } ] }
 *************************************/
function update_voyages_list_cb(response)
{
    process_response();
    console.log("update_voyages_list_cb()");
    var voyages = response.data.voyages;
    var voyages_list = $("#voyage-list");
    var hdr_row = $('#voyage-list-hdr-row');
    hdr_row.nextAll().remove();
    for (var i = 0; i < voyages.length; i++) {
        var voy_row = (gen_voyage_row(voyages[i]));
        voyages_list.append(voy_row);
        var voyage_id = voyages[i].voyage_id;
        $('#save-row-btn-'+voyage_id).click(save_voyage_row);
        $('#select-row-'+voyage_id).click(voyage_select_change);
    }
    var new_voy_row = gen_new_voyage_row();
    voyages_list.append(new_voy_row);
    $('#save-row-new-btn').click(save_new_voyage_row);
}

/**************************************
 *//**
 * @brief request update to voyages list
 *************************************/
function update_voyage_list()
{
    console.log("update_voyage_list()");
    send_request("get_voyages", {}, update_voyages_list_cb);
}

/**************************************
 *//**
 * @brief set the status bar text field.
 *************************************/
function set_voyages_status_bar(msg)
{
    var status_bar = $("#status-bar");
    status_bar.empty();
    status_bar.append('<span>' + msg + '</span');
}

/**************************************
 *//**
 * @brief deselect all selected voyages
 *************************************/
function deselect_all_voyages()
{
    console.log('deselect_all_voyages');
    console.log('selected voyage ids before: "%s"', selected_voyage_ids);
    selected_voyage_ids = [];
    $('.select-voyage-row').prop('checked', false);
    console.log('selected voyage ids after: "%s"', selected_voyage_ids);
}

/**************************************
 *//**
 * @brief confirm deleting voyages
 *************************************/
function confirm_delete_voyages()
{
    $('#confirm-delete-voyage-modal').modal();
}

/**************************************
 *//**
 * @brief delete voyages callback
 *************************************/
function delete_voyages_cb(response)
{
    process_response(response);
    update_voyage_list();
    deselect_all_voyages();
}

/**************************************
 *//**
 * @brief delete selected voyages
 *************************************/
function delete_voyages()
{
    var in_data = {voyages_to_delete_ids: selected_voyage_ids};
    send_request('delete_voyages_by_id', in_data, delete_voyages_cb);
}

/**************************************
 *//**
 * @brief set up the client-side UI and other freatures.
 *************************************/
$(document).ready(function()
{
    update_voyage_list();
    $('#select-all-voyages-btn').click(select_all_voyages);
    $('#deselect-all-voyages-btn').click(deselect_all_voyages);
    $('#delete-voyage-btn').click(confirm_delete_voyages);
    $('#confirm-delete-voyage-btn').click(delete_voyages);
});

/*******************************************************************************
 * END OF FILE
 ******************************************************************************/