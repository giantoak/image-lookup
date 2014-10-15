$(document).ready(function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/gallery');
    console.log(socket);
    socket.on('result', function (msg) {
        console.log(msg);
    });
});
