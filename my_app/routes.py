from my_app import app, db
from flask import render_template, jsonify, redirect, url_for
from my_app.models import User
from my_app.forms import RegistrationForm

@app.route('/')
def hello_world():
    return render_template('home.html')
