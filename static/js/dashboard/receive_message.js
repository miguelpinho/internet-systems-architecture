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

function config_receive_message() {

}