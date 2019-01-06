// This file handles things related with location, radius and building

function getLocation() {
    console.log("Update request for location")
    if (navigator.geolocation) {
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
            location = LOCATION_NO;
            clearInterval(location_timer_code);
        });
    } else {
        console.log("Geolocation is not supported by this browser.");
        location = LOCATION_NO;
        clearInterval(location_timer_code);
    }
}

function get_location_success(position) {
    let lat = position.coords.latitude;
    let lon = position.coords.longitude;
    let json_body = JSON.stringify({"body":{lat,lon}});

    socket.emit("building_change", json_body)
    user_location_status = LOCATION_TRY;
}


function refresh_location() {
    if(user_location_status !== LOCATION_TRY &&
        user_location_status !== LOCATION_ERR )
            getLocation()
}

function config_location(nearby_callback) {
    socket.on("building_change_success",(body)=>{
        console.log("Location Updated")
        if(body["success"] === "yes"){
            // Configure nearby only after location is set
            nearby_callback();
            jQuery("#people_room").text(body["building"]);
            user_location_status = LOCATION_YES;
        }
        else {
            user_location_status = LOCATION_NO;
            console.log("Error in building change")
        }

    });
    refresh_location();
    location_timer_code = setInterval(refresh_location, LOCATION_REFRESH_TIMEOUT);
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