from my_app import app, db
from flask import render_template, jsonify, redirect, url_for
from my_app.models import Artist, Album

class Artist(Resource):
    def get(self):
        pass
    