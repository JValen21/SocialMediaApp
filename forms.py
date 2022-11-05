from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')

class CreateAccountForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    repeatPassword = PasswordField('Repeat-Password')
    submit = SubmitField('Submit')