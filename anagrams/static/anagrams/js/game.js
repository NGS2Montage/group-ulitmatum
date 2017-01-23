

// var socket = new WebSocket("ws://" + window.location.host + "/chat/");
// socket.onmessage = function(e) {
//     // alert(e.data);
//     console.log('socket.onmessage', e);
// }
// socket.onopen = function() {
//     var message = {
//         type: 'chat',
//         text: "hello world"
//     };
//     socket.send(JSON.stringify(message));
// }
// // Call onopen directly if socket is already open
// if (socket.readyState == WebSocket.OPEN) {
//     socket.onopen();
// }
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
