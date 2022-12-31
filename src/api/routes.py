"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Users, Planets, Characters, Fav_characters, Fav_planets
from api.utils import generate_sitemap, APIException
import json

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/users', methods=['GET'])
def get_users_list():
    message = {"Full list of users."}
    users=Users.query.all()
    return list(map(lambda item: item.serialize(),users)), 200

@api.route('users/<int:user_param>/favorites', methods=['GET'])
def get_favorites(user_param):
    message = {"List of Favorites per user"}
    fav_planets=Fav_planets.query.filter(Fav_planets.user_id==user_param).all()
    fav_characters=Fav_characters.query.filter(Fav_characters.user_id==user_param).all()
    char_list=list(map(lambda item: item.serialize(),fav_characters))
    plan_list=list(map(lambda item: item.serialize(),fav_planets))
    full_list=[{'Characters': char_list}, {'Planets': plan_list}]
    return full_list, 200

@api.route('/favorites/<string:fav_type>/<int:fav_id>', methods=['DELETE'])
def delete_favorite(fav_type, fav_id):
    if fav_type == 'planets':
        planet=Fav_planets.query.filter_by(id=fav_id).delete()
        db.session.commit()
        return jsonify("Favorite Planet Deleted")
    elif fav_type == "characters":
        character=Fav_characters.query.filter_by(id=fav_id).delete()
        db.session.commit()
        return jsonify("Favorite Character Deleted")

@api.route('users/<int:user_id>/favorites/<string:fav_type>/<int:element_id>', methods=['POST'])
def add_favorite(fav_type, user_id, element_id):
    if fav_type == 'planets':
        new_planet=Fav_planets(user_id = user_id,planet_id = element_id)
        db.session.add(new_planet)
        db.session.commit()
        db.session.refresh(new_planet)
        return jsonify("Favorite Planet Added"), 200
    elif fav_type == 'characters':
        new_character=Fav_characters(
            user_id = user_id, 
            character_id = element_id
            )
        db.session.add(new_character)
        db.session.commit()
        db.session.refresh(new_character)
        return jsonify("Favorite Character Added"), 200

@api.route('/planets', methods=['GET'])
def get_planets_list():
    message = {"Full list of planets."}
    planets=Planets.query.all()
    return list(map(lambda item: item.serializeCompact(),planets)), 200

@api.route('/planets/<int:planet_param>', methods=['GET'])
def get_planet_detail(planet_param):
    message = {"Details of specific planet."}
    planet=Planets.query.filter(Planets.id==planet_param).all()
    return list(map(lambda item: item.serializeFull(),planet)), 200

@api.route('/characters', methods=['GET'])
def get_Characters_list():
    message = {"Full list of characters."}
    characters=Characters.query.all()
    return list(map(lambda item: item.serializeCompact(),characters)), 200

@api.route('/characters/<int:character_param>', methods=['GET'])
def get_character_detail(character_param):
    message = {"Details of specific character."}
    character=Characters.query.filter(Characters.id==character_param).all()
    return list(map(lambda item: item.serializeFull(),character)), 200

@api.route('/characters/new', methods=['POST'])
def add_character():
    body = json.loads(request.data)
    character_exists=Characters.query.filter(Characters.name==body["name"]).first()
    for i in body:
        if body[i] is None:
            raise APIException('There are empty values', status_code=404)
    if character_exists is None:
        new_character= Characters(
            name=body["name"],
            height=body["height"],
            mass=body["mass"],
            hair_color=body["hair_color"],
            eye_color=body["eye_color"],
            skin_color=body["skin_color"],
            birth_year=body["birth_year"],
            gender=body["gender"]
        )
        db.session.add(new_character)
        db.session.commit()
        return jsonify("New Character Added"), 200
    raise APIException('Character already exists', status_code=404)

@api.route('/characters/update/<int:character_param>', methods=['PUT'])
def update_character(character_param):
    body = json.loads(request.data)
    character_exists=Characters.query.filter(Characters.id==character_param).first()
    for i in body:
        if body[i] is None:
            raise APIException('There are empty values', status_code=404)
    if character_exists != None:
        character = Characters.query.get(character_param)
        character.name= body["name"]
        character.height= body["height"]
        character.mass= body["mass"]
        character.hair_color= body["hair_color"]
        character.eye_color= body["eye_color"]
        character.skin_color= body["skin_color"]
        character.birth_year= body["birth_year"]
        character.gender= body["gender"]
        db.session.commit()
        return jsonify("Character Updated"), 200

@api.route('/characters/delete/<int:character_param>', methods=['DELETE'])
def delete_character(character_param):
    character=Characters.query.filter(Characters.id==character_param).first()
    db.session.delete(character)
    db.session.commit()
    return jsonify("Character Deleted")

@api.route('/planets/new', methods=['POST'])
def add_planet():
    body = json.loads(request.data)
    planet_exists=Planets.query.filter(Planets.name==body["name"]).first()
    for i in body:
        if body[i] is None:
            raise APIException('There are empty values', status_code=404)
    if planet_exists is None:
        new_planet= Planets(
            name=body["name"],
            diameter=body["diameter"],
            rotation_period=body["rotation_period"],
            orbital_period=body["orbital_period"],
            gravity=body["gravity"],
            population=body["population"],
            climate=body["climate"],
            terrain=body["terrain"],
            surface_water=body["surface_water"]
        )
        db.session.add(new_planet)
        db.session.commit()
        return jsonify("New Planet Added"), 200
    raise APIException('Planet already exists', status_code=404)

@api.route('/planets/update/<int:planet_param>', methods=['PUT'])
def update_planet(planet_param):
    body = json.loads(request.data)
    planet_exists=Planets.query.filter(Planets.id==planet_param).first()
    for i in body:
        if body[i] is None:
            raise APIException('There are empty values', status_code=404)
    if planet_exists != None:
        planet = Planets.query.get(planet_param)
        planet.name= body["name"]
        planet.diameter= body["diameter"]
        planet.rotation_period= body["rotation_period"]
        planet.orbital_period= body["orbital_period"]
        planet.gravity= body["gravity"]
        planet.population= body["population"]
        planet.climate= body["climate"]
        planet.terrain= body["terrain"]
        planet.surface_water= body["surface_water"]
        db.session.commit()
        return jsonify("Planet Updated"), 200

@api.route('/planets/delete/<int:planet_param>', methods=['DELETE'])
def delete_planet(planet_param):
    planet=Planets.query.filter(Planets.id==planet_param).first()
    db.session.delete(planet)
    db.session.commit()
    return jsonify("Planet Deleted")