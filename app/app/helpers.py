from flask_mail import Message
from flask import render_template, current_app
from .config import config, config_name
from .extensions import mail
from threading import Thread
from app.models import Song
from app.extensions import db
import eyed3
from os import listdir, path


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):

    MUSIC_FLOW_MAIL_SUBJECT_PREFIX = \
        config[config_name]().MUSIC_FLOW_MAIL_SUBJECT_PREFIX

    MUSIC_FLOW_MAIL_SENDER = \
        config[config_name]().MUSIC_FLOW_MAIL_SENDER
    
    app = current_app._get_current_object()

    msg = Message(MUSIC_FLOW_MAIL_SUBJECT_PREFIX + ' ' + subject,
                  sender=MUSIC_FLOW_MAIL_SENDER, recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def rewrite_music_db():
    
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