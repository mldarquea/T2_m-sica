from my_app import app, db
from flask import render_template, jsonify, redirect, url_for, request
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
    if request.method == 'POST' and form.validate_on_submit() == False:
        abort(400, message="Datos mal ingresados")
    if request.method not in ["GET", "POST"]:
        abort(405, message="Método no implementado")
    if form.validate_on_submit():
        name = form.name.data
        en_bytes = form.name.data.encode('utf-8')
        en_64 = base64.b64encode(en_bytes)
        id_codificado = en_64.decode('utf-8')
        if len(id_codificado) > 22:
            id_codificado = id_codificado[:22]
        result = Artist.query.filter_by(id=id_codificado).first()
        if result:
            artists = Artist.query.filter_by(id=id_codificado).first()
            a =   {
                    "id": artists.id,
                    "name": str(artists.name),
                    "age": artists.age,
                    "albums": artists.albums_url,
                    "tracks": artists.tracks_url,
                    "self": artists.self_url
                } 
            return jsonify(a), 409
        self_id = "https://t2musica.herokuapp.com/artists/" + id_codificado
        albums_id = self_id + "/albums"
        tracks_id = self_id + "/tracks"
        artist = Artist(id=id_codificado, name=name, age=form.age.data, \
            albums_url=albums_id, tracks_url=tracks_id, self_url=self_id )
        db.session.add(artist)
        db.session.commit()
        artists = Artist.query.filter_by(id=id_codificado).first()
        a = {
                "id": artists.id,
                "name": str(artists.name),
                "age": artists.age,
                "albums": artists.albums_url,
                "tracks": artists.tracks_url,
                "self": artists.self_url
            }
        return jsonify(a), 201
    if form.name.errors:
        return "name error"
    if form.age.errors:
        return "age error"
    artists = Artist.query.all()
    a = [{
            "id": i.id,
            "name": str(i.name),
            "age": i.age,
            "albums": i.albums_url,
            "tracks": i.tracks_url,
            "self": i.self_url
        } for i in artists]
    return jsonify(a), 200
####
@app.route('/albums', methods=["GET"])
def albums():
    form = AlbumForm(csrf_enabled=False)
    if request.method not in ["GET"]:
        abort(405, message="Método no implementado")
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
    return jsonify(a), 200

@app.route('/tracks', methods=["GET"])
def tracks():
    form = SongForm(csrf_enabled=False)
    if request.method not in ["GET"]:
        abort(405, message="Método no implementado")
    tracks = Song.query.all()
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
    return jsonify(a), 200

@app.route('/artists/<string:dame_artist_id>/albums', methods=["GET", "POST"])
def album_artista(dame_artist_id):
    form = AlbumForm(csrf_enabled=False)
    if request.method not in ["GET", "POST"]:
        abort(405, message="Método no implementado")
    if not Artist.query.filter_by(id=dame_artist_id).first():
        if request.method == "POST":
            abort(422, message="Artista no existe")
        if request.method == "GET":
            abort(404, message="Artista no existe")
    if request.method == 'POST' and form.validate_on_submit() == False:
        abort(400, message="Datos mal ingresados")
    if form.validate_on_submit():
        informacion = form.name.data + ":" + dame_artist_id
        en_bytes = informacion.encode('utf-8')
        en_64 = base64.b64encode(en_bytes)
        id_codificado = en_64.decode('utf-8')
        if len(id_codificado) > 22:
            id_codificado = id_codificado[:22]
        result = Album.query.filter_by(id=id_codificado).first()
        if result:
            i = Album.query.filter_by(id=id_codificado).first()
            a = {
                "id": i.id,
                "artist_id": i.artist_id, 
                "name": str(i.name),
                "genre": i.genre,
                "artist": i.artist_url,
                "tracks": i.tracks_url,
                "self": i.self_url
            }
            return jsonify(a), 409
        self_id = "https://t2musica.herokuapp.com/albums/" + id_codificado
        artist_id2 = "https://t2musica.herokuapp.com/artists/" + dame_artist_id
        tracks_id = self_id + "/tracks"
        album = Album(id=id_codificado, artist_id = dame_artist_id, name=form.name.data, genre=form.genre.data, \
            artist_url=artist_id2, tracks_url=tracks_id, self_url=self_id )
        db.session.add(album)
        db.session.commit()
    # if form.name.errors:
    #     string = "name error"
    #     return string 
    albumes_r = Album.query.filter_by(artist_id=dame_artist_id)
    a = [{
            "id": i.id,
            "artist_id": i.artist_id, 
            "name": str(i.name),
            "genre": i.genre,
            "artist": i.artist_url,
            "tracks": i.tracks_url,
            "self": i.self_url
        } for i in albumes_r]
    if form.validate_on_submit():
        return jsonify(a[0]), 201
    else:
        return jsonify(a), 200

@app.route('/albums/<string:dame_album_id>/tracks', methods=["GET", "POST"])
def cancion_album(dame_album_id):
    form = SongForm(csrf_enabled=False)
    if request.method not in ["GET", "POST"]:
        abort(405, message="Método no implementado")
    if not Album.query.filter_by(id=dame_album_id).first():
        if request.method == "POST":
            abort(422, message="Artista no existe")
        if request.method == "GET":
            abort(404, message="Artista no existe")
    if request.method == 'POST' and form.validate_on_submit() == False:
        abort(400, message="Datos mal ingresados")
    if form.validate_on_submit():
        informacion = form.name.data + ":" + dame_album_id
        en_bytes = informacion.encode('utf-8')
        en_64 = base64.b64encode(en_bytes)
        id_codificado = en_64.decode('utf-8')
        if len(id_codificado) > 22:
            id_codificado = id_codificado[:22]
        result = Song.query.filter_by(id=id_codificado).first()
        if result:
            i = Song.query.filter_by(id=id_codificado).first()
            a = {
                "id": i.id,
                "album_id": i.album_id, 
                "name": str(i.name),
                "duration": i.duration,
                "times_played": i.times_played,
                "artist": i.artist_url,
                "album": i.album_url,
                "self": i.self_url
            }
            return jsonify(a), 409
        self_id = "https://t2musica.herokuapp.com/tracks/" + id_codificado ##
        buscando_album = Album.query.filter_by(id=dame_album_id).first()
        buscando_artista = buscando_album.artist_id
        artist_id2 = "https://t2musica.herokuapp.com/artists/" + buscando_artista
        albums_id2 = "https://t2musica.herokuapp.com/albums/" + dame_album_id ##
        song = Song(id=id_codificado, album_id = dame_album_id, name=form.name.data, duration=form.duration.data, \
            times_played=0, artist_url=artist_id2, album_url=albums_id2, self_url=self_id )
        db.session.add(song)
        db.session.commit()
    raro = Song.query.filter_by(album_id=dame_album_id)
    a = [{
            "id": i.id,
            "album_id": i.album_id, 
            "name": str(i.name),
            "duration": i.duration,
            "times_played": i.times_played,
            "artist": i.artist_url,
            "album": i.album_url,
            "self": i.self_url
        } for i in raro]
    if form.validate_on_submit():
        return jsonify(a[0]), 201
    else:
        return jsonify(a), 200

@app.route('/artists/<string:dame_artist_id>/tracks', methods=["GET"])
def cancion_artista(dame_artist_id):
    if request.method not in ["GET"]:
        abort(405, message="Método no implementado")
    if not Artist.query.filter_by(id=dame_artist_id).first():
        abort(404, message="Artista no existe")
    link_tracks = "https://t2musica.herokuapp.com/artists/" + dame_artist_id
    tracks_buscado = Song.query.filter_by(artist_url=link_tracks)
    a = [{
            "id": i.id,
            "album_id": i.album_id, 
            "name": str(i.name),
            "duration": i.duration,
            "times_played": i.times_played,
            "artist": i.artist_url,
            "album": i.album_url,
            "self": i.self_url
        } for i in tracks_buscado]
    return jsonify(a), 200

@app.route('/tracks/<string:dame_track_id>', methods=["GET","DELETE"])
def track_por_id(dame_track_id):
    i = Song.query.filter_by(id=dame_track_id).first()
    if not i:
        abort(404, message="mato")
    if request.method not in ["GET","DELETE"]:
        abort(405, message="Método no implementado") 
    if request.method == "GET":
        a = {
            "id": i.id,
            "album_id": i.album_id, 
            "name": str(i.name),
            "duration": i.duration,
            "times_played": i.times_played,
            "artist": i.artist_url,
            "album": i.album_url,
            "self": i.self_url
        }
        return jsonify(a), 200
    if request.method == "DELETE":
        Song.query.filter_by(id=dame_track_id).delete()
        db.session.commit()
        return 'delete', 204

@app.route('/albums/<string:dame_album_id>', methods=["GET","DELETE"])
def album_por_id(dame_album_id):
    i = Album.query.filter_by(id=dame_album_id).first()
    if not i:
        abort(404, message="mato")
    if request.method not in ["GET","DELETE"]:
        abort(405, message="Método no implementado")
    if request.method == "GET":
        a = {
            "id": i.id,
            "artist_id": i.artist_id, 
            "name": str(i.name),
            "genre": i.genre,
            "artist": i.artist_url,
            "tracks": i.tracks_url,
            "self": i.self_url
        }
        return jsonify(a), 200
    if request.method == "DELETE":
        ######tracks
        tracks_buscado = Song.query.filter_by(album_id=dame_album_id)
        a = [{
                "id": i.id,
                "album_id": i.album_id, 
                "name": str(i.name),
                "duration": i.duration,
                "times_played": i.times_played,
                "artist": i.artist_url,
                "album": i.album_url,
                "self": i.self_url
            } for i in tracks_buscado]
        if a != []:
            Song.query.filter_by(album_id=dame_album_id).delete()
            db.session.commit()
        ###Album
        Album.query.filter_by(id=dame_album_id).delete()
        db.session.commit()
        return 'delete', 204

@app.route('/artists/<string:dame_artist_id>', methods=["GET", "DELETE"])
def artista_por_id(dame_artist_id):
    i = Artist.query.filter_by(id=dame_artist_id).first()
    if not i:
        abort(404, message="mato")
    if request.method not in ["GET", "DELETE"]:
        abort(405, message="Método no implementado")
    if request.method == "GET":
        a = {
                "id": i.id,
                "name": str(i.name),
                "age": i.age,
                "albums": i.albums_url,
                "tracks": i.tracks_url,
                "self": i.self_url
            }
        return jsonify(a), 200
    if request.method == "DELETE":
        ####Tracks
        link_tracks = "https://t2musica.herokuapp.com/artists/" + dame_artist_id
        tracks_buscado = Song.query.filter_by(artist_url=link_tracks)
        a = [{
                "id": i.id,
                "album_id": i.album_id, 
                "name": str(i.name),
                "duration": i.duration,
                "times_played": i.times_played,
                "artist": i.artist_url,
                "album": i.album_url,
                "self": i.self_url
            } for i in tracks_buscado]
        if a != []:
            Song.query.filter_by(artist_url=link_tracks).delete()
            db.session.commit()
        ####Albums
        album_buscado = Album.query.filter_by(artist_id=dame_artist_id)
        a = [{
                "id": i.id,
                "artist_id": i.artist_id, 
                "name": str(i.name),
                "genre": i.genre,
                "artist": i.artist_url,
                "tracks": i.tracks_url,
                "self": i.self_url
            } for i in album_buscado]
        if a != []:
            Album.query.filter_by(artist_id=dame_artist_id).delete()
            db.session.commit()

        ###ARtist
        Artist.query.filter_by(id=dame_artist_id).delete()
        db.session.commit() 
        return 'delete', 204

@app.route('/tracks/<string:dame_track_id>/play', methods=["PUT"])
def reproduce_track(dame_track_id):
    i = Song.query.filter_by(id=dame_track_id).first()
    if not i:
        abort(404, message="mato")
    if request.method != "PUT":
        abort(405, message="Método no implementado")
    i = Song.query.filter_by(id=dame_track_id).first()
    a = {
            "id": i.id,
            "album_id": i.album_id, 
            "name": str(i.name),
            "duration": i.duration,
            "times_played": i.times_played,
            "artist": i.artist_url,
            "album": i.album_url,
            "self": i.self_url
        } 
    nuevas_reproducciones = a["times_played"] + 1
    Song.query.filter_by(id=dame_track_id).update(dict(times_played=nuevas_reproducciones))
    db.session.commit()
    return "yey   ", 200

@app.route('/albums/<string:dame_album_id>/tracks/play', methods=["PUT"])
def reproduce_album(dame_album_id):
    i = Album.query.filter_by(id=dame_album_id).first()
    if not i:
        abort(404, message="mato")
    if request.method != "PUT":
        abort(405, message="Método no implementado")
    # track_actual = Song.query.filter_by(id=dame_track_id).first()
    # track_actual.times_played += 1
    canciones_album = Song.query.filter_by(album_id=dame_album_id)
    for i in canciones_album:
        a = {
                "id": i.id,
                "album_id": i.album_id, 
                "name": str(i.name),
                "duration": i.duration,
                "times_played": i.times_played,
                "artist": i.artist_url,
                "album": i.album_url,
                "self": i.self_url
            } 
        nuevas_reproducciones = a["times_played"] + 1
        Song.query.filter_by(album_id=dame_album_id).update(dict(times_played=nuevas_reproducciones))
        db.session.commit()
    return "yey   ", 200

@app.route('/artists/<string:dame_artist_id>/albums/play', methods=["PUT"])
def reproduce_artista(dame_artist_id):
    i = Artist.query.filter_by(id=dame_artist_id).first()
    if not i:
        abort(404, message="mato")
    if request.method != "PUT":
        abort(405, message="Método no implementado")
    link_artista = "https://t2musica.herokuapp.com/artists/" + dame_artist_id
    canciones_album = Song.query.filter_by(artist_url=link_artista)
    for i in canciones_album:
        a = {
                "id": i.id,
                "album_id": i.album_id, 
                "name": str(i.name),
                "duration": i.duration,
                "times_played": i.times_played,
                "artist": i.artist_url,
                "album": i.album_url,
                "self": i.self_url
            } 
        nuevas_reproducciones = a["times_played"] + 1
        Song.query.filter_by(artist_url=link_artista).update(dict(times_played=nuevas_reproducciones))
        db.session.commit()
    return "yey   ", 200