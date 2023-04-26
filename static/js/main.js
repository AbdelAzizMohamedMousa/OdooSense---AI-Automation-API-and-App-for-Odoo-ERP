$(document).ready(function() {
    var socket = io();
    $('form').submit(function() {
        var message = $('#message').val();
        $('#message').val('');
        $('.chat-history').append('<div class="chat-message"><strong>You:</strong> ' + message + '</div>');
        socket.emit('message', message);
        return false;
    });
    socket.on('response', function(response) {
        $('.chat-history').append('<div class="chat-message"><strong>OdooSense:</strong> ' + response + '</div>');
    });
});