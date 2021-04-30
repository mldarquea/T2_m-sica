from my_app import db
import base64
from sqlalchemy.ext.hybrid import hybrid_property

class Artist(db.Model):
    id = db.Column(db.String(22), unique=True, nullable=False) #, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    albums = db.relationship("Album", lazy=True, backref="recorded")
    #codificar_nombre = base64.b64encode(self.name.encode('ascii'))
    
    # def id_str(self):
    #     casi_encoded = base64.b64encode(self.name.encode('ascii'))
    #     self.id = casi_encoded.decode('ascii')
    #     if len(id) > 22:
    #         self.id = id[:21]
    #     return id 

    def __repr__(self):
        return f"Artist('{self.id}', '{self.name}', '{self.age}')"

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"), nullable=False)
    songs = db.relationship("Song", lazy=True, backref="included")
    
    def __repr__(self):
        return f"Album('{self.id}', '{self.name}', '{self.genre}')"

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    duration = db.Column(db.Float, nullable=False)
    times_played = db.Column(db.Integer, nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey("album.id"), nullable=False)

    def __repr__(self):
        return f"Song('{self.id}', '{self.name}', '{self.duration}', '{self.times_played}')"


# Run migrations
db.create_all()
