from my_app import db
from sqlalchemy.ext.hybrid import hybrid_property

class Artist(db.Model):
    id = db.Column(db.String(22), primary_key=True) 
    name = db.Column(db.String(50), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    albums_url =  db.Column(db.String(150), unique=True)
    tracks_url = db.Column(db.String(150), unique=True)
    self_url =  db.Column(db.String(150), unique=True)
    albums = db.relationship("Album", lazy=True, backref="recorded")
     
    def __repr__(self):
        return f"id: '{self.id}', name:'{self.name}', '{self.age}', '{self.albums_url}', '{self.tracks_url}', '{self.self_url}'"

class Album(db.Model):
    id = db.Column(db.String(22), primary_key=True)
    artist_id = db.Column(db.String(50), db.ForeignKey("artist.id"), nullable=False)#######
    name = db.Column(db.String(50), unique=True, nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    artist_url = db.Column(db.String(150), unique=True)
    tracks_url = db.Column(db.String(150), unique=True)
    self_url =  db.Column(db.String(150), unique=True)
    songs = db.relationship("Song", lazy=True, backref="included")
    
    # def __dict__(self):
    #     return {
    #         "id": self.id,
    #         "artist_id": self.artist_id, 
    #         "name": str(self.name),
    #         "genre": self.genre,
    #         "artist": self.artist_url,
    #         "tracks": self.tracks_url,
    #         "self": self.self_url
    #     }
        #return f"Album('{self.id}', '{self.artist_id}','{self.name}', '{self.genre}', '{self.artist_url}', '{self.tracks_url}', '{self.self_url}')"

class Song(db.Model):
    id = db.Column(db.String(22), primary_key=True)
    album_id = db.Column(db.String(22), db.ForeignKey("album.id"), nullable=False) #####################
    name = db.Column(db.String(50), unique=True, nullable=False)
    duration = db.Column(db.Float, nullable=False)
    times_played = db.Column(db.Integer, nullable=False)
    artist_url =  db.Column(db.String(150), unique=True)
    album_url =  db.Column(db.String(150), unique=True)
    self_url = db.Column(db.String(150), unique=True)

    def __repr__(self):
        return f"Song('{self.id}', '{self.album_id}', '{self.name}', '{self.duration}', '{self.times_played}', \
            '{self.artist_url}', '{self.album_url}', '{self.self_url}')"


# Run migrations
db.create_all()