from app.helpers import rewrite_music_db
from flask import render_template, redirect, request, url_for, flash, current_app, session
from flask_login import login_user, logout_user, current_user, login_required

from app.extensions import db
from app.models import Song

from flask import render_template
from . import library


@library.route('/')
def library_home():

    # TODO return list of 10 songs

    return render_template('library/library_index.html')


@library.route('/refresh_db')
@login_required
def refresh_db():
   
    
    return rewrite_music_db()
    