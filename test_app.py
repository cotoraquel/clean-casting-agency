import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor


# Mock headers with JWT tokens (These tokens should be generated using your authentication provider)
CASTING_ASSISTANT_HEADER = {
    'Authorization': f"Bearer {os.environ.get('CASTING_ASSISTANT')}"
}
CASTING_DIRECTOR_HEADER = {
    'Authorization': f"Bearer {os.environ.get('CASTING_DIRECTOR')}"
}
EXECUTIVE_PRODUCER_HEADER = {
    'Authorization': f"Bearer {os.environ.get('EXECUTIVE_PRODUCER')}"
}

class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_redux"
        self.database_path = os.environ.get('DATABASE_URL')
        setup_db(self.app, self.database_path)

        self.new_actor = {
            'name': 'John Doe',
            'age': 30,
            'gender': 'Male'
        }

        self.new_movie = {
            'title': 'New Movie',
            'release_date': '2024-01-01'
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    # Success and error tests for each endpoint
    def test_get_actors_success(self):
        res = self.client().get('/actors', headers=CASTING_ASSISTANT_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_actor_unauthorized(self):
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        

    def test_get_movies_success(self):
        res = self.client().get('/movies', headers=CASTING_ASSISTANT_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    def test_get_movies_unauthorized(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
 
    def test_create_actor_success(self):
        res = self.client().post('/actors', json=self.new_actor, headers=EXECUTIVE_PRODUCER_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
     
    def test_create_actor_unauthorized(self):
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        
    def test_create_actor_bad_request(self):
        res = self.client().post('/actors', json={}, headers=EXECUTIVE_PRODUCER_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_create_movie_success(self):
        res = self.client().post('/movies', json=self.new_movie, headers=EXECUTIVE_PRODUCER_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
    def test_create_movie_unauthorized(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
      

    def test_create_movie_bad_request(self):
        res = self.client().post('/movies', json={}, headers=EXECUTIVE_PRODUCER_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_update_actor_success(self):
        res = self.client().post('/actors', json=self.new_actor, headers=EXECUTIVE_PRODUCER_HEADER)
        actor_id = json.loads(res.data)['actor']['id']
        res = self.client().patch(f'/actors/{actor_id}', json={'name': 'Jane Doe'}, headers=EXECUTIVE_PRODUCER_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_actor_unauthorized(self):
        res = self.client().patch('/actors/1', json={'name': 'Jane Doe'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        

    def test_update_actor_not_found(self):
        res = self.client().patch('/actors/1000', json={'name': 'Jane Doe'}, headers=EXECUTIVE_PRODUCER_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_update_movie_success(self):
        res = self.client().post('/movies', json=self.new_movie, headers=EXECUTIVE_PRODUCER_HEADER)
        movie_id = json.loads(res.data)['movie']['id']
        res = self.client().patch(f'/movies/{movie_id}', json={'title': 'Updated Movie'}, headers=EXECUTIVE_PRODUCER_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_movie_unauthorized(self):
        res = self.client().patch('/movies/1', json={'title': 'Updated Movie'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        
    def test_update_movie_not_found(self):
        res = self.client().patch('/movies/1000', json={'title': 'Updated Movie'}, headers=EXECUTIVE_PRODUCER_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_actor_success(self):
        res = self.client().post('/actors', json=self.new_actor, headers=EXECUTIVE_PRODUCER_HEADER)
        actor_id = json.loads(res.data)['actor']['id']
        res = self.client().delete(f'/actors/{actor_id}', headers=EXECUTIVE_PRODUCER_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # def test_delete_actor_unauthorized(self):
    #     res = self.client().delete('/actors/1')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 401)
    #     self.assertEqual(data['success'], False)

    def test_delete_actor_not_found(self):
        res = self.client().delete('/actors/1000', headers=EXECUTIVE_PRODUCER_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)

    def test_delete_movie_success(self):
        res = self.client().post('/movies', json=self.new_movie, headers=EXECUTIVE_PRODUCER_HEADER)
        movie_id = json.loads(res.data)['movie']['id']
        res = self.client().delete(f'/movies/{movie_id}', headers=EXECUTIVE_PRODUCER_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # def test_delete_movie_unauthorized(self):
    #     res = self.client().delete('/movies/1')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 401)
    #     self.assertEqual(data['success'], False)

    def test_delete_movie_not_found(self):
        res = self.client().delete('/movies/1000', headers=EXECUTIVE_PRODUCER_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)

    # RBAC tests
    def test_casting_assistant_get_actors(self):
        res = self.client().get('/actors', headers=CASTING_ASSISTANT_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_casting_assistant_get_movies(self):
        res = self.client().get('/movies', headers=CASTING_ASSISTANT_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #def test_casting_assistant_unauthorized_create_actor(self):
        #res = self.client().post('/actors', json=self.new_actor, headers=CASTING_ASSISTANT_HEADER)
        #data = json.loads(res.data)
        #self.assertEqual(res.status_code, 403)
        #self.assertEqual(data['success'], False)

    # def test_casting_assistant_unauthorized_delete_movie(self):
    #     res = self.client().delete('/movies/1', headers=CASTING_ASSISTANT_HEADER)
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 403)
    #     self.assertEqual(data['success'], False)

    def test_executive_producer_create_actor(self):
        res = self.client().post('/actors', json=self.new_actor, headers=EXECUTIVE_PRODUCER_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_executive_producer_delete_movie(self):
        res = self.client().post('/movies', json=self.new_movie, headers=EXECUTIVE_PRODUCER_HEADER)
        movie_id = json.loads(res.data)['movie']['id']
        res = self.client().delete(f'/movies/{movie_id}', headers=EXECUTIVE_PRODUCER_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Error handling tests
    def test_404_error(self):
        res = self.client().get('/nonexistent', headers=CASTING_ASSISTANT_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_400_error(self):
        res = self.client().post('/actors', json={}, headers=EXECUTIVE_PRODUCER_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    def test_405_error(self):
        res = self.client().post('/actors/1', json=self.new_actor, headers=EXECUTIVE_PRODUCER_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    def test_500_error(self):
        res = self.client().delete('/actors/1000', headers=EXECUTIVE_PRODUCER_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Internal server error.')


if __name__ == "__main__":
    unittest.main()
