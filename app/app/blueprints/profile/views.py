from flask import render_template
# from app.extensions import db
from . import profile

@profile.route('/')
def profile_home():
    return render_template('profile/profile_index.html')