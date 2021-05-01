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
        en_bytes = form.name.data.encode('ascii')
        en_64 = base64.b64encode(en_bytes)
        id_codificado = en_64.decode('ascii')
        if len(id_codificado) > 22:
            id_codificado = id_codificado[:22]
        result = Artist.query.filter_by(id=id_codificado).first()
        if result:
            abort(409, message="Artista ya existente, intenta con otro")
        self_id = "https://t2musica.herokuapp.com/" + id_codificado
        albums_id = self_id + "/albums"
        tracks_id = self_id + "/tracks"
        artist = Artist(id=id_codificado, name=form.name.data, age=form.age.data, \
            albums_url=albums_id, tracks_url=tracks_id, self_url=self_id )
        db.session.add(artist)
        db.session.commit()
    if form.name.errors:
        return "name error"
    if form.age.errors:
        return "age error"
    artists = Artist.query.all()
    a = [str(i) for i in artists]
    return jsonify(a), 201

@app.route('/albums', methods=["GET"])
def albums():
    form = AlbumForm(csrf_enabled=False)
    albums = Album.query.all()
    a = [str(i) for i in albums]
    return jsonify(a), 201

@app.route('/tracks', methods=["GET"])
def tracks():
    form = SongForm(csrf_enabled=False)
    tracks = Song.query.all()
    a = [str(i) for i in tracks]
    return jsonify(a), 201

@app.route('/artists/<string:dame_artist_id>/albums', methods=["GET", "POST"])
def album_artista(dame_artist_id):
    form = AlbumForm(csrf_enabled=False)
    if form.validate_on_submit():
        informacion = form.name.data + ":" + dame_artist_id
        en_bytes = informacion.encode('ascii')
        en_64 = base64.b64encode(en_bytes)
        id_codificado = en_64.decode('ascii')
        if len(id_codificado) > 22:
            id_codificado = id_codificado[:22]
        result = Album.query.filter_by(id=id_codificado).first()
        if result:
            abort(409, message="Album ya existente, intenta con otro")
        self_id = "https://t2musica.herokuapp.com/albums/" + id_codificado
        artist_id = "https://t2musica.herokuapp.com/artists/" + dame_artist_id
        tracks_id = self_id + "/tracks"
        album = Album(id=id_codificado, artist_id = artist_id, name=form.name.data, genre=form.genre.data, \
            artist_url=artist_id, tracks_url=tracks_id, self_url=self_id )
        db.session.add(album)
        db.session.commit()
    if form.name.errors:
        string = "name error"
        return form.name.data 
    albums = Album.query.filter_by(artist_id=dame_artist_id)
    a = [str(i) for i in albums]
    return jsonify(a), 201
