from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    height = db.Column(db.Integer, unique=False, nullable=False)
    weitght = db.Column(db.Integer, unique=False, nullable=False)
    birth_year = db.Column(db.String(80), unique=False, nullable=False)
    

    def to_dict(self):
        return {
        '<character %s>' % self.characters
        }

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "Last name": self.last_name,
            "Height": self.height,
            "Weight": self.weitght,
            "Birth year": self.birth_year,
            
        }



class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=False)
    terrain = db.Column(db.String(500), unique=False, nullable=False)
    users = db.relationship("Favorite", back_populates="user")

    def to_dict(self):
        return {
        '<planet %s>' % self.planets
        }


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain,
            
        }

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=False, nullable=False)
    model = db.Column(db.String(150), unique=False, nullable=False)
    manufacturer = db.Column(db.String(150), unique=False, nullable=False)

    def to_dict(self):
        return {
        '<vehicle %s>' % self.vehicles
        }


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer
            
        }

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    first_name = db.Column(db.String(80), unique= False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=False, nullable=False)
    favorite_planets = db.relationship("Favorite", back_populates="planet")
    favorite_characters = db.relationship("Favorite", back_populates="character")
    favorite_vehicles = db.relationship("Favorite", back_populates="vehicle")

    def to_dict(self):
        return {
        '<user %s>' % self.users
        }


    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            
        }

class Favorite(db.Model):
    __tablename__ = 'favorite'
    user_id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    planet_id = db.Column(db.ForeignKey('planet.id'), primary_key=True)
    character_id = db.Column(db.ForeignKey('character.id'), primary_key=True)
    vehicle_id = db.Column(db.ForeignKey('vehicle.id'), primary_key=True)
    user = db.relationship("Planet", back_populates="users")
    planet = db.relationship("User", back_populates="favorite_planets")
    character = db.relationship("User", back_populates="favorite_characters")
    vehicle = db.relationship("User", back_populates="favorite_vehicles")

    def to_dict(self):
        return {
        '<favorite %s>' % self.favorite
        }


    def serialize(self):
        return {
            # "id": self.id,
            # "characterId": self.character_id,
            # "vehicleId": self.vehicle_id,
            # "planetId": self.planet_id,
            # "userid": self.user_id,
            
        }
        
