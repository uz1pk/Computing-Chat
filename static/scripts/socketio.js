document.addEventListener('DOMContentLoaded', () => {
    // Initializing SocketIO
    var socket = io();

    let room = "courses";
    joinRoom(room);

    function leaveRoom(room) {
        socket.emit('leave', {'currUsername': username, 'room': room});
    }

    function joinRoom(room) {
        socket.emit('join', {'currUsername': username, 'room': room});
        document.querySelector('#display-message-section').innerHTML = '';
    }

    function printMessage(msg) {
        const paragraph = document.createElement('p');
        paragraph.innerHTML = msg;
        document.querySelector('#display-message-section').append(paragraph);
    }

    // Display user message
    socket.on('message', data => {
        const userParagraph = document.createElement('p');
        const usernameSpan = document.createElement('span');
        const currTime = document.createElement('span');
        const br = document.createElement('br');

        if (data.currUsername) {
            usernameSpan.innerHTML = data.currUsername;
            currTime.innerHTML = data.time;
            userParagraph.innerHTML = usernameSpan.outerHTML + br.outerHTML + data.currMessage + br.outerHTML + currTime.outerHTML + br.outerHTML;
        }
        else {
            printMessage(data.currMessage);
        }

        document.querySelector('#display-message-section').append(userParagraph);
    });

    // Sending messages
    document.querySelector('#send-message').onclick = () => {
        socket.send({'currMessage': document.querySelector('#user-message').value, 'currUsername': username, 'room': room });
        document.querySelector('#user-message').value = '';
    }

    // Selecting a room
    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let selectedRoom = p.innerHTML;
            if (selectedRoom == room) {
                message = `You are already in ${room}.`;
                printMessage(message);
            }
            else {
                leaveRoom(room);
                joinRoom(selectedRoom);
                room = selectedRoom;
            }
        }
    });
})
