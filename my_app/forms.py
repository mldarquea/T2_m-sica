from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
class ArtistForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired(),
                            Length(min = 1, max = 50)])
    age = IntegerField('Age', validators = [DataRequired()])

    def validate_name(self, name):
        artist = Artist.query.filter_by(name = name.data).first()
        if artist:
            raise ValidationError('That name is taken, add another artist')