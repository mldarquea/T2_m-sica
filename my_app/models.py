from my_app import db

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    albums = db.relationship("Album", lazy=True, backref="recorded")

    def __repr__(self):
        return f"Artist('{self.id}', '{self.name}', '{self.age}')"

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"), nullable=False)

    def __repr__(self):
        return f"Album('{self.id}', '{self.name}', '{self.genre}')"


# Run migrations
db.create_all()
