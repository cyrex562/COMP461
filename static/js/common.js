/*******************************************************************************
 *//**
 * @file common.js
 * @brief common javascript code for the whole we app
 * @author Josh Madden <cyrex562@gmail.com>
 * @copyright Josh Madden 2014
 ******************************************************************************/
/*******************************************************************************
 * GLOBALS
 ******************************************************************************/
/*******************************************************************************
 * FUNCTIONS
 ******************************************************************************/
/**************************************
 *//**
 * @brief send a request to the server.
 * @param action the action reuqested
 * @param request_data the data to be prcessed/required by the request.
 * @param callback the callback to call on success.
 *************************************/
function send_request(action, request_data, callback)
{
    $.ajax({
        type : "POST",
        url : $SCRIPT_ROOT + "/" + action,
        data : JSON.stringify({action: action, params: request_data},
            null, '\t'),
        contentType : "application/json; charset=UTF-8",
        success : callback,
        error : function(request, status, error) {
            console.log("AJAX request failed: action: {0}, " +
                "request_data: {1}, callback: {2}, status: {3}, request: " +
                "{4}, error: {5}", action, request_data, callback, status,
                request, error);
        }
    });
}

/**************************************
 *//**
 * @brief stuff always done when an AJAX request response is received.
 *************************************/
function process_response(response)
{
    console.log('process_response');
    console.log('response: %s', response);
}

/*******************************************************************************
 * END OF FILE
 ******************************************************************************/
