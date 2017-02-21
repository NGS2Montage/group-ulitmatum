var app = {
    friends: [],
    chats: [],
    user: {
        name: "",
        letters: [],
        requests: [],
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
    approveRequest: function (event, model) {
        model.request.approve();
    }
};

//////////////////////////////////////////////////////////////
// RemoteLetter
//////////////////////////////////////////////////////////////
function RemoteLetter(letter, owner) {
    this.letter = letter;
    this.owner = owner;
    this.requested = false;
    this.received = false;
};

RemoteLetter.prototype.toString = function () {
    return this.letter;
};

RemoteLetter.prototype.request = function () {
    if (this.requested) {
        console.log(this.letter, "is already requested from", this.owner, " - ignoring");
        return false;
    }
    this.requested = true; // This is optimistic, server might tell us this is illegal...
    var message = {
        type: "request-letter",
        from_user: this.owner,
        letter: this.letter
    };
    socket.sendJSON(message);
    return true;
};

rivets.formatters.letterRequest = function(remoteLetter){
    return remoteLetter.letter + " from " + remoteLetter.owner;
};

//////////////////////////////////////////////////////////////
// LetterRequest
//////////////////////////////////////////////////////////////
function LetterRequest(letter, requester) {
    this.letter = letter;
    this.requester = requester;
    this.approved = false;
};

LetterRequest.prototype.approve = function () {
    var message = {
        type: "request-approved",
        letter: this.letter,
        requester: this.requester,
    };
    socket.sendJSON(message);

    // Remove this request from the page
    app.user.requests.splice(app.user.requests.indexOf(this), 1);
}

rivets.formatters.requestedLetter = function(letterRequest){
    return letterRequest.letter + " by " + letterRequest.requester;
};


//////////////////////////////////////////////////////////////
// Friend
//////////////////////////////////////////////////////////////
function Friend(friend) {
    this.name = friend.name;
    this.letters = friend.letters.map(function (letter) {
        var el = new RemoteLetter(letter, friend.name);
        app.letters.push(el);
        return el;
    });
};

rivets.bind(document.getElementById('app-view'), {app: app});

//////////////////////////////////////////////////////////////
// WebSocket
//////////////////////////////////////////////////////////////
socket = new WebSocket("ws://" + window.location.host + "/anagrams/");
socket.sendJSON = function (message) {
    console.log("OUT", message);
    socket.send(JSON.stringify({
        stream: 'anagrams',
        payload: message
    }));
}

socket.onmessage = function(e) {
    try {
        var message = JSON.parse(e.data);
    } catch (exc) {
        console.error("Unexpected string from server", e.data);
    }

    console.log("IN", message);
    message = message.payload;
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
    if (message.type === "request-letter") {
        if (!message.legal) {
            var illegalRequest = app.letters.find(function (letter) {
                return letter.owner === message.from_user && letter.letter === message.letter;
            });
            illegalRequest.requested = false;
        }
    }
    if (message.type === "letter-requested") {
        if (app.user.letters.includes(message['letter'])) {
            app.user.requests.push(new LetterRequest(message['letter'], message['by_user']));
        }
    }
    if (message.type === "request-approved") {
        var remoteLetter = app.letters.find(function (letter) {
            return letter.letter === message.letter && letter.owner === message.lender;
        });
        remoteLetter.requested = false;
        remoteLetter.received = true;
    }
}

socket.onopen = function() {
    // socket.sendJSON({
    //     type: "chat",
    //     message: "Hello world chat"
    // });

    socket.sendJSON({
        type: "init-game"
    });

    var msg = {
      stream: "userletter",
      payload: {
        action: "list",
        data: {}
      }
    };

    socket.send(JSON.stringify(msg));

    msg = {
      stream: "lettertransaction",
      payload: {
        action: "list",
        data: {}
      }
    };

    socket.send(JSON.stringify(msg));
}
// Call onopen directly if socket is already open
if (socket.readyState == WebSocket.OPEN) socket.onopen();
