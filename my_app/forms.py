from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(),
                            Length(min = 2, max = 20)])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password =PasswordField('Confirm Password',
                            validators = [DataRequired(), EqualTo('password')])
    register = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
