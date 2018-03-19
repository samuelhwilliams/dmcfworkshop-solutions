from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired


class LoginForm(Form):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Submit')


class CreateUserForm(Form):
    username = StringField('Username for new account', validators=[InputRequired()])
    password = PasswordField('Password for new account', validators=[InputRequired()])
    submit = SubmitField('Create account')
