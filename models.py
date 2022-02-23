import json
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange, InputRequired
from datetime import datetime

albums_json = "albums.json"

class AlbumsRepository:
    def __init__(self):
        try:
            with open(albums_json, "r") as f:
                self.albums = json.load(f)
        except FileNotFoundError:
            self.albums = []
    
    def all(self):
        return self.albums
    
    def get(self, id):
        return self.albums[id]
    
    def create(self, data):
        data.pop("csrf_token")
        self.albums.append(data)
    
    def save_all(self):
        with open(albums_json, "w") as f:
            json.dump(self.albums, f)

    def update(self, id, data):
        data.pop('csrf_token')
        self.albums[id] = data
        self.save_all()

albums = AlbumsRepository()

current_year = datetime.now().year

class AlbumForm(FlaskForm):
    albumname = StringField("Album Name", validators=[DataRequired()])
    artistname = StringField("Artist Name", validators=[DataRequired()])
    releaseyear = IntegerField("Release Year", validators=[NumberRange(min=1900, max=current_year, message=f'Please insert the year between 1900 and {current_year}')])
    genre = SelectField("Genre", choices = [('rock'), ('pop'), ('alternative'), ('hip-how'), ('dance'), ('jazz'), ('electronic'), ('classic')], validators=[InputRequired()])
    id_album = StringField("Album id", validators=[DataRequired()])
