from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from my_app.models import Artist
import base64
class ArtistForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired(),
                            Length(min = 1, max = 50)])
    id = StringField('id', validators = [DataRequired(),
                            Length(min = 1, max = 50)])
    age = IntegerField('Age', validators = [DataRequired()])
    #id = base64.b64encode(name.encode('ascii')).decode('ascii')
    # if len(id) > 22:
    #     id = id[0:21]

    def validate_name(self, name):
        artist = Artist.query.filter_by(name = name.data).first()
        if artist:
            raise ValidationError('That name is taken, add another artist')