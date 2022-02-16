import json
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange, InputRequired
from datetime import datetime


class Albums:
    def __init__(self):
        try:
            with open("albums.json", "r") as f:
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
        with open("albums.json", "w") as f:
            json.dump(self.albums, f)

    def update(self, id, data):
        data.pop('csrf_token')
        self.albums[id] = data
        self.save_all()

albums = Albums()

thisyear = datetime.now().year

class AlbumForm(FlaskForm):
    albumname = StringField("Album Name", validators=[DataRequired()])
    artistname = StringField("Artist Name", validators=[DataRequired()])
    releaseyear = IntegerField("Release Year", validators=[NumberRange(min=1900, max=thisyear, message='Please insert the year between 1900 and {thisyear}')])
    genre = SelectField("Genre", choices = [('rock'), ('pop'), ('alternative'), ('hip-how'), ('dance'), ('jazz'), ('electronic'), ('classic')], validators=[InputRequired()])
    id_album = StringField("Album id", validators=[DataRequired()])
