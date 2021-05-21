from flask_mail import Message
from flask import render_template
from .config import config, config_name
from .extensions import mail


def send_email(to, subject, template, **kwargs):

    MUSIC_FLOW_MAIL_SUBJECT_PREFIX = \
        config[config_name]().MUSIC_FLOW_MAIL_SUBJECT_PREFIX

    MUSIC_FLOW_MAIL_SENDER = \
        config[config_name]().MUSIC_FLOW_MAIL_SENDER

    msg = Message(MUSIC_FLOW_MAIL_SUBJECT_PREFIX + subject,
                  sender=MUSIC_FLOW_MAIL_SENDER, recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)