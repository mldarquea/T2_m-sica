from my_app import app, db
from flask import render_template, jsonify, redirect, url_for
from my_app.models import Artist, Album
from my_app.forms import ArtistForm

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/artists', methods=["GET", "POST"])
def artists():
    form = ArtistForm(csrf_enabled=False)
    if form.validate_on_submit():
        artist = Artist(name=form.name.data, age=form.age.data)
        db.session.add(artist)
        db.session.commit()
    artists = Artist.query.all()
    return jsonify({"artists":artists})
