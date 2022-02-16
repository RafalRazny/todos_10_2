from flask import Flask, request, render_template, redirect, url_for
from models import AlbumForm, albums

app = Flask(__name__)
app.config["SECRET_KEY"] = "achtungbaby"

@app.route("/albums/", methods=["GET", "POST"])
def albums_list():
    album = AlbumForm()
    error = ""
    if request.method == "POST":
        if album.validate_on_submit():
            albums.create(album.data)
            albums.save_all()
        return redirect(url_for("albums_list"))
    return render_template("albums.html", album=album, albums=albums.all(), error=error)

@app.route("/albums/<int:album_id>/", methods=["GET", "POST"])
def album_details(album_id):
    album_update = albums.get(album_id - 1)
    album = AlbumForm(data=album_update)

    if request.method == "POST":
        if album.validate_on_submit():
            albums.update(album_id -1, album.data)
        return redirect(url_for("albums_list"))
    return render_template("details.html", album=album, album_id=album_id)

if __name__ == "__main__":
    app.run(debug=True)

