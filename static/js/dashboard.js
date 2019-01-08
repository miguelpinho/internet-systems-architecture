$(document).ready( () => {
    socket = io.connect('https://' + document.domain + ':' + location.port, {secure: true});
    config_receive_message(config_location, config_nearby, config_send_message);
    token = getCookie("x-auth")
    console.log("User token: "+token)

    let slider = $("#radius_range")[0];
    let output = $("#radius")[0];
    output.innerHTML = `Radius [${slider.value}m]`; // Display the default slider value

    // Update the current slider value (each time you drag the slider handle)
    slider.oninput = function() {
      output.innerHTML = `Radius [${this.value}m]`;
      refresh_nearby()
    }

    let username = $("#username")[0];
    userid = getCookie("username")
    username.innerHTML = "User: " + userid
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

