from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#, create_engine
from dotenv import load_dotenv
import os

#create_engine("sqlight:///myapp.db")
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
