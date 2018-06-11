import json

import jwt
import datetime
from models import User, Point, Path
from flask_cors import CORS
from database import db_session, init_db
from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
CORS(app)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            token = request.form['token']
        if not token:
            return jsonify({'message': 'Token is missing!'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid'})
        return f(*args, **kwargs)

    return decorated


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username, password=password).first()
    if registered_user is None:
        return 'Error login'
    token = jwt.encode(
        {
            'id': registered_user.id,
            'email': registered_user.email,
            'user': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=3600)
        },
        app.config['SECRET_KEY'])
    return jsonify(
        {
            'token': token.decode('UTF-8'),
            'id': registered_user.id,
            'email': registered_user.email
        })


@app.route('/request', methods=['GET'])
@login_required
def requ():
    return 'ok'


@app.route('/register', methods=['POST'])
def register():
    user = User(request.form['username'], request.form['password'], request.form['email'])
    db_session.add(user)
    print(user.id)  
    db_session.commit()

    return 'ok'


@app.route('/create_path', methods=['POST'])
@login_required
def create_path():
    new_path = Path(request.form['id'], request.form['name'])
    db_session.add(new_path)
    db_session.commit()
    for point in json.loads(request.form['points']):
        db_session.add(Point(new_path.id, float(point['lat']), float(point['lng'])))
    db_session.commit()
    return 'ok'


@app.route('/get_all_name_path', methods=['GET'])
@login_required
def get_all_path():
    return jsonify([
        {
            'name': path.name
        } for path in Path.query.filter_by(id_user=request.args['id'])])


@app.route('/get_path_by_name', methods=['GET'])
@login_required
def get_path():
    name = request.args['path_name']
    id = request.args['id']
    path = Path.query.filter_by(id_user=id, name=name).first()
    points = Point.query.filter_by(id_path=path.id)
    return jsonify([{
        'lat': str(p.lat),
        'lng': str(p.lng)
    } for p in points])


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
