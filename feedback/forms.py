from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from feedback.models import Registration

class FeedbackForm(FlaskForm):
    customer = StringField('Customer Name', validators = [DataRequired()])
    dealer = StringField('Dealer', validators = [DataRequired()])
    rating = StringField('Rating', validators = [DataRequired()])
    comments = TextAreaField('Comments', validators = [DataRequired()])
    submit = SubmitField('Post')

class RegistrationForm(FlaskForm):    
    fullname = StringField('Full Name', validators= [DataRequired()])
    email = StringField('Email', validators= [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = Registration.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please try another one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators= [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):    
    fullname = StringField('Full Name', validators= [DataRequired()])
    email = StringField('Email', validators= [DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators = [FileAllowed(
                ['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Registration.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please try another one.')


