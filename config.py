import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', './uploads')
