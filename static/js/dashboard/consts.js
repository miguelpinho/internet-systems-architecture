const NEARBY_REFRESH_TIMEOUT = 60000;
const LOCATION_REFRESH_TIMEOUT = 30000;

const LOCATION_ENDPOINT = "/api/user/location";
const POSTMSG_ENDPOINT = "/api/user/messages";
const GETNRBY_ENDPOINT = "/api/user/nearby";

const CONTENT_JSON = "application/json";

const LOCATION_ERR = -1;
const LOCATION_NO = 0;
const LOCATION_TRY = 1;
const LOCATION_YES = 2;
let user_location_status = LOCATION_NO;
let location_timer_code = -1;

const NEARBY_ALREADY_CONFIGURED = 1;
const NEARBY_ERR = -1;
const NEARBY_NO = 0;
const NEARBY_TRY = 1;
const NEARBY_YES = 2;
let nearby_config = 0;
let nearby_status = 0;
let nearby_interval;

let socket; //Unified socket handler