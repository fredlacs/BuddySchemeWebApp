from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    k_number = StringField('k-number', validators=[DataRequired(), Length(min=8, max=9)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    login_submit = SubmitField("Login")

class RegistrationForm(FlaskForm):
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    k_number = StringField('k-number', validators=[DataRequired(), Length(min=8, max=9)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo("password")])
    is_mentor = BooleanField('is_mentor')
    registration_submit = SubmitField("Sign Up")

class RequestPasswordResetForm(FlaskForm):
    k_number = StringField('k-number', validators=[DataRequired(), Length(min=8, max=9)])
    request_reset_password_submit = SubmitField("Send me an email")

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo("password")])
    reset_password_submit = SubmitField("Reset Password")
