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
from models import db, User, Characters, Planets, FavPlanets, FavCharacters, FavStarships
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


    return jsonify(response_body), 200


@app.route('/users', methods=['GET'])
def users():
    users = User.query.all()
   
    users_serialized = []
    for user in users:
        users_serialized.append(user.serialize())
        
    return jsonify({'List of users:': users_serialized })

@app.route('/user/<int:user_id>', methods=['GET'])
def user(user_id):
    user = User.query.get(user_id)
        
    return jsonify({'User requested:': user.serialize() })


@app.route('/register', methods=['POST'])
def add_user():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Body needs email and password.'}), 400
    if 'email' not in body:
        return jsonify({'msg':'email field is mandatory'}), 400
    if 'password' not in body:
        return jsonify({'msg':'Password field is mandatory'}), 400
    # print(body)    
    new_user = User()
    new_user.email = body['email']
    new_user.password = body['password']
    new_user.is_active = True
    
    # print(type(new_user))
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'msg': 'User Registered!', 'User:': new_user.serialize()})


@app.route('/people', methods=['GET'])
def people():
    people = Characters.query.all()
    people_serialized = []
    
    for character in people:
        people_serialized.append(character.serialize())
    return jsonify({f'List of People:': people_serialized})
    
@app.route('/planets', methods=['GET'])
def planets():
    all_planets = Planets.query.all()
    planet_list_serialized = []
    for planetas in all_planets:  
        planet_list_serialized.append(planetas.serialize())
    return jsonify({'msg': planet_list_serialized}), 200
    
    
@app.route('/planets/<int:planet_id>', methods=['GET'])
def find_planet(planet_id):
    planet_query = Planets.query.get(planet_id)
    planets = Planets.query.all()
    
    planet_list = []
    for planet in planets:
        planet_list.append(planet.serialize())
    
    if planet_query is None:
        return jsonify({f'That planet ID doesnt exist, Here is the list with al planets':planet_list })
        
    
    return jsonify({'msg': planet_query.serialize()})


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favorite_charac(user_id):
    user = User.query.get(user_id)
    users_list =  User.query.all()
    returned_users = []
    for individual in users_list:
        returned_users.append(individual.serialize())
    
    if user is None:
        return jsonify({f'User with ID: {user_id} doesnt exist. Here is the list with registered Users': returned_users}), 404
    
    
    fav_chacs = user.favorites_characters_list
    fav_planets = user.favorites_planets_list
    fav_starships = user.favorites_starships_list
    
    fav_chacs_list = []
    for register in fav_chacs:
        character = register.people.serialize()
        like_id_character= register.id
        fav_chacs_list.append([character, {'like_id_register': like_id_character}])
        
    fav_planets_list = []
    for register in fav_planets:
        planets = register.planets.serialize()
        like_id_planets = planets.id
        fav_planets_list.append([planets, {'Like_id_register': like_id_planets}])
        
    fav_starships_list = []
    for register in fav_starships:
        starship = register.starships_list.serialize()
        like_id_starships = starship.id
        fav_starships_list.append([starship, {'Like_id_register': like_id_starships}])
    
    
    return jsonify({f'favorites planets of {user.username}:': fav_planets_list,
                    f'favorites characters of {user.username}:': fav_chacs_list,
                    f'favorites starships of {user.username}': fav_starships_list
                    })
    
    
@app.route('/favorite/<int:user_id>/people/<int:people_id>', methods=['POST'])
def add_favorite_character(user_id, people_id):
    user = User.query.get(user_id)
    people = Characters.query.get(people_id)
    
    if user is None or people is None:
        return jsonify({'msg': 'usuario o personaje no encontrado'}), 400
    

    
    new_fav_character= FavCharacters(user_id = user_id, character_id= people_id)
    db.session.add(new_fav_character)
    db.session.commit()
    
    
    
    return jsonify({'User': user.serialize(), 'liked': people.serialize()}), 200
    # return jsonify({'msg': 'Todo salio bien'}), 200



@app.route('/favorite/<int:user_id>/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    
    
    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)
    
    if user is None or planet is None:
        return jsonify({'msg': 'User or Planet does not exist'}), 400

    
    new_fav_planet = FavPlanets(user_id = user_id, planet_id = planet_id)
    db.session.add(new_fav_planet)
    db.session.commit()
    
    return jsonify({'User:': user.serialize(), 'liked:': planet.serialize()}), 200


@app.route('/favorite/<int:user_id>/people/<int:people_id>', methods=['DELETE'])
def delete_fav_people (user_id, people_id):
    
    user = User.query.get(user_id)
    
    user_favorites = user.favorites_characters_list
    
    user_favorites_list = []
    for register in user_favorites:
        favorite = register.id
        user_favorites_list.append(favorite)
    
    for like in user_favorites_list:
        if like == people_id:

            register_query = FavCharacters.query.filter_by(id=like).first()
            db.session.delete(register_query)
            db.session.commit()

            return jsonify({f'User: {user.username}' : 'Liked character deleted succesfully'}), 200
        else:
           return jsonify({f'User: {user.username}': 'Didnt like that character yet'}), 400
    
@app.route('/favorite/<int:user_id>/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet (user_id, planet_id):
    
    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)
    
    
    user_favorites = user.favorites_planets_list
    
    user_favorites_list = []
    for register in user_favorites:
        favorite = register.id
        user_favorites_list.append(favorite)
    
    for like in user_favorites_list:
        if like == planet_id:

            register_query = FavPlanets.query.filter_by(id=like).first()
            db.session.delete(register_query)
            db.session.commit()

            return jsonify({'msg': 'Liked planet deleted succesfully' }), 200
        else:
           return jsonify({'msg': 'Didnt like that character yet'}), 400


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
