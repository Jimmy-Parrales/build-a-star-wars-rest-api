from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User , Planet , People
from api.utils import generate_sitemap, APIException

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/user', methods=['GET'])
def get_user():
	users = User.query.all()
	users = list(map(lambda user: user.serialize(),users))
	print(users)
	return jsonify(users), 200

@api.route('/user/<user_id>', methods=['PUT'])
def resgister_user(user_id):
	body = request.json
	user = User.query.get(user_id)
	if not (isinstance(user, User)):
		user = User()

	user.email = body["email"]
	user.password = body["password"]
	user.is_active = body["is_active"]

	db.session.add(user)
	try:        
		db.session.commit()
		return jsonify(user.serialize()), 201
	except Exception as error:
		print(error)
		db.session.rollback()
		return jsonify({"message":error}), 400

@api.route('/planet', methods=['GET'])
def get_planets():
  planets = Planet.query.all()
  planets = list(map(lambda planet: planet.serialize(),planets))
  print(planets)
  return jsonify(planets), 200

@api.route('/planet/<planet_id>', methods=['GET'])
def get_planet(planet_id):
	planet = Planet.query.get(planet_id)
	if isinstance(planet, Planet):
			return jsonify(planet.internal()), 200
	else:
			return jsonify({
					"message":"Planeta no encontrado"
			})

@api.route('/planet', methods=['POST'])
def register_planet():
	
	planet = Planet()
	body = request.json
	
	planet.name = body["name"]
	planet.climate = body["climate"]
	planet.created = body["created"]
	planet.diameter= body["diameter"]
	planet.gravity = body["gravity"]
	planet.orbital_period = body["orbital_period"]

	db.session.add(planet)
	try:        
			db.session.commit()
			return jsonify(planet.serialize()), 201
	except Exception as error:
			print(error)
			db.session.rollback()
			return jsonify({"message":error}), 400

@api.route('/planet/<planet_id>', methods=['PUT'])
def full_update_planet(planet_id):
	body = request.json
	planet = Planet.query.get(planet_id)
	if not (isinstance(planet, Planet)):
		planet = Planet();

	planet.climate = body["climate"]
	planet.created = body["created"]
	planet.diameter= body["diameter"]
	planet.gravity = body["gravity"]
	planet.name = body["name"]
	planet.orbital_period = body["orbital_period"]
	
	db.session.add(planet)
	try:        
		db.session.commit()
		return jsonify(planet.serialize()), 200
	except Exception as error:
		print(error)
		db.session.rollback()
		return jsonify({"message":error}), 400

@api.route('/planet/<planet_id>', methods=['PATCH'])
def partial_update_planet(planet_id):
	body = request.json
	planet = Planet.query.get(planet_id)
	for field in body:
		setattr(planet, field, body[field])
	
	db.session.add(planet)
	try:        
		db.session.commit()
		return jsonify(planet.serialize()), 200
	except Exception as error:
		print(error)
		db.session.rollback()
		return jsonify({"message":error}), 400

@api.route('/planet/<planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
	planet = Planet.query.get(planet_id)
	db.session.delete(planet)
	try:        
		db.session.commit()
		return jsonify( {"message":"Registro eliminado"}), 200
	except Exception as error:
		print(error)
		db.session.rollback()
		return jsonify({"message":error}), 400

@api.route('/people', methods=['GET'])
def get_peoples():
  peoples = People.query.all()
  peoples = list(map(lambda people: people.serialize(),peoples))
  print(peoples)
  return jsonify(peoples), 200

@api.route('/people/<people_id>', methods=['GET'])
def get_people(people_id):
	people = People.query.get(people_id)
	if isinstance(people, People):
			return jsonify(people.internal()), 200
	else:
			return jsonify({
					"message":"Persona no encontrada"
			})

@api.route('/people/<people_id>', methods=['PUT'])
def full_update_people(people_id):
	body = request.json
	people = People.query.get(people_id)
	if not (isinstance(people, People)):
		people = People();

	people.name = body["name"]
	people.gender = body["gender"]
	people.birth_year= body["birth_year"]
	
	db.session.add(people)
	try:        
		db.session.commit()
		return jsonify(people.serialize()), 200
	except Exception as error:
		print(error)
		db.session.rollback()
		return jsonify({"message":error}), 400