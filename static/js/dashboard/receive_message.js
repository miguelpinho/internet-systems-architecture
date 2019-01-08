// This file handles things related with receiving messages with the message queue

function scrollToBottom () {
    //Selectors
    let messages = jQuery("#messages");
    let newMessage = messages.children("li:last-child");
    //Heights
    let clientHeight = messages.prop("clientHeight");
    let scrollTop = messages.prop("scrollTop");
    let scrollHeight = messages.prop("scrollHeight");
    let newMessageHeight = newMessage.innerHeight();
    let lastMessageHeight = newMessage.prev().innerHeight();

    if (clientHeight + scrollTop + newMessageHeight + lastMessageHeight >= scrollHeight) {
    messages.scrollTop(scrollHeight);
    }
}

function display_message(message) {
    var template = $("#message-template").html();
    var html = Mustache.render(template, {
        text: message.text,
        createdAt: message.time,
        from: message.from
    });
    jQuery("#messages").append(html);
    scrollToBottom();
}

function config_receive_message(location_callback, nearby_callback, send_msg_callback) {
    // Socket.io connection

    socket.on('connect', () => {
        socket.emit('handshake', {data: getCookie("x-auth")});
    });

    socket.on("handshake_allowed", (message)=> {
        console.log("handshake success")
        location_callback(nearby_callback)
        send_msg_callback()
    })

    socket.on("user:incoming", (message) =>{
        console.log("User Message Received: "+message)
        display_message(message);
    });

    socket.on("bot:incoming", (message) =>{
        console.log("Bot Message Received: "+message)
        display_message(message);
    });

    socket.on("disconnect", ()=>{
        console.log("Disconnected from the io server");
        user_location_status = LOCATION_ERR;
        clearInterval(nearby_interval);
        clearInterval(location_timer_code);
        confirm("User not authenticated, please login first!\nYou will be redirected to the home page.");
        location.href = "/";
    })

    socket.on("error", (e)=>{
        console.log("Error: " + e["error"]);
    })
}