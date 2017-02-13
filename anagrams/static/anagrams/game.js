var app = {
    friends: [],
    chats: [],
    user: {
        name: "",
        letters: [],
    },
    newChat: "",
    letters: [],
    sendChat: function (event, model) {
        socket.sendJSON({
            type: "chat",
            message: app.newChat,
        });
        app.newChat = "";
    },
    requestLetter: function (event, model) {
        model.letter.request();
    },
};

//////////////////////////////////////////////////////////////
// Letter
//////////////////////////////////////////////////////////////
function Letter(letter, owner) {
    this.letter = letter;
    this.owner = owner;
    this.requested = false;
};

Letter.prototype.toString = function () {
    return this.letter;
};

Letter.prototype.request = function () {
    if (this.requested) {
        console.log(this.letter, "is already requested from", this.owner, " - ignoring");
        return false;
    }
    this.requested = true;
    var message = {
        type: "request-letter",
        from_user: this.owner,
        letter: this.letter
    };
    socket.sendJSON(message);
    return true;
};

rivets.formatters.letterRequest = function(letter){
  return letter.letter + " from " + letter.owner;
};


//////////////////////////////////////////////////////////////
// Friend
//////////////////////////////////////////////////////////////
function Friend(friend) {
    this.name = friend.name;
    this.letters = friend.letters.map(function (letter) {
        var el = new Letter(letter, friend.name);
        app.letters.push(el);
        return el;
    });
};

rivets.bind(document.getElementById('app-view'), {app: app});

//////////////////////////////////////////////////////////////
// WebSocket
//////////////////////////////////////////////////////////////
socket = new WebSocket("ws://" + window.location.host + "/anagrams");
socket.sendJSON = function (message) {
    console.log("OUT", message);
    socket.send(JSON.stringify(message));
}

socket.onmessage = function(e) {
    try {
        var message = JSON.parse(e.data);
    } catch (exc) {
        console.error("Unexpected string from server", e.data);
    }

    console.log("IN", message);

    if (message.type === "chat") {
        app.chats.push(message);
    }
    if (message.type === "init-game") {
        app.user.name = message.username;
        app.user.letters = message.letters;
        app.friends = message.friends.map(function (friend) {
            return new Friend(friend);
        });
    }
}

socket.onopen = function() {
    socket.sendJSON({
        type: "chat",
        message: "Hello world chat"
    });

    socket.sendJSON({
        type: "init-game"
    });
}
// Call onopen directly if socket is already open
if (socket.readyState == WebSocket.OPEN) socket.onopen();
