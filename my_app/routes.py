from my_app import app, db
from flask import render_template, jsonify, redirect, url_for
from my_app.models import Artist, Album, Song
from my_app.forms import ArtistForm, AlbumForm, SongForm
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
        artist = Artist(name=form.name.data, age=form.age.data, id=id_codificado)
        db.session.add(artist)
        db.session.commit()
    if form.name.errors:
        return "name error"
    if form.age.errors:
        return "age error"
    artists = Artist.query.all()
    a = [str(i) for i in artists]
    return jsonify({"artists":a})
