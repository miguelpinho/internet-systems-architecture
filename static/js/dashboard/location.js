// This file handles things related with location, radius and building

function getLocation() {
    if (navigator.geolocation) {
        console.log("Asked for current postition");
        navigator.geolocation.getCurrentPosition(get_location_success, (error) => {
            switch(error.code) {
                case error.PERMISSION_DENIED:
                    console.log("User denied the request for Geolocation.");
                    break;
                case error.POSITION_UNAVAILABLE:
                    console.log("Location information is unavailable.");
                    break;
                case error.TIMEOUT:
                    console.log("The request to get user location timed out.");
                    break;
                default :
                    console.log("An unknown error occurred.");
            }
            location_error_dialog(error.message);
        });
    } else {
        console.log("Geolocation is not supported by this browser.");
        location_error_dialog("Geolocation is not supported by this browser.");
    }
}

function get_location_success(position) {
    let lat = position.coords.latitude;
    let lon = position.coords.longitude;
    let json_body = JSON.stringify({lat,lon});

    let oReq = new XMLHttpRequest(); // New ajax request

    oReq.addEventListener("load", () => {
        try {
            let response = JSON.parse(oReq.responseText);
            console.log(response);
            // TODO: Get Building from response, add it to UI
            //   jQuery("#people_room").text(roomName);
        }
        catch (e) {
            console.log("Could not handle location post request response");
            // Condition user intentions due to no location, or use the last location it had
            // Send alert
            location_error_dialog("Could not handle server respose.")
        }
    });

    oReq.open("POST", LOCATION_ENDPOINT);
    oReq.setRequestHeader("Content-type", "application/json; charset=UTF-8");
    oReq.send(json_body);
}


function refresh_location() {
    // TODO: Try to minimize unnecessary requests, or just remove this
    getLocation()
}

function config_location() {
    refresh_location();
    setInterval(refresh_location, LOCATION_REFRESH_TIMEOUT);
}

function location_error_dialog(message) {
    let new_dialog = $("#dialogs");
    new_dialog.dialog({
        resizable:false,
        draggable: false,
        modal: true,
        title: "Confirmation",
        open: function() {
            var markup = message;
            $(this).html(markup);
            },
        buttons: {
            Ok: function() {
            $( this ).dialog( "close" );
            }
        }
    });
}