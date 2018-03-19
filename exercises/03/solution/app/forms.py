import os

from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, ValidationError


class LoginForm(Form):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Submit')

    @staticmethod
    def validate_username(form, field):
        if field.data != os.getenv('DMCF_USERNAME'):
            raise ValidationError('That username is not correct.')

    @staticmethod
    def validate_password(form, field):
        if field.data != os.getenv('DMCF_PASSWORD'):
            raise ValidationError('That password is not correct.')
