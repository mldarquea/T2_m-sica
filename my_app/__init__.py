from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_restful import Api, Resource, reqparse, abort
from dotenv import load_dotenv
import os

# Load environmet variables
load_dotenv('./env')

# Create app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

#_______________________________________________________________________________
# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)
if db:
    print('DB IS READY!!!\n')

from my_app import routes
#from my_app import prueba