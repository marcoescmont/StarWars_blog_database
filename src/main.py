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
from models import db, User, Character, Vehicle, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

@app.route('/user', methods=['GET'])
def handle_user():
    users = User.query.all()
    mapped_users=[u.serialize() for u in users]
    return jsonify(mapped_users), 200

@app.route('/user', methods=['POST'])
def post_user():
    user1 = User(username="my_super_username", email="my_super@email.com", first_name="mysupername", last_name="mysuperlastname")
    db.session.add(user1)
    db.session.commit()
    return jsonify(user1.serialize())

@app.route('/character', methods=['GET'])
def handle_character():
    characters = Character.query.all()
    mapped_characters=[c.serialize() for c in characters]
    return jsonify(mapped_characters), 200

@app.route('/character', methods=['POST'])
def post_character():
    character1 = Character(first_name="my_super_name", last_name="my_super_last_name", height="my_super_height", weight="my_super_weight", birth_year="my_super_birth_year")
    db.session.add(character1)
    db.session.commit()
    return jsonify(character1.serialize())

@app.route('/planet', methods=['GET'])
def handle_planet():
    planets = Planet.query.all()
    mapped_planets=[p.serialize() for p in planets]
    return jsonify(mapped_planets), 200

@app.route('/planet', methods=['POST'])
def post_planet():
    planet1 = Planet(name="my_super_name", climate="my_super_climate", diameter="my_super_diameter", orbital_period="my_super_orbital_period", population="my_super_population")
    db.session.add(planet1)
    db.session.commit()
    return jsonify(planet1.serialize())

@app.route('/vehicle', methods=['GET'])
def handle_vehicle():
    vehicles = Vehicle.query.all()
    mapped_vehicles=[v.serialize() for v in vehicles]
    return jsonify(mapped_vehicles), 200

@app.route('/vehicle', methods=['POST'])
def post_vehicle():
    vehicle1 = Vehicle(model="my_super_model", manufacturer="my_super_manufacturer")
    db.session.add(vehicle1)
    db.session.commit()
    return jsonify(vehicle1.serialize())

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
