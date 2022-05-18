from flask_wtf import FlaskForm
from wtforms import DateField, StringField, PasswordField, TextAreaField, RadioField,IntegerField, DecimalField, SelectField,EmailField
from wtforms.validators import DataRequired, Email, Length
import email_validator

class SearchForm(FlaskForm):
    """Form for searching by area"""
    text = StringField('Keyword' , validators = [DataRequired()])
    e_city = StringField('City name' , validators = [DataRequired()])
   
class CommentForm(FlaskForm):
    """Form for adding/editing comments for events"""
    
    city = StringField('City' , validators = [DataRequired()])
    eventname = StringField('Event name' , validators = [DataRequired()])
    text = TextAreaField('text' , validators=[DataRequired()])

class SignUpForm(FlaskForm):
    """Form for adding users"""

    username = StringField('Username' , validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    img_url = StringField('(Optional) Image URL')
    first_name = StringField('First Name' , validators=[DataRequired()])
    last_name  = StringField('Last Name' , validators=[DataRequired()])

class UserEditForm(FlaskForm):
    """Form for editing users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    img_url = StringField('(Optional) Image URL')
    password = PasswordField('Password', validators=[Length(min=6)])

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6), DataRequired()])

class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""

class WishlistForm(FlaskForm):
    wishlistname = StringField('Your Event List name' , validators=[DataRequired()])