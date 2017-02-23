var app = {
    user: {},
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
app.user = new User({
    username: USERNAME, // from template
    pk: USERPK, // from template
});


//////////////////////////////////////////////////////////////
// LetterTransaction
//////////////////////////////////////////////////////////////
function LetterTransaction(obj) {
    this.letter = obj.letter;
    this.pk = obj.pk;
    this.borrower = obj.borrower;
    this.approved = ('approved' in obj) ? obj.approved : false;
}

LetterTransaction.prototype.approve = function (event, model) {
    msg = {
      stream: "lettertransactions",
      payload: {
        action: "update",
        pk: model.transaction.pk,
        data: {
            borrower: model.transaction.borrower,
            letter: model.transaction.letter.pk,
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
function UserLetter(obj, username) {
    this.letter = obj.letter;
    this.pk = obj.pk;
    this.user = username;
}

UserLetter.prototype.requestLetter = function (event, model) {
    var existingTransaction = app.user.transactions.find(function (transaction) {
        return (transaction.letter.pk === model.letter.pk);
    });

    if (existingTransaction) {
        console.log("There is already a request for " + model.letter);
    } else {
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
    }
};

UserLetter.prototype.toString = function () {
    return this.letter;
};


//////////////////////////////////////////////////////////////
// rivets init
//////////////////////////////////////////////////////////////
rivets.bind(document.getElementById('app-view'), {app: app});


//////////////////////////////////////////////////////////////
// User
//////////////////////////////////////////////////////////////
function User(user) {
    this.name = user.username;
    this.pk = user.pk;
    this.letters = [];
    this.transactions = [];
};

User.prototype.addTransaction = function (transaction) {
    this.transactions.push(transaction);
};

User.prototype.updateTransaction = function (transaction) {
    var index = this.transactions.findIndex(function (t) {
        return t.pk === transaction.pk;
    });
    if (index != -1) {
        this.transactions.splice(index, 1, transaction);
    } else {
        console.error(this.name + " has no such transaction " + transaction);
    }
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
                return new User(friend.friend);
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
        if (message.payload.action === 'create' && !('response_status' in message.payload)) {
            message.payload.data.letter = app.letters[message.payload.data.letter];

            var transactingUser = null;
            if (message.payload.data.borrower !== app.user.pk) {
                transactingUser = app.friends.find(function (friend) {
                    return friend.pk === message.payload.data.borrower;
                });
            } else {
                transactingUser = app.user;
            }

            if (transactingUser != null) {
                transactingUser.addTransaction(new LetterTransaction(message.payload.data));
            } else {
                console.error("No user with pk ", message.payload.data.borrower);
            }
        }
        if (message.payload.action === 'update' && !('response_status' in message.payload)) {
            message.payload.data.letter = app.letters[message.payload.data.letter];

            var transactingUser = null;
            if (message.payload.data.borrower !== app.user.pk) {
                var transactingUser = app.friends.find(function (friend) {
                    return friend.pk === message.payload.data.borrower;
                });
            } else {
                transactingUser = app.user;
            }

            if (transactingUser != null) {
                transactingUser.updateTransaction(new LetterTransaction(message.payload.data));
            } else {
                console.error("No user with pk ", message.payload.data.borrower);
            }
        }
    }

    if (message.stream === 'userletters') {
        if (message.payload.action === 'list') {
            app.user.letters = message.payload.data.filter(function (letter) {
                return letter.user === app.user.pk;
            }).map(function (letter) {
                return new UserLetter(letter, app.user.name);
            });
            app.saveLetters(app.user.letters);

            app.friends.forEach(function (friend) {
                friend.letters = message.payload.data.filter(function (letter) {
                    return letter.user === friend.pk;
                }).map(function (letter) {
                    return new UserLetter(letter, friend.name);
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
}

socket.onopen = function() {

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
