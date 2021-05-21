from flask import Blueprint

player = Blueprint('player', __name__, url_prefix='/player')

from . import views