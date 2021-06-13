from flask import render_template, redirect, request, url_for, flash, current_app, session
from flask_login import login_user, logout_user, current_user, login_required

from app.extensions import db
from app.models import Song

from flask import render_template
from . import library

import eyed3
from os import listdir, path

@library.route('/')
def library_home():

    # TODO return list of 10 songs

    return render_template('library/library_index.html')


@library.route('/refresh_db')
@login_required
def refresh_db():

    Song.query.delete()
    
    music_dir = current_app.config['MUSIC_DIRECTORY']
    # Get all file names in music directory
    song_files = listdir(music_dir)

    songs_added = 0

    current_app.logger.info(song_files)

    for file in song_files:

        if file[-4:] !=".mp3":
            continue

        current_app.logger.info('Updating songs in Database')

        # Load File
        audiofile = eyed3.load(path.join(music_dir, file))
        current_app.logger.info(audiofile.tag.genre)
        current_app.logger.info(audiofile.tag.getBestDate())
        audiofile.tag.getBestDate()

        song = Song(
            song_name = audiofile.tag.title,
            artist = audiofile.tag.artist,
            album = audiofile.tag.album or None,
            year = str(audiofile.tag.getBestDate()) or None,
            genre = str(audiofile.tag.genre) or None,
            filename = file
        )
        db.session.add(song)
        db.session.commit()
        songs_added += 1
    
    songs_found = len(song_files)

    message = f"Total files found {songs_found} and songs added {songs_added}"

    return message
    