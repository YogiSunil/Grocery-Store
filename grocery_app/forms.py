
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField, PasswordField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from grocery_app.models import GroceryStore, ItemCategory, User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""
    title = StringField('Store Title', 
        validators=[DataRequired(), Length(min=3, max=80)])
    address = StringField('Store Address',
        validators=[DataRequired(), Length(min=3, max=200)])
    submit = SubmitField('Submit')

class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""
    name = StringField('Item Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    price = FloatField('Price', validators=[DataRequired()])
    category = SelectField('Category', choices=[(cat.name, cat.value) for cat in ItemCategory])
    photo_url = StringField('Photo URL', validators=[URL()])
    store = QuerySelectField('Store',
        query_factory=lambda: GroceryStore.query.all(),
        get_label='title')
    submit = SubmitField('Submit')

class SignUpForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email',
        validators=[DataRequired(), Length(min=5, max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
