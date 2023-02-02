from flask import Flask
# from config import Config

# Config Values
# location where file uploads will be stored
UPLOAD_FOLDER = './app/static/uploads'
# UPLOAD_FOLDER = 'uploads/'

# needed for session security, the flash() method in this case stores the message
# in a session
SECRET_KEY = 'Sup3r$3cretkey'

app = Flask(__name__)
app.config.from_object(__name__)
# app.config.from_object(Config)
from app import views