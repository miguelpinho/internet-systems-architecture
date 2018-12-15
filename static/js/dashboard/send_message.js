// This file handles things related with sending messages with ajax (or eventually message queue)

function handle_send_message(e) {

  let input_box = $("#send_message_input")[0];

  let message = input_box.value;

  //Clean Input Box
  input_box.value = "";

  console.log("Sending: " + message);

  $.ajax({
      type: "POST",
      url: POSTMSG_ENDPOINT,
      data: {message:message},
      success: (data, status, jqXHR)=>{
          console.log("Message Response received to POSTMSG: "+data);
          //Update UI with the message content as a personal message
          display_message(data["message"]);
      },
      error: (jqXHR, textStatus, errorThrown) =>{
          console.log("Error received to POSTMSG: "+textStatus);
          //TODO: Some type of alert to the user
      },
      dataType: CONTENT_JSON
    });
}


function config_send_message(){
    $("#send_message_button").on("click", handle_send_message);
    $("#send_message_input").on("keydown",(e)=>{
        if(e.key === "Enter"){
            handle_send_message(e)
        }
    });
}
