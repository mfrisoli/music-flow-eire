from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), 
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Username must have only letters or numbers')])
    password = PasswordField('Password', validators=[
                    DataRequired(), 
                    EqualTo('password2', 
                    message="Passwords don't match")])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already exists')


    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists')


class UpdatePassForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
                        DataRequired(),
                        EqualTo('new_password2', 
                        message="Passwords don't match")])
    new_password2 = PasswordField('Confirm new password', validators=[DataRequired()])
    submit = SubmitField('Update')


class PassResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), 
                                             Email()])
    submit = SubmitField('Send')                 


class PassResetForm(FlaskForm):
    password = PasswordField('New Password', validators=[
                        DataRequired(),
                        EqualTo('password2', 
                        message="Passwords don't match")])
    password2 = PasswordField('Confirm new password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

