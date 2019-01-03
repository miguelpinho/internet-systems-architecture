// This file handles things related with nearby users fetch and display

function refresh_nearby() {
    $.ajax({
        type: "GET",
        url: GETNRBY_ENDPOINT,
        success: (data, status, jqXHR)=>{
            console.log("Message Response received to GETNRBY: "+data);
            // Update UI with the nearby users
            var ul = $("<ul></ul>");
            users.forEach(function (user) {
                ul.append($("<li></li>").text(user));
            });
            $("#users").html(ul);
        },
        error: (jqXHR, textStatus, errorThrown) =>{
          console.log("Error received to GETNRBY: "+textStatus);
        },
        dataType: CONTENT_JSON
    });
}

function config_nearby() {
    // Configure timer that each X time refreshes the nearby users
    setInterval(refresh_nearby, NEARBY_REFRESH_TIMEOUT);
}
