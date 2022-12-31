from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<Users {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Planets(db.Model):
    __tablename__="planets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    gravity = db.Column(db.String(120), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    climate = db.Column(db.String(120), nullable=False)
    terrain = db.Column(db.String(120), nullable=False)
    surface_water = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Planets %r>' % self.name
    
    def serializeCompact(self):
        return {
            "id":self.id,
            "name":self.name,
        }      
    
    def serializeFull(self):
        return {
            "id":self.id,
            "name":self.name,
            "diameter":self.diameter,
            "rotation_period":self.rotation_period,
            "orbital_period":self.orbital_period,
            "gravity":self.gravity,
            "population":self.population,
            "climate":self.climate,
            "terrain":self.terrain,
            "surface_water":self.surface_water,
        } 


class Characters(db.Model):
    __tablename__="characters"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.Integer, nullable=False)
    hair_color = db.Column(db.String(120), nullable=False)
    eye_color = db.Column(db.String(120), nullable=False)
    skin_color = db.Column(db.String(120), nullable=False)
    birth_year = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(120), nullable=False)
    def __repr__(self):
        return '<Characters %r>' % self.name
    
    def serializeCompact(self):
        return {
            "character id":self.id,
            "name":self.name,
        }  

    def serializeFull(self):
        return {
            "id":self.id,
            "name":self.name,
            "height":self.height,
            "mass":self.mass,
            "hair_color":self.hair_color,
            "eye_color":self.eye_color,
            "skin_color":self.skin_color,
            "birth_year":self.birth_year,
            "gender":self.gender,
        }    

class Fav_planets(db.Model):
    __tablename__="fav_planets"
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    planet=db.relationship(Planets)
    user_id=db.Column(db.Integer, db.ForeignKey("users.id"))
    user=db.relationship(Users)
    def __repr__(self):
        return '<Fav_planets %r>' % self.id
    
    def serialize(self):
        return {
            "id":self.id,
            "planet":self.planet.name,
            "user_id":self.user_id,
        }

class Fav_characters(db.Model):
    __tablename__="fav_characters"
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey("characters.id"))
    character=db.relationship(Characters)
    user_id=db.Column(db.Integer, db.ForeignKey("users.id"))
    user=db.relationship(Users)
    def __repr__(self):
        return '<Fav_characters %r>' % self.id
    
    def serialize(self):
        return {
            "id":self.id,
            "character_id":self.character_id,
            "user_id":self.user_id,
        }       

