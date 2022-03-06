import json
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
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

    def get(self, id_album):
        album = [album for album in self.all()
                 if album["id_album"] == id_album]
        if album:
            return album[0]
        return []

    def create(self, data):
        self.albums.append(data)
        self.save_all()

    def save_all(self):
        with open("albums.json", "w") as f:
            json.dump(self.albums, f)

    def update(self, id_album, data):
        album = self.get(id_album)
        if album:
            index = self.albums.index(album)
            self.albums[index] = data
            self.save_all()
            return True
        return False

    def delete(self, id_album):
        album = self.get(id_album)
        if album:
            self.albums.remove(album)
            self.save_all()
            return True
        return False


albums = Albums()

thisyear = datetime.now().year


class AlbumForm(FlaskForm):
    id_album = IntegerField("Album id")
    albumname = StringField("Album Name", validators=[DataRequired()])
    artistname = StringField("Artist Name", validators=[DataRequired()])
    releaseyear = IntegerField("Release Year")
    genre = StringField("Genre")