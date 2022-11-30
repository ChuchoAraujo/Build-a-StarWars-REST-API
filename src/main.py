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
from models import db, User, Planets, Characters, Favorites
import json
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

#-------------------------- LLAMADAS GET --------------------------------------------#

### GET PEOPLE
@app.route('/people', methods=['GET'])
def get_people():
    callCharacters = Characters.query.all()
    result = [element.serialize() for element in callCharacters]
    response_body = {"message": "Todo ok bro"}
    return jsonify(result), 200


### GET PLANETS
@app.route('/planets', methods=['GET'])
def get_planets():
    callPlanet = Planets.query.all()
    result = [element.serialize() for element in callPlanet]
    response_body = {"message": "Todo ok bro"}
    return jsonify(result), 200


### GET USERS
@app.route('/users', methods=['GET'])
def get_users():
    callUsers = User.query.all()
    result = [element.serialize() for element in callUsers]
    response_body = {"message": "Todo ok bro"}
    return jsonify(result), 200

### GET FAVORITES
@app.route('/favorites', methods=['GET'])
def get_favorites():
    callFavorites = Favorites.query.all()
    result = [element.serialize() for element in callFavorites]
    response_body = {"message": "Todo ok bro"}
    return jsonify(result), 200

#-------------------------- LLAMADAS GET ID --------------------------------------------#

### GET PEOPLE ID
@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id(people_id):
    callOneCharacter = Characters.query.get(people_id)
    result = callOneCharacter.serialize()
    response_body = {"message": "Todo ok bro"}
    return jsonify(result), 200


### GET PLANET ID
@app.route('/planets/<int:planets_id>', methods=['GET'])
def getOnePlanet(planets_id):
    callPlanetOne = Planets.query.get(planets_id)
    result = callPlanetOne.serialize()
    response_body = {"message": "Todo ok bro"}
    return jsonify(result), 200


### GET USERS_ID
@app.route('/users/<int:users_id>', methods=['GET'])
def get_users_id(users_id):
    callOneUser = User.query.get(users_id)
    result = callOneUser.serialize()
    response_body = {"message": "Todo ok bro"}
    return jsonify(result), 200

#-------------------------- LLAMADAS POST --------------------------------------------#
### POST PLANETS
@app.route('/planets', methods= ['POST'])
def createPlanet():
    data= request.data
    data = json.loads(data)
    planet = Planets(name = data["name"], id = data["id"], diameter = data["diameter"], description = data["description"])
    db.session.add(planet)
    db.session.commit()

    response_body ={"msg": "ok"}
    return jsonify(planet.serialize())


### POST PEOPLE
@app.route('/people', methods= ['POST'])
def createCharacter():
    data = request.data
    data = json.loads(data)
    character = Characters(name = data["name"], height = data["height"], gender = data["gender"], description = data["description"])
    db.session.add(character)
    db.session.commit()

    response_body = {"msg": "recived"}
    return jsonify(character.serialize())


### POST USERS
@app.route('/users', methods= ['POST'])
def createUser():
    data = request.data
    data = json.loads(data)
    newUser = User(name = data["name"], email = data["email"], id = data["id"], password = data["password"], is_active = data["is_active"])
    db.session.add(newUser)
    db.session.commit()

    response_body = {"msg": "recived"}
    return jsonify(newUser.serialize())



#-------------------------- LLAMADAS DELETE --------------------------------------------#

### DELETE PLANET
@app.route('/planets/<int:planets_id>', methods= ['DELETE'])
def deletePlanet(planets_id):
    planet = Planets.query.get(planets_id)
    db.session.delete(planet)
    db.session.commit()

    response_body = {"msg": "borrado"}
    return jsonify(planet.serialize())


### DELETE PEOPLE
@app.route('/people/<int:people_id>', methods= ['DELETE'])
def deletePeople(people_id):
    character = Characters.query.get(people_id)
    db.session.delete(character)
    db.session.commit()

    response_body = {"msg": "borrado"}
    return jsonify(character.serialize())


### DELETE PEOPLE
@app.route('/users/<int:users_id>', methods= ['DELETE'])
def deleteUser(users_id):
    byeUser = User.query.get(users_id)
    db.session.delete(byeUser)
    db.session.commit()

    response_body = {"msg": "borrado"}
    return jsonify(byeUser.serialize())

#-------------------------- LLAMADAS DELETE --------------------------------------------#

### FAVORITES PLANETS
@app.route('/favorite/planets/<int:planet_id>', methods=['POST'])
def fav_planet(planet_id):
    body_request = request.get_json()

    user_id = body_request.get("user_id", None)
    planet_id = body_request.get("planet_id", None)

    newplanetFav = Favorites(user_id=user_id, planet_id=planet_id)
    db.session.add(newplanetFav)
    db.session.commit()

    response_body = {"msg": "Favorite add"}
    return jsonify(newplanetFav.serialize())


### FAVORITES CHARACTERS
@app.route('/favorite/characters/<int:character_id>', methods=['POST'])
def fav_character(character_id):
    body_request = request.get_json()

    user_id = body_request.get("user_id", None)
    character_id = body_request.get("character_id", None)

    newCharacterFav = Favorites(user_id=user_id, character_id=character_id)
    db.session.add(newCharacterFav)
    db.session.commit()

    response_body = {"msg": "Favorite add"}
    return jsonify(newCharacterFav.serialize())










# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
