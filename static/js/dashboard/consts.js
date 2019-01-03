const NEARBY_REFRESH_TIMEOUT = 10000;
const LOCATION_REFRESH_TIMEOUT = 10000;

const LOCATION_ENDPOINT = "/api/user/location";
const POSTMSG_ENDPOINT = "/api/user/messages";
const GETNRBY_ENDPOINT = "/api/user/nearby";

const CONTENT_JSON = "application/json";

let user_location_status = false;
let location_timer_code = -1;
const LOCATION_NO = 0;
const LOCATION_YES = 2;
const LOCATION_TRY = 1;

let socket; //Unified socket handler