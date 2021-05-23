# from flask.globals import session
from . import auth
from flask import render_template, redirect, request, url_for, flash, current_app, session
from flask_login import login_user, logout_user, current_user, login_required

from .forms import LoginForm, RegisterForm, UpdatePassForm, PassResetRequestForm, PassResetForm
from app.extensions import db
from app.helpers import send_email
from app.models import User


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.blueprint != 'auth' \
            and request.endpoint != 'status':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    current_app.logger.info('THIS IS A LOG MESSAGE!!!!')
    if current_user.is_authenticated:
        flash('You are already logged in!')
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            user.reset_pass_token = ''
            db.session.add(user)
            db.session.commit()
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have logged out!')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    try:
        # POST method
        if form.validate_on_submit():
            user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data)
            db.session.add(user)  
            db.session.commit()      
            token = user.generate_confirmation_token()
            send_email(user.email, 'Confirm your account',
                       'auth/email/confirm', user=user, token=token)
            flash_message = """Confirmation link sent to your email \
                               - Please confirm your email"""
            flash(flash_message)
            current_app.logger.info('New user added to the db')
            return redirect(url_for('main.index'))
    except Exception as e:
        current_app.logger.critical(str(e))
        current_app.logger.exception("Error Message: ")
        db.session.delete(user)
        db.session.commit()
        flash('an error occured, please try again later')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        flash('You have already confirmed your account')
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account!')
    else:
        flash('The confirmation link is invalid or has expired')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    try:
        token = current_user.generate_confirmation_token()
        send_email(current_user.email, 'Confirm your account',
                    'auth/email/confirm', user=current_user, token=token)
        flash_message = "A new confirmation link was sent to your \
                            email - Please confirm your email"
        flash(flash_message)
        current_app.logger.info('New user added to the db')
        return redirect(url_for('main.index'))
    except Exception as e:
        current_app.logger.critical(str(e))
        current_app.logger.exception("Error Message: ")
        flash('an error occured, please try again later')
        return redirect(url_for('main.index'))
    

@auth.route('/password-update', methods=["GET", "POST"])
@login_required
def password_update():
    form = UpdatePassForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash("Your password was updated.")
            return redirect(url_for('main.index'))
        else:
            flash("Invalid Password.")
    return render_template("auth/update_password.html", form=form)


@auth.route('/password-reset', methods=["GET", "POST"])
def password_reset_request():
    if not current_user.is_anonymous:
        flash("You're already logged in, try changing your password")
        return redirect(url_for('main.index'))
    form = PassResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, "Reset Your Password", 
                       "auth/email/reset_password_email",
                       user=user, token=token)
        flash_message = "If you have an account registered an email with \
                         instructions has been sent to you"
        flash(flash_message)
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password_request.html", form=form)


@auth.route('/password-reset/<email>/<token>', methods=["GET", "POST"])
def password_reset(email, token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PassResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash("Your password has been changed")
            return redirect(url_for('auth.login'))
        else:
            flash("Sorry, this link is no longer valid, please request another one")
            return redirect(url_for('main.index'))
    return render_template("auth/reset_password.html", email=email, form=form)
    