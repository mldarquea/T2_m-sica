from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, ValidationError
from my_app.models import Artist, Album, Song
class ArtistForm(FlaskForm):
    name = StringField('name', validators = [DataRequired(),
                            Length(min = 1, max = 50)])
    age = IntegerField('age', validators = [DataRequired()])

    # def validate_name(self, name):
    #     artist = Artist.query.filter_by(name = name.data).first()
    #     if artist:
    #         raise ValidationError('That name is taken, add another artist')

class AlbumForm(FlaskForm):
    artist_id = StringField('artist_id', validators = [DataRequired(),
                            Length(min = 1, max = 50)])
    name = StringField('name', validators = [DataRequired(),
                            Length(min = 1, max = 50)])
    genre = StringField('genre', validators = [DataRequired(),
                            Length(min = 1, max = 20)])

    # def validate_name(self, name):
    #     album = Album.query.filter_by(name = name.data).first()
    #     if album:
    #         raise ValidationError('That name is taken, add another album')

class SongForm(FlaskForm):
    album_id = StringField('album_id', validators = [DataRequired(),
                            Length(min = 1, max = 50)])
    name = StringField('name', validators = [DataRequired(),
                            Length(min = 1, max = 50)])
    duration = FloatField('duration', validators = [DataRequired()])

    # def validate_name(self, name):
    #     artist = Artist.query.filter_by(name = name.data).first()
    #     if artist:
    #         raise ValidationError('That name is taken, add another artist')
