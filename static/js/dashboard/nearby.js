// This file handles things related with nearby users fetch and display

function refresh_nearby() {

}

function config_nearby() {
    // Configure timer that each X time refreshes the nearby users
    setInterval(refresh_nearby, NEARBY_REFRESH_TIMEOUT);
}
