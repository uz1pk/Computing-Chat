from socket import socket
from time import localtime, strftime
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from passlib.hash import pbkdf2_sha256
from wtform_fields import *
from models import *

# Configurations
app = Flask(__name__)
app.secret_key = 'MUST REPLACE'  #REPLACE SECRET KEY

# Database setup (REQWRITE KEY FOR PUBLICATION)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://qfdtdkunaroicj:c3d36f692efe24709974488ec30f5158d0b22cdf18eb470e854867cc2094f3bd@ec2-52-21-136-176.compute-1.amazonaws.com:5432/dcfco3jf2ii5bc'
db = SQLAlchemy(app)

socketio = SocketIO(app)
CHATROOMS = ["courses", "coop", "resume", "stand-up", "other"]

login = LoginManager(app)
login.init_app(app)

@login.user_loader  
def load_user(id):
    return User.query.get(int(id))

# Route for login page
@app.route("/", methods=['GET', 'POST'])
def index():

    user_login_form = UserLoginForm()
    
    if user_login_form.validate_on_submit():
        cur_user = User.query.filter_by(username = user_login_form.username.data).first()
        login_user(cur_user)
        return redirect(url_for('chat'))

    return render_template("login.html", form = user_login_form)


@app.route("/register", methods=['GET', 'POST']) # Default route
def register():

    user_reg_form = RegistrationForm()
    
    if user_reg_form.validate_on_submit():
        current_username = user_reg_form.username.data
        current_password = user_reg_form.password.data

        hash_password = pbkdf2_sha256.hash(current_password) # hash password before adding to DB
        
        cur_user = User(username = current_username, password = hash_password)
        db.session.add(cur_user)
        db.session.commit() # add the users data to the DB

        flash('Registered Successfully')
        return redirect(url_for('index'))

    return render_template("index.html", form = user_reg_form)


@app.route("/chat", methods=['GET', 'POST'])
def chat():

    if not current_user.is_authenticated:
        flash('Must be logged in before accessing chat')
        return redirect(url_for('index'))

    user_room_add = AddRoomForm()

    if user_room_add.validate_on_submit():
        new_room = user_room_add.roomname.data
        if new_room.lower() not in CHATROOMS:
            CHATROOMS.append(new_room)

    return render_template('main.html', username=current_user.username, form = user_room_add, rooms=CHATROOMS)


@app.route("/logout", methods=['GET'])
def logout():
    logout_user()

    flash('Logout successful')
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@socketio.on('incoming-message')
def on_message(data):

    message = data["message"]
    username = data["username"]
    time = strftime('%b-%d %I:%M%p', localtime())

    send({"username": username, "message": message, "time": time}, room=data["room"])


@socketio.on('join')
def join(data):

    join_room(data['room'])
    send({'message': data['username'] + " has joined " + data['room']}, room=data['room'])


@socketio.on('leave')
def leave(data):

    leave_room(data['room'])
    send({'message': data['username'] + " has left the room"}, room=data['room'])


if __name__ == "__main__":
    socketio.run(app, debug = True)
