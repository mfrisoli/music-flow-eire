from flask_mail import Message
from flask import render_template, current_app
from .config import config, config_name
from .extensions import mail
from threading import Thread

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

