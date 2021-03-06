import unittest
from app import create_app, db
from app.models import User



class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password='foo')
        self.assertTrue(u.password_hash is not None)
    

    def test_no_password_getter(self):
        u = User(password='foo')
        with self.assertRaises(AttributeError):
            u.password
        

    def test_password_verification(self):
        u = User(password='foo')
        self.assertTrue(u.verify_password('foo'))
        self.assertFalse(u.verify_password('boo'))


    def test_password_salts_are_random(self):
        u = User(password='foo')
        u2 = User(password='foo')
        self.assertTrue(u.password_hash != u2.password_hash)


    def test_confirmation_token(self):
        u = User(password='foo')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

