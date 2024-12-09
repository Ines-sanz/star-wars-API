"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, Planets, People
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():
    data= Users.query.all()
    data= [user.serialize() for user in data]
    
    return jsonify(data), 200

@app.route('/users/<int:id>', methods=['GET'])
def get_one_user(id):
    try:
        data= Users.query.get(id)
        if data is None:
            raise Exception ('error!')
        return jsonify(data.serialize())
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/planets', methods=['GET'])
def get_planets():
    data= Planets.query.all()
    data= [user.serialize() for user in data]
    
    return jsonify(data), 200

@app.route('/planets/<int:id>', methods=['GET'])
def get_one_planet(id):
    try:
        data= Planets.query.get(id)
        if data is None:
            raise Exception ('error!')
        return jsonify(data.serialize())
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/people', methods=['GET'])
def get_people():
    data= People.query.all()
    data= [user.serialize() for user in data]
    
    return jsonify(data), 200

@app.route('/people/<int:id>', methods=['GET'])
def get_one_person(id):
    try:
        data= People.query.get(id)
        if data is None:
            raise Exception ('error!')
        return jsonify(data.serialize())
    except Exception as e:
        return jsonify({"error": str(e)})



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
