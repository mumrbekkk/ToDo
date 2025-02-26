from flask_wtf import FlaskForm
from wtforms.fields.datetime import DateTimeLocalField
from wtforms.fields.simple import StringField, TextAreaField, SubmitField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Length, Optional


class EditTemplateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Update')

class AddTemplateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AddTask(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    start_date = DateTimeLocalField('Start date', validators=[Optional()])
    end_date = DateTimeLocalField('End date', validators=[Optional()])
    submit = SubmitField('Add ToDo')

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                                 Length(min=8, message='Password must be at least 8 characters')
                             ])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

