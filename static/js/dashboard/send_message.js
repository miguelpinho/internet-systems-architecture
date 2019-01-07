// This file handles things related with sending messages with ajax (or eventually message queue)

function handle_send_message(e) {

  let input_box = $("#send_message_input")[0];
  let message = input_box.value;
  let slider = $("#radius_range")[0];
  let radius = parseFloat(slider.value)/10000;
  //Clean Input Box
  input_box.value = "";

  console.log("Sending: " + message);

  $.ajax({
      type: "POST",
      url: POSTMSG_ENDPOINT,
      data: JSON.stringify({message:message, radius:radius}),
      contentType: "application/json",
      success: (data, status, jqXHR)=>{
          console.log("Message Response received to POSTMSG: "+data);
          //Update UI with the message content as a personal message
          display_message(data["Message"]);
      },
      error: (jqXHR, textStatus, errorThrown) =>{
          console.log("Error received to POSTMSG: "+textStatus+"  "+errorThrown);
          //TODO: Some type of alert to the user
      },
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
