// This file handles things related with nearby users fetch and display

function refresh_nearby() {
    if (nearby_status != NEARBY_TRY){
        console.log("Update request for nearby users")
        let slider = $("#radius_range")[0];
        let radius = parseInt(slider.value);
        $.ajax({
            type: "GET",
            data: {radius:radius},
            url: GETNRBY_ENDPOINT,
            success: (data, status, jqXHR)=>{
                // Update UI with the nearby users
                users = data["users"]
                var ul = $("<ul></ul>");
                if(Array.isArray(users)){
                    users.forEach(function (user) {
                        ul.append($("<li></li>").text(user));
                    });
                }
                $("#users").html(ul);
                nearby_status = NEARBY_YES;
                console.log("Nearby Users Updated")
            },
            error: (jqXHR, textStatus, errorThrown) =>{
              console.log("Error received to GETNRBY: "+textStatus);
              nearby_status = NEARBY_ERR;
            }
        });
        nearby_status = NEARBY_TRY;
    }
}

function config_nearby() {
    // Configure timer that each X time refreshes the nearby users
    if (nearby_config !== NEARBY_ALREADY_CONFIGURED) {
        refresh_nearby();
        nearby_interval = setInterval(refresh_nearby, NEARBY_REFRESH_TIMEOUT);
        nearby_config = NEARBY_ALREADY_CONFIGURED;
    }
}
