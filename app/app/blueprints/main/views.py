from flask import Flask, render_template, redirect, url_for, session, flash
from flask_mail import Message
from datetime import datetime
from app.forms import NameForm
from . import main

from app.helpers import send_email
from app.extensions import db

import os
from app.models import User, Role


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            flash('Welcome New user!!!')
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if app.config['MUSIC_FLOW_ADMIN']:
                send_email(app.config['MUSIC_FLOW_ADMIN'], ' New User', 'mail/new_user', user=user)
            else:
                session['known'] = True
            session['name'] = form.name.data
            form.name.data = ''
        else:
            flash('Welcome Old user!!!')
            session['name'] = form.name.data
            form.name.data = ''
        return redirect(url_for('main.index'))
    return render_template('index.html', current_time=datetime.utcnow(),
                            form=form, name=session.get('name'), known=session.get('known', False))


@main.route('/test')
def test():
    return str(os.getenv('FLASK_CONFIG'))