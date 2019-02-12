from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager
from forms import LoginForm, RegistrationForm
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
app.config["SECRET_KEY"]="powerful secretkey"

## TODO: refactor user into different file
class User(db.Model):
    id = db.Column(db.String(15), primary_key=True)
    password = db.Column(db.String(15))
    email = id + "@kcl.ac.uk"
    first_name = db.Column(db.String(15))
    last_name = db.Column(db.String(15))


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    registration_form = RegistrationForm(request.form)
    login_form = LoginForm(request.form)

    if registration_form.registration_submit.data: # if the registation form was submitted
        if registration_form.validate_on_submit(): # if the form was valid
            # hash the user password
            first_name = registration_form.first_name.data
            last_name = registration_form.last_name.data
            k_number = registration_form.k_number.data
            # hashed_password = generate_password_hash(registration_form.password.data)
            hashed_password = generate_password_hash("12345678", method="sha256")

            # store user data in database
            new_user = User(k_number=k_number, first_name=first_name, last_name=last_name, password=hashed_password)
            
            # db.session.add(new_user)
            # db.session.commit()

            app.logger.warning('registered')

            #redirect to profile page, where he must insert his preferences
            return redirect("/dashboard")
        else: # if the form was NOT valid
            # Flash the error message
            app.logger.warning('error registering')
            return render_template("login.html", registration_form=registration_form, login_form=login_form, sign_up_visible=True)

    if login_form.login_submit.data: # if the login form was submitted
        if login_form.validate_on_submit(): # if the form was valid
            # check if he is authorised
            ## TODO: get from db
            hashed_password = generate_password_hash("12345678", method="sha256")
            input_password = login_form.password.data
            if check_password_hash(hashed_password, input_password):
                # redirect to profile page, where he must insert his preferences
                app.logger.warning('logged in')
                return redirect("/dashboard")
            else:
                app.logger.warning('wrong password')
                return redirect("/login")
        else: # if the form was NOT valid
            # Flash the error message
            app.logger.warning('error logging in')
            return render_template("login.html", registration_form=registration_form, login_form=login_form)

    return render_template("login.html", registration_form=registration_form, login_form=login_form)


@app.route("/dashboard")
def dashboard():
    return redirect("/")


@app.route("/mentee/<k_number>")
def mentee(k_number):
    # ensure user is authenticated: the session is valid; the user is k_number

    # user_info = getMenteeData(k_number): Dictionary
            # Query database with k number to get the following fields:
                # k number: string
                # First Name: string
                # Last Name: string
                # Age: int
                # Hobbies: List[string]
                # Academic interests: List[string]
            # Format into dictionary
    user_info = {
        "k_number": "k1763763",
        "first_name": "Nicholas",
        "last_name": "Pezzotti",
        "age": 20,
        "hobbies": ["football", "poker"],
        "academic_interests": ["AI", "Blockchain"]
    }

    return render_template("user_screens/mentee_page.html", title="Your Profile", user_info=user_info)

# We only need this for local dev
if __name__ == '__main__':
    app.run(debug=True, port=5000)
