$(document).ready( () => {
    config_nearby();
    config_location();
    config_send_message();
    config_receive_message();
});


// TODO: Change socket.on to handler called (timer) function
// socket.on("updateRoomName", function (roomName) {
//   jQuery("#people_room").text(roomName);
// });

// TODO: Change socket.on to handler called (timer) function
// socket.on("updateUserList", function (users) {
//   let ul = jQuery("<ul></ul>");
//
//   users.forEach(function (user) {
//     ul.append(jQuery("<li></li>").text(user));
//   });
//
//   jQuery("#users").html(ul);
// });

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

