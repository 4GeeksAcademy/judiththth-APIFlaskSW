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
from models import db, User, Character, Planet
from sqlalchemy import select
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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


# ---------------------------------ENDPOINTS-----------------------------------------------

#----------------------------------CHARACTERS----------------------------------

@app.route('/characters', methods=['GET'])
def get_all_characters():

    #para consultar todos los registros de una tabla
    all_characters = db.session.execute(select(Character)).scalars().all()
    
    #procesa la info en un formato legible para el desarrollador (serialize)
    results = list(map(lambda item: item.serialize(), all_characters))
    print(results)

    response_body = {
    "msg": "ok character",
    "results": results
    }

    return jsonify(response_body), 200

@app.route('/character/<int:id>', methods=['GET'])
def get_one_character(id):
    
    character = db.session.get(Character, id)
    
    if character is None:
        return jsonify({"msg":"The character doesn't exist"}), 404

    response_body = {
    "msg": "ok character id",
    "result": character.serialize()
    }

    return jsonify(response_body), 200


@app.route('/character', methods=['POST']) #la ruta no lleva id porque aún no se ha creado
def add_character():
    
    character_data = request.get_json()
    new_character = Character(
        name=character_data.get("name"), #("") -> en Python indica que estás apuntando a ese sitio
        age=character_data.get("age"),
        origin=character_data.get("origin")
    )

    db.session.add(new_character)
    db.session.commit()
  
    response_body = {
    "msg": "The character has been added successfully",
    "result": new_character.serialize()
    }

    return jsonify(response_body), 200


@app.route('/characters/<int:id>', methods=['DELETE'])
def remove_character(id):

    remove_character = db.session.get(Character, id)
    db.session.delete(remove_character)
    db.session.commit()
    
    return jsonify("The character has been removed"), 200


#----------------------------------PLANETS------------------------------------------------------------

@app.route('/planets', methods=['GET'])
def get_all_planets():

    #para consultar todos los registros de una tabla
    all_planets = db.session.execute(select(Planet)).scalars().all()
    
    #procesa la info en un formato legible para el desarrollador (serialize)
    results = list(map(lambda item: item.serialize(), all_planets))
    print(results)

    response_body = {
    "msg": "ok planet",
    "results": results
    }

    return jsonify(response_body), 200

@app.route('/planets/<int:id>', methods=['GET'])
def get_one_planet(id):
    
    planet = db.session.get(Planet, id)
    
    if planet is None:
        return jsonify({"msg":"The planet doesn't exist"}), 404

    response_body = {
    "msg": "ok planet id",
    "result": planet.serialize()
    }

    return jsonify(response_body), 200


@app.route('/planet', methods=['POST']) 
def add_planet():
    
    planet_data = request.get_json()
    new_planet = Planet(
        name=planet_data.get("name"), 
        population=planet_data.get("population"),
        surface=planet_data.get("surface")
    )

    db.session.add(new_planet)
    db.session.commit()
  
    response_body = {
    "msg": "The planet has been added successfully",
    "result": new_planet.serialize()
    }

    return jsonify(response_body), 200


@app.route('/planets/<int:id>', methods=['DELETE'])
def remove_planet(id):

    remove_planet = db.session.get(Planet, id)
    db.session.delete(remove_planet)
    db.session.commit()
    
    return jsonify("The planet has been removed"), 200


#-------------------------------------USERS--------------------------------------

@app.route('/user', methods=['GET'])
def get_all_users():

    #para consultar todos los registros de una tabla
    all_users = db.session.execute(select(User)).scalars().all()
    
    #procesa la info en un formato legible para el desarrollador (serialize)
    results = list(map(lambda item: item.serialize(), all_users))
    print(results)

    response_body = {
    "msg": "ok users",
    "results": results
    }

    return jsonify(response_body), 200

@app.route('/user/<int:id>', methods=['GET'])
def get_one_user(id):
    
    user = db.session.get(User, id)
    
    if user is None:
        return jsonify({"msg":"The user doesn't exist"}), 404

    response_body = {
    "msg": "ok user id",
    "result": user.serialize()
    }

    return jsonify(response_body), 200


@app.route('/user', methods=['POST'])
def add_user():
    
    user_data = request.get_json()
    new_user = User(
        email=user_data.get("enail"),
        password=user_data.get("password"),
    )

    db.session.add(new_user)
    db.session.commit()
  
    response_body = {
    "msg": "The user has been added successfully",
    "result": new_user.serialize()
    }

    return jsonify(response_body), 200


@app.route('/users/<int:id>', methods=['DELETE'])
def remove_user(id):

    remove_user = db.session.get(User, id)
    db.session.delete(remove_user)
    db.session.commit()
    
    return jsonify("The user has been removed"), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
