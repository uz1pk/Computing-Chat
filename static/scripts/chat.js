document.addEventListener('DOMContentLoaded', () => {
    let message = document.querySelector('#user-message');
    message.addEventListener('keyup', event => {
        if (event.keyCode == 13) { // 13 keycode == enter key
            document.querySelector('#send-message').click();
        }
    });
});