from flask import Flask, jsonify, abort, make_response, request
from models import albums

app = Flask(__name__)
app.config["SECRET_KEY"] = "achtungbaby"


@app.route("/api/v1/albums/", methods=["GET"])
def todos_list_api_v1():
    return jsonify(albums.all())


@app.route("/api/v1/albums/<int:album_id>", methods=["GET"])
def get_album(album_id):
    album = albums.get(album_id)
    if not album:
        abort(404)
    return jsonify({"album": album})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': '404'}))


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}))


@app.route("/api/v1/albums/", methods=["POST"])
def create_album():
    if not request.json or 'albumname' not in request.json:
        abort(400)
    album = {
        'id_album': albums.all()[-1]['id_album']+1,
        'albumname': request.json['albumname'],
        'artistname': request.json['artistname'],
        'releaseyear': request.json.get('releaseyear', ""),
        'genre': request.json.get('genre', "")
    }
    albums.create(album)
    return jsonify({'album': album}), 201


@app.route("/api/v1/albums/<int:album_id>", methods=['DELETE'])
def delete_album(album_id):
    result = albums.delete(album_id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/api/v1/albums/<int:album_id>", methods=["PUT"])
def update_album(album_id):
    album = albums.get(album_id)
    if not album:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'albumname' in data and not isinstance(data.get('albumname'), str),
        'artistname' in data and not isinstance(data.get('artistname'), str),
        'releaseyear' in data and not isinstance(data.get('releaseyear'), int),
        'genre' in data and not isinstance(data.get('genre'), str),
        'id_album' in data and not isinstance(data.get('id_album'), int)
    ]):
        abort(400)
    album = {
        'albumname': data.get('albumyear', album['albumname']),
        'artistname': data.get('artistname', album['artistname']),
        'releaseyear': data.get('releaseyear', album['releaseyear']),
        'genre': data.get('genre', album['genre']),
        'id_album': data.get('id_album', album['id_album'])
    }
    albums.update(album_id, album)
    return jsonify({'album': album})

if __name__ == "main":
    app.run(debug=True)
