from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from passlib.hash import pbkdf2_sha256
from wtform_fields import *
from models import *

# Configurations
app = Flask(__name__)
app.secret_key = 'MUST REPLACE'  #REPLACE SECRET KEY

# Database setup (REQWRITE KEY FOR PUBLICATION)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://qfdtdkunaroicj:c3d36f692efe24709974488ec30f5158d0b22cdf18eb470e854867cc2094f3bd@ec2-52-21-136-176.compute-1.amazonaws.com:5432/dcfco3jf2ii5bc'
db = SQLAlchemy(app)

login = LoginManager(app)
login.init_app(app)

@login.user_loader  
def load_user(id):
    return User.query.get(int(id))

@app.route("/", methods=['GET', 'POST']) # Default route
def index():
    user_reg_form = RegistrationForm() # instanciate class for form imported from our wtform_field.py
    
    if user_reg_form.validate_on_submit(): # trigger validators to check form request and if input parameters are valid
        current_username = user_reg_form.username.data
        current_password = user_reg_form.password.data

        hash_password = pbkdf2_sha256.hash(current_password)
        
        cur_user = User(username = current_username, password = hash_password)
        db.session.add(cur_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("index.html", form = user_reg_form) # render the page



# Route for login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    user_login_form = UserLoginForm()
    
    if user_login_form.validate_on_submit():
        cur_user = User.query.filter_by(username = user_login_form.username.data).first()
        login_user(cur_user)
        return redirect(url_for('chat'))

    return render_template("login.html", form = user_login_form)



@app.route("/chat", methods=['GET', 'POST'])
def chat():
    if not current_user.is_authenticated:
        return "Must login before using chat"

    return "Welcome to chat"



@app.route("/logout", methods=['GET'])
def logout():
    logout_user()
    return "Successfully Logged Out"



# host server on local IP
if __name__ == "__main__":
    app.run(debug = True)
