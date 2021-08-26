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
from models import db, User, Character, Vehicle, Planet, Favorite
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# from flask_jwt_extended import create_access_token

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
app.config["JWT_SECRET_KEY"] = "MSWAPI_secret"  # Change this "super secret" with something else!
jwt = JWTManager(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)


## LOGIN

@app.route("/token", methods=["POST"])
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    # Query your database for username and password
    user = User.filter.query(username=username, password=password).first()
    if user is None:
        # the user was not found on the database
        return jsonify({"msg": "Bad username or password"}), 401
    
    # create a new token with the user id inside
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id })

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    user = User.filter.get(current_user_id)
    
    return jsonify({"id": user.id, "username": user.username }), 200

## USER

@app.route('/user', methods=['GET'])
def handle_user():
    users = User.query.all()
    mapped_users=[u.serialize() for u in users]
    return jsonify(mapped_users), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def handle_single_user(user_id):
    users = User.query.get(user_id)
    users = users.serialize()
    return jsonify(users), 200

@app.route('/user', methods=['POST'])
def post_user():
    user1 = User(username="my_super_username", email="my_super@email.com", first_name="mysupername", last_name="mysuperlastname")
    db.session.add(user1)
    db.session.commit()
    return jsonify(user1.serialize())

## CHARACTER

@app.route('/character', methods=['GET'])
@jwt_required()
def handle_character():
    characters = Character.query.all()
    mapped_characters=[c.serialize() for c in characters]
    return jsonify(mapped_characters), 200

@app.route('/character/<int:character_id>', methods=['GET'])
@jwt_required()
def handle_single_character(character_id):
    characters = Character.query.get(character_id)
    characters = characters.serialize()
    return jsonify(characters), 200

@app.route('/character', methods=['POST'])
def post_character():
    character1 = Character(first_name="my_super_name", last_name="my_super_last_name", height="my_super_height", weight="my_super_weight", birth_year="my_super_birth_year")
    db.session.add(character1)
    db.session.commit()
    return jsonify(character1.serialize())

## PLANET

@app.route('/planet', methods=['GET'])
@jwt_required()
def handle_planet():
    planets = Planet.query.all()
    mapped_planets=[p.serialize() for p in planets]
    return jsonify(mapped_planets), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
@jwt_required()
def handle_single_planet(planet_id):
    planets = Planet.query.get(planet_id)
    planets = planets.serialize()
    return jsonify(planets), 200

@app.route('/planet', methods=['POST'])
def post_planet():
    planet1 = Planet(name="my_super_name", climate="my_super_climate", diameter="my_super_diameter", orbital_period="my_super_orbital_period", population="my_super_population")
    db.session.add(planet1)
    db.session.commit()
    return jsonify(planet1.serialize())

## VEHICLE

@app.route('/vehicle', methods=['GET'])
@jwt_required()
def handle_vehicle():
    vehicles = Vehicle.query.all()
    mapped_vehicles=[v.serialize() for v in vehicles]
    return jsonify(mapped_vehicles), 200

@app.route('/vehicle/<int:vehicle_id>', methods=['GET'])
@jwt_required()
def handle_single_vehicle(vehicle_id):
    vehicles = Vehicle.query.get(vehicle_id)
    vehicles = vehicles.serialize()
    return jsonify(vehicles), 200

@app.route('/vehicle', methods=['POST'])
def post_vehicle():
    vehicle1 = Vehicle(model="my_super_model", manufacturer="my_super_manufacturer")
    db.session.add(vehicle1)
    db.session.commit()
    return jsonify(vehicle1.serialize())

## FAVORITE

@app.route('/favorite', methods=['GET'])
@jwt_required()
def handle_favorite():
    favorites = Favorite.query.all()
    mapped_favorites=[f.serialize() for f in favorites]
    return jsonify(mapped_favorites), 200

@app.route('/favorite/<int:favorite_id>', methods=['GET'])
@jwt_required()
def handle_single_favorite(favorite_id):
    favorites = Favorite.query.get(favorite_id)
    favorites = favorites.serialize()
    return jsonify(favorites), 200

@app.route('/favorite', methods=['POST'])
def post_favorite():
    favorite1 = Favorite(model="my_super_model", manufacturer="my_super_manufacturer")
    db.session.add(favorite1)
    db.session.commit()
    return jsonify(favorite1.serialize())


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
