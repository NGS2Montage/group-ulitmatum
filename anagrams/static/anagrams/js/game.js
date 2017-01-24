
var socket;

function getConnected() {
    socket = new WebSocket("ws://" + window.location.host + "/anagrams");
    socket.onmessage = function(e) {
        console.log(e);
    }
    socket.onopen = function() {
        socket.send("hello world");
    }
    // Call onopen directly if socket is already open
    if (socket.readyState == WebSocket.OPEN) socket.onopen();
}
