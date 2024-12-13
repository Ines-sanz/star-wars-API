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

@app.route('/users/favorites', methods=['GET'])
def get_users_favorites():
    try: 
        users = Users.query.all()
        users_data = []
        for user in users:
            user_data = {
                "id": user.id,
                "name": f"{user.first_name} {user.last_name}",
                "favorites" : {
                    "planets":  [planet.serialize() for planet in user.planets],
                    "people":  [person.serialize() for person in user.people]
                }
            }
            users_data.append(user_data)

        return jsonify(users_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/users/<int:id>/favorites', methods=['GET'])
def get_one_user_favorites(id):
    try: 
        user = Users.query.get(id)
        if user is None:  
            return jsonify({"error": "User not found"}), 404
        
        user_data = {
                "id": user.id,
                "name": f"{user.first_name} {user.last_name}",
                "favorites" : {
                    "planets":  [planet.serialize() for planet in user.planets],
                    "people":  [person.serialize() for person in user.people]
                }
            }
        if len(user_data) < 1:
            return jsonify({"This user has no favorites"})

        return jsonify(user_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/users/<int:user_id>/favorites/newfavperson/<int:people_id>', methods=['Post'])
def post_new_favorite_person(user_id, people_id):
    try: 
        user = Users.query.get(user_id)
        if user is None:  
            return jsonify({"error": "User not found"}), 400
        
        person = People.query.get(people_id)
        if person is None:  
            return jsonify({"error": "People not found"}), 400
        
        
        if person in user.people:
             return jsonify({"message": "Person is already in user's favorites"}), 400
        
        user.people.append(person)
        db.session.commit()

        return jsonify({
            "message": "Person added to user's favorites successfully",
            "user_id": user.id,
            "person": person.name
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/users/<int:user_id>/favorites/deletefavperson/<int:people_id>', methods=['Delete'])
def delete_favorite_person(user_id, people_id):
    try: 
        user = Users.query.get(user_id)
        if user is None:  
            return jsonify({"error": "User not found"}), 400
        
        person = People.query.get(people_id)
        if person is None:  
            return jsonify({"error": "People not found"}), 400
        
        
        if person not in user.people:
             return jsonify({"message": "Person is not in user's favorites"}), 400
        
        user.people.remove(person)
        db.session.commit()

        return jsonify({
            "message": "Person deleted from user's favorites successfully",
            "user_id": user.id,
            "person": person.name
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@app.route('/users/<int:user_id>/favorites/newfavplanet/<int:planet_id>', methods=['Post'])
def post_new_favorite_planet(user_id, planet_id):
    try:
        user = Users.query.get(user_id)
        if user is None:
            return jsonify({"message": "User not found"}), 400
        

        planet = Planets.query.get(planet_id)
        if planet is None:
            return jsonify({"message": "Planet not found"}), 400
        
        if planet in user.planets:
            return jsonify({"message": "Planet alredy in user's favorites"}), 400
        
        user.planets.append(planet)
        db.session.commit()

        return jsonify({
                "message": "Planet added to user's favorites successfully",
                "user_id": user.id,
                "planet": planet.name
            }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/users/<int:user_id>/favorites/deletefavplanet/<int:planet_id>', methods=['Delete'])
def delete_favorite_planet(user_id, planet_id):
    try:
        user = Users.query.get(user_id)
        if user is None:
            return jsonify({"message": "User not found"}), 400
        

        planet = Planets.query.get(planet_id)
        if planet is None:
            return jsonify({"message": "Planet not found"}), 400
        
        if planet not in user.planets:
            return jsonify({"message": "Planet is not in user's favorites"}), 400
        
        user.planets.remove(planet)
        db.session.commit()

        return jsonify({
                "message": "Planet deleted from user's favorites successfully",
                "user_id": user.id,
                "planet": planet.name
            }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
