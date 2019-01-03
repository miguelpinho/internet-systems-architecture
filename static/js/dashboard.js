$(document).ready( () => {
    socket = io.connect('http://' + document.domain + ':' + location.port);
    config_nearby();
    config_location();
    config_send_message();
    config_receive_message();
    token = getCookie("x-auth")
    console.log(token)
});

// TODO: Change socket.on to message queue
// socket.on("newMessage", function (message) {
//   let formattedTime = moment(message.createdAt).format("h:mm a");
//   let template = jQuery("#message-template").html();
//   let html = Mustache.render(template, {
//     text: message.text,
//     createdAt: formattedTime,
//     from: message.from
//   });
//
//   jQuery("#messages").append(html);
//   scrollToBottom();
//   // let formattedTime = moment(message.createdAt).format("h:mm a");
//   //
//   // let li = jQuery("<li></li>");
//   // li.text(`${message.from}=>${formattedTime}<=:${message.text}`);
//   //
//   // jQuery("#messages").append(li);
// });

