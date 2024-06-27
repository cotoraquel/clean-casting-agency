import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import setup_db, db, Movie, Actor
from auth import requires_auth, AuthError
from datetime import datetime

def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = os.environ.get('APP_SECRET_KEY', 'default_secret_key') 
    setup_db(app)
    CORS(app)

    Migrate(app, db)  # Initialize Flask-Migrate

    def is_not_integer(value):
        return not isinstance(value, int)

    @app.route('/actors', methods=['GET'])
    @requires_auth('read:actors')
    def get_actors():
            try:
                actors = Actor.query.all()
                return jsonify({
                    'success': True,
                    'actors': [actor.format() for actor in actors]
                })
            except Exception as e: 
                abort(e.code)

    @app.route('/movies', methods=['GET'])
    @requires_auth('read:movies')
    def get_movies():
        try:
            movies = Movie.query.all()
            return jsonify({
                'success': True,
                'movies': [movie.format() for movie in movies]
            })
        except Exception as e: 
            abort(e.code)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(actor_id):
        try:
            actor = Actor.query.get(actor_id)
            if actor is None:
                abort(404, description="Actor not found.")
            actor.delete()
            return jsonify({
                'success': True,
                'delete': actor_id
            })
        except Exception as e:
            abort(500, description="Internal server error.")

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(movie_id):
        try:
            movie = Movie.query.get(movie_id)
            if movie is None:
                abort(404, description="Movie not found.")
            movie.delete()
            return jsonify({
                'success': True,
                'delete': movie_id
            })
        except Exception as e:
            abort(500, description="Internal server error.")

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor():
        data = request.get_json()
        name = data.get('name', None)
        age = data.get('age', None)
        gender = data.get('gender', None)

        if None in [name, age, gender]:
            abort(400)

        try:
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()
            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        except Exception as e: 
            abort(e.code)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie():
        data = request.get_json()
        title = data.get('title', None)
        release_date = data.get('release_date', None)

        if None in [title, release_date]:
            abort(400)

        try:
            movie = Movie(title=title, release_date=datetime.strptime(release_date, '%Y-%m-%d'))
            movie.insert()
            return jsonify({
                'success': True,
                'movie': movie.format()
            })
        except Exception as e:
            abort(e.code)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(actor_id):
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)

        data = request.get_json()
        if 'name' in data:
            actor.name = data['name']
        if 'age' in data:
            actor.age = data['age']
        if 'gender' in data:
            actor.gender = data['gender']

        try:
            actor.update()
            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        except Exception as e: 
            abort(e.code)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(movie_id):
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)

        data = request.get_json()
        if 'title' in data:
            movie.title = data['title']
        if 'release_date' in data:
            movie.release_date = datetime.strptime(data['release_date'], '%Y-%m-%d')

        try:
            movie.update()
            return jsonify({
                'success': True,
                'movie': movie.format()
            })
        except Exception as e: 
            abort(e.code)
            

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed'
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error.'
        }), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
