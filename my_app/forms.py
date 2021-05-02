from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, ValidationError
from my_app.models import Artist, Album, Song
class ArtistForm(FlaskForm):
    name = StringField('name', validators = [DataRequired(),
                            Length(min = 1, max = 50)])
    age = IntegerField('age', validators = [DataRequired()])

class AlbumForm(FlaskForm):
    name = StringField('name', validators = [DataRequired(),
                            Length(min = 1, max = 50)])
    genre = StringField('genre', validators = [DataRequired(),
                            Length(min = 1, max = 20)])
class SongForm(FlaskForm):
    name = StringField('name', validators = [DataRequired(),
                            Length(min = 1, max = 50)])
    duration = FloatField('duration', validators = [DataRequired()])