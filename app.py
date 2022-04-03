from flask import Flask, render_template
from wtform_fields import *

# Configurations
app = Flask(__name__)
app.secret_key = 'MUST REPLACE' 

@app.route("/", methods=['GET', 'POST']) # Default route
def index():

    user_reg_form = RegistrationForm() #instanciate class for form imported from our wtform_field.py
    
    if user_reg_form.validate_on_submit(): #trigger validators to check form request and if input parameters are valid
        return "Valid params"

    return render_template("index.html", form=user_reg_form) #render the page

if __name__ == "__main__": #host server on local IP
    app.run(debug = True)
