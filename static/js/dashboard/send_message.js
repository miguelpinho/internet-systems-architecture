// This file handles things related with sending messages with ajax (or eventually message queue)

function handle_send_message(e) {

  let input_box = $("#send_message_input")[0];

  let message = input_box.value;

  //Clean Input Box
  input_box.value = "";

  console.log(message)

  // TODO: Instead of using socket.emit, use ajax
  // socket.emit("createMessage", {
  //   text: jQuery("[name=message]").val()
  // }, function () {
  //   jQuery("[name=message]").val("");
  // });
}


function config_send_message(){
    $("#send_message_button").on("click", handle_send_message);
    $("#send_message_input").on("keydown",(e)=>{
        if(e.key === "Enter"){
            handle_send_message(e)
        }
    });
}
