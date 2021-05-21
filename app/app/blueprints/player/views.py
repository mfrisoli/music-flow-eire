from flask import render_template
from flask_login import login_required
# from app.extensions import db
from . import player

@player.route('/')
@login_required
def player_home():
    return render_template('player/player_index.html')