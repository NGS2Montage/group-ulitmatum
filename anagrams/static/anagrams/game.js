var app = {
    user: {
        name: USERNAME, // from template
        pk: USERPK, // from template
        letters: [],
    },
    friends: [],
    chats: [],
    subscribed: false,
    letters: {},
    saveLetters: function (letters) {
        letters.forEach(function (letter) {
            app.letters[letter.pk] = letter;
        });
    }
}



//////////////////////////////////////////////////////////////
// LetterTransaction
//////////////////////////////////////////////////////////////
function LetterTransaction(obj) {
    this.letter = obj.letter;
    this.pk = obj.pk;
    this.borrower = obj.borrower;
}

LetterTransaction.prototype.approve = function (event, model) {
    msg = {
      stream: "lettertransactions",
      payload: {
        action: "update",
        data: {
            pk: model.pk,
            approved: true,
        }
      }
    };

    socket.send(JSON.stringify(msg));
}

LetterTransaction.prototype.toString = function () {
    return this.letter.toString();
};

//////////////////////////////////////////////////////////////
// UserLetter
//////////////////////////////////////////////////////////////
function UserLetter(obj) {
    this.letter = obj.letter;
    this.pk = obj.pk;
    this.user = obj.user;
}

UserLetter.prototype.requestLetter = function (event, model) {
    msg = {
      stream: "lettertransactions",
      payload: {
        action: "create",
        data: {
            borrower: app.user.pk,
            letter: model.letter.pk
        }
      }
    };

    socket.send(JSON.stringify(msg));
};

UserLetter.prototype.toString = function () {
    return this.letter;
};


//////////////////////////////////////////////////////////////
// rivets init
//////////////////////////////////////////////////////////////
rivets.bind(document.getElementById('app-view'), {app: app});

// var app = {
//     friends: [],
//     chats: [],
//     user: {
//         name: "",
//         letters: [],
//         requests: [],
//         pk: 1,
//     },
//     newChat: "",
//     letters: [],
//     sendChat: function (event, model) {
//         socket.sendJSON({
//             type: "chat",
//             message: app.newChat,
//         });
//         app.newChat = "";
//     },
//     requestLetter: function (event, model) {
//         model.letter.request();
//     },
//     approveRequest: function (event, model) {
//         model.request.approve();
//     },
//     ownsLetter: function (letter, user) {
//         return user ;
//     },
// };

// //////////////////////////////////////////////////////////////
// // RemoteLetter
// //////////////////////////////////////////////////////////////
// function RemoteLetter(letter, owner) {
//     this.letter = letter;
//     this.owner = owner;
//     this.requested = false;
//     this.received = false;
// };

// RemoteLetter.prototype.toString = function () {
//     return this.letter;
// };

// RemoteLetter.prototype.request = function () {
//     if (this.requested) {
//         console.log(this.letter, "is already requested from", this.owner, " - ignoring");
//         return false;
//     }
//     this.requested = true; // This is optimistic, server might tell us this is illegal...
//     var message = {
//         type: "request-letter",
//         from_user: this.owner,
//         letter: this.letter
//     };
//     socket.sendJSON(message);
//     return true;
// };

// rivets.formatters.letterRequest = function(remoteLetter){
//     return remoteLetter.letter + " from " + remoteLetter.owner;
// };

// //////////////////////////////////////////////////////////////
// // LetterRequest
// //////////////////////////////////////////////////////////////
// function LetterRequest(letter, requester) {
//     this.letter = letter;
//     this.requester = requester;
//     this.approved = false;
// };

// LetterRequest.prototype.approve = function () {
//     var message = {
//         type: "request-approved",
//         letter: this.letter,
//         requester: this.requester,
//     };
//     socket.sendJSON(message);

//     // Remove this request from the page
//     app.user.requests.splice(app.user.requests.indexOf(this), 1);
// }

// rivets.formatters.requestedLetter = function(letterRequest){
//     return letterRequest.letter + " by " + letterRequest.requester;
// };


// //////////////////////////////////////////////////////////////
// // UserLetter
// //////////////////////////////////////////////////////////////
// function UserLetter(obj) {
//     for (key in obj) {
//         this[key] = obj[key];
//     }
// }

// UserLetter.prototype.request = function () {
//     console.log("NEED TO MAKE A LETTERTRANSACTION FOR THIS USERLETTER as long as it's not mine");
// };

// UserLetter.prototype.toString = function () {
//     return this.letter;
// };


//////////////////////////////////////////////////////////////
// Friend
//////////////////////////////////////////////////////////////
function Friend(friend) {
    this.name = friend.username;
    this.pk = friend.pk;
    this.letters = [];
    this.transactions = [];
    // = friend.letters.map(function (letter) {
    //     var el = new RemoteLetter(letter, friend.name);
    //     app.letters.push(el);
    //     return el;
    // });
};

Friend.prototype.addTransaction = function (transaction) {
    this.transactions.push(transaction);
};

// //////////////////////////////////////////////////////////////
// // rivets init
// //////////////////////////////////////////////////////////////
// rivets.bind(document.getElementById('app-view'), {app: app});

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

    console.log("IN (" + message.stream + ")", message.payload);

    if (message.stream === 'friends') {
        if (message.payload.action === 'list') {
            app.friends = message.payload.data.map(function (friend) {
                return new Friend(friend.friend);
            });

            var msg = {
              stream: "userletters",
              payload: {
                action: "list",
                data: {}
              }
            };
            socket.send(JSON.stringify(msg));
        }
    }

    if (message.stream === "lettertransactions") {
        if (message.payload.action === 'create') {
            message.payload.data.letter = app.letters[message.payload.data.letter];

            if (message.payload.data.borrower !== app.user.pk) {
                friend = app.friends.find(function (friend) {
                    return friend.pk === message.payload.data.borrower;
                });
                friend.addTransaction(new LetterTransaction(message.payload.data));
            } else {
                console.log("Need to show that we requested this and are waiting for approval");
            }
            // app.transactions.push(new LetterTransaction(message.payload.data));
        }
    }

    if (message.stream === 'userletters') {
        if (message.payload.action === 'list') {
            app.user.letters = message.payload.data.filter(function (letter) {
                return letter.user === app.user.pk;
            }).map(function (letter) {
                return new UserLetter(letter);
            });
            app.saveLetters(app.user.letters);

            app.friends.forEach(function (friend) {
                friend.letters = message.payload.data.filter(function (letter) {
                    return letter.user === friend.pk;
                }).map(function (letter) {
                    return new UserLetter(letter);
                });
                app.saveLetters(friend.letters)
            });

            if (!app.subscribed) {
                app.subscribed = true;

                var msg = {
                  stream: "lettertransactions",
                  payload: {
                    action: "subscribe",
                    data: {
                        action: "create"
                    }
                  }
                };
                socket.send(JSON.stringify(msg));

                var msg = {
                  stream: "lettertransactions",
                  payload: {
                    action: "subscribe",
                    data: {
                        action: "update"
                    }
                  }
                };
                socket.send(JSON.stringify(msg));

                var msg = {
                  stream: "lettertransactions",
                  payload: {
                    action: "subscribe",
                    data: {
                        action: "delete"
                    }
                  }
                };
                socket.send(JSON.stringify(msg));
            }
        }
    }

    // var msg = {
    //   stream: "userletters",
    //   payload: {
    //     action: "list",
    //     data: {}
    //   }
    // };

    // socket.send(JSON.stringify(msg));

    // msg = {
    //   stream: "lettertransactions",
    //   payload: {
    //     action: "list",
    //     data: {}
    //   }
    // };

    // socket.send(JSON.stringify(msg));


    // message = message.payload;

    // if (message.type === "chat") {
    //     app.chats.push(message);
    // }
    // if (message.type === "init-game") {
    //     app.user.name = message.username;
    //     app.user.letters = message.letters;
    //     app.friends = message.friends.map(function (friend) {
    //         return new Friend(friend);
    //     });
    // }
    // if (message.type === "request-letter") {
    //     if (!message.legal) {
    //         var illegalRequest = app.letters.find(function (letter) {
    //             return letter.owner === message.from_user && letter.letter === message.letter;
    //         });
    //         illegalRequest.requested = false;
    //     }
    // }
    // if (message.type === "letter-requested") {
    //     if (app.user.letters.includes(message['letter'])) {
    //         app.user.requests.push(new LetterRequest(message['letter'], message['by_user']));
    //     }
    // }
    // if (message.type === "request-approved") {
    //     var remoteLetter = app.letters.find(function (letter) {
    //         return letter.letter === message.letter && letter.owner === message.lender;
    //     });
    //     remoteLetter.requested = false;
    //     remoteLetter.received = true;
    // }
}

socket.onopen = function() {
    // socket.sendJSON({
    //     type: "chat",
    //     message: "Hello world chat"
    // });

    // socket.sendJSON({
    //     type: "init-game"
    // });

    var msg = {
      stream: "friends",
      payload: {
        action: "list",
        data: {}
      }
    };
    socket.send(JSON.stringify(msg));


}
// Call onopen directly if socket is already open
if (socket.readyState == WebSocket.OPEN) socket.onopen();
