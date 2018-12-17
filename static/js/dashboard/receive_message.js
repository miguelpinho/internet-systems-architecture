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

function config_receive_message() {
    //TODO: CONFIG MESSAGE_QUEUES
}