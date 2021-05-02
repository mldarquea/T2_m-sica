from my_app import app, db
from flask import render_template, jsonify, redirect, url_for
from my_app.models import Artist, Album, Song
from my_app.forms import ArtistForm, AlbumForm, SongForm
from flask_restful import Api, Resource, reqparse, abort
import base64

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/artists', methods=["GET", "POST"])
def artists():
    form = ArtistForm(csrf_enabled=False)
    if form.validate_on_submit():
        name = form.name.data
        en_bytes = form.name.data.encode('utf-8')
        en_64 = base64.b64encode(en_bytes)
        id_codificado = en_64.decode('utf-8')
        if len(id_codificado) > 22:
            id_codificado = id_codificado[:22]
        result = Artist.query.filter_by(id=id_codificado).first()
        if result:
            abort(409, message="Artista ya existente, intenta con otro")
        self_id = "https://t2musica.herokuapp.com/" + id_codificado
        albums_id = self_id + "/albums"
        tracks_id = self_id + "/tracks"
        artist = Artist(id=id_codificado, name=name, age=form.age.data, \
            albums_url=albums_id, tracks_url=tracks_id, self_url=self_id )
        db.session.add(artist)
        db.session.commit()
        artists = Artist.query.filter_by(id=id_codificado).first()
        a = [  {
                "id": artists.id,
                "name": str(artists.name),
                "age": artists.age,
                "albums": artists.albums_url,
                "tracks": artists.tracks_url,
                "self": artists.self_url
            } ]
        return jsonify(a), 201
    if form.name.errors:
        return "name error"
    if form.age.errors:
        return "age error"
    artists = Artist.query.all()
    a = [  {
            "id": i.id,
            "name": str(i.name),
            "age": i.age,
            "albums": i.albums_url,
            "tracks": i.tracks_url,
            "self": i.self_url
        } for i in artists]
    return jsonify(a), 201

@app.route('/albums', methods=["GET"])
def albums():
    form = AlbumForm(csrf_enabled=False)
    albums = Album.query.all()
    a = [{
            "id": i.id,
            "artist_id": i.artist_id, 
            "name": str(i.name),
            "genre": i.genre,
            "artist": i.artist_url,
            "tracks": i.tracks_url,
            "self": i.self_url
        } for i in albums]
    return jsonify(a), 201

@app.route('/tracks', methods=["GET"])
def tracks():
    form = SongForm(csrf_enabled=False)
    tracks = Song.query.all()
    a = [{
            "id": i.id,
            "album_id": i.album_id,
            "name": str(i.name),
            "duration": i.duration,
            "times_played": i.times_played,
            "artist": i.artist_url,
            "album": i.albums_url,
            "self": i.self_url
        } for i in tracks]
    return jsonify(a), 201

@app.route('/artists/<string:dame_artist_id>/albums', methods=["GET", "POST"])
def album_artista(dame_artist_id):
    form = AlbumForm(csrf_enabled=False)
    if form.validate_on_submit():
        informacion = form.name.data + ":" + dame_artist_id
        en_bytes = informacion.encode('utf-8')
        en_64 = base64.b64encode(en_bytes)
        id_codificado = en_64.decode('utf-8')
        if len(id_codificado) > 22:
            id_codificado = id_codificado[:22]
        result = Album.query.filter_by(id=id_codificado).first()
        if result:
            abort(409, message="Album ya existente, intenta con otro")
        self_id = "https://t2musica.herokuapp.com/albums/" + id_codificado
        artist_id2 = "https://t2musica.herokuapp.com/artists/" + dame_artist_id
        tracks_id = self_id + "/tracks"
        album = Album(id=id_codificado, artist_id = dame_artist_id, name=form.name.data, genre=form.genre.data, \
            artist_url=artist_id2, tracks_url=tracks_id, self_url=self_id )
        db.session.add(album)
        db.session.commit()
    if form.name.errors:
        string = "name error"
        return string 
    albums = Album.query.filter_by(artist_id=dame_artist_id)
    a = [{
            "id": i.id,
            "artist_id": i.artist_id, 
            "name": str(i.name),
            "genre": i.genre,
            "artist": i.artist_url,
            "tracks": i.tracks_url,
            "self": i.self_url
        } for i in albums]
    return jsonify(a), 201

@app.route('/albums/<string:dame_album_id>/tracks', methods=["GET", "POST"])
def cancion_album(dame_album_id):
    form = SongForm(csrf_enabled=False)
    if form.validate_on_submit():
        informacion = form.name.data + ":" + dame_album_id
        en_bytes = informacion.encode('utf-8')
        en_64 = base64.b64encode(en_bytes)
        id_codificado = en_64.decode('utf-8')
        if len(id_codificado) > 22:
            id_codificado = id_codificado[:22]
        result = Song.query.filter_by(id=id_codificado).first()
        if result:
            abort(409, message="Canción ya existente, intenta con otra")
        self_id = "https://t2musica.herokuapp.com/tracks/" + id_codificado ##
        buscando_album = Album.query.filter_by(id=dame_album_id).first()
        print(buscando_album.name, "#################################")
        #buscando_artista = Artist.query.filter_by(id=id_codificado).first()
        artist_id2 = "https://t2musica.herokuapp.com/artists/" + dame_album_id
        albums_id2 = "https://t2musica.herokuapp.com/albums/" + dame_album_id ##
        song = Song(id=id_codificado, album_id = dame_album_id, name=form.name.data, duration=form.duration.data, \
            times_played=0, artist_url=artist_id2, album_url=albums_id2, self_url=self_id )
        db.session.add(song)
        db.session.commit()
    # if form.name.errors:
    #     string = "name error"
    #     return string 
    tracks = Song.query.filter_by(album_id=dame_album_id)
    a = [{
            "id": i.id,
            "album_id": i.album_id, 
            "name": str(i.name),
            "duration": i.duration,
            "times_played": i.times_played,
            "artist": i.artist_url,
            "album": i.album_url,
            "self": i.self_url
        } for i in tracks]
    return jsonify(a), 201
