import unittest
from flask_testing import TestCase
from app import app, db
from app.models import User


class UnitTests(unittest.TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def test_connect_manager_page(self):
        response = app.test_client(self).get('/app/manager')
        self.assertEqual(response.status_code, 404)

    def test_wrong_login_without_id(self):
        login = app.test_client(self).post('login', data=dict(first_name='tomer', last_name='admon'))
        self.assertEqual(login.status_code, 400)

    def test_login_with_user_not_exist(self):
        login = app.test_client(self).post('login', data=dict(first_name='aba', last_name='aca', id=900))
        loginString = login.data.decode('utf-8')
        assert 'User not found!' in loginString

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

if (__name__ == '__main__'):
    unittest.main()
