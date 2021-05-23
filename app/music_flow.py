from app import create_app
from dotenv import load_dotenv
from os import getenv

load_dotenv('.env')

app = create_app(getenv('FLASK_CONFIG') or 'default')

@app.cli.command('hello')
def hello():
    print("hello")


@app.cli.command()
def test():
    """Run unittests"""
    import unittest
    tests = unittest.TestLoader().discover('app/tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
