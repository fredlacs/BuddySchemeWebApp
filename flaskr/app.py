import basic as db
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from forms import LoginForm, RegistrationForm
import json
from permissions import permissioned_login_required
from werkzeug.security import generate_password_hash, check_password_hash
from auth_token import verify_token
import requests
from user import User
from werkzeug.security import check_password_hash, generate_password_hash
from emailer import send_email, send_email_confirmation_to_user
import controllers.adminctrl as adminctrl
import controllers.loginctrl as loginctrl
import controllers.mentorctrl as mentorctrl
import controllers.menteectrl as menteectrl
import logging


app = Flask(__name__)
app.config["SECRET_KEY"]="powerful secretkey"
# app.config["SECURITY_PASSWORD_SALT"]=53
app.config["EMAIL_CONFIRMATION_EXPIRATION"] = 86400
app.config["SECRET_KEY"] = "powerful secretkey"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login.login"

app.register_blueprint(adminctrl.admin_blueprint)
app.register_blueprint(loginctrl.login_blueprint)
app.register_blueprint(mentorctrl.mentor_blueprint)
app.register_blueprint(menteectrl.mentee_blueprint)

log = logging.getLogger(__name__)


@login_manager.user_loader
def load_user(id):
    user = User(id)
    return user

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")



# We only need this for local dev
if __name__ == '__main__':
    app.run(debug=True)
