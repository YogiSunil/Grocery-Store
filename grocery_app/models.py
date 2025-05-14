from grocery_app.extensions import db
from grocery_app.utils import FormEnum
from flask_login import UserMixin

# Bridge table for shopping list
shopping_list_table = db.Table(
    'shopping_list', db.Column('user_id', db.Integer,
                               db.ForeignKey('user.id')),
    db.Column('item_id', db.Integer, db.ForeignKey('grocery_item.id')))


class ItemCategory(FormEnum):
    """Categories of grocery items."""
    PRODUCE = 'Produce'
    DELI = 'Deli'
    BAKERY = 'Bakery'
    PANTRY = 'Pantry'
    FROZEN = 'Frozen'
    REFRIGERATED = 'Refrigerated'
    COSMETICS = 'Cosmetics'
    PERSONAL_CARE = 'Personal Care'
    HOUSEHOLD = 'Household'
    PET_SUPPLIES = 'Pet Supplies'
    CLOTHING = 'Clothing'
    ELECTRONICS = 'Electronics'
    TOYS = 'Toys'
    BOOKS = 'Books'
    SPORTS = 'Sports'
    AUTOMOTIVE = 'Automotive'
    BEAUTY = 'Beauty'
    HEALTH = 'Health'
    OFFICE = 'Office'
    GARDEN = 'Garden'
    HOME_IMPROVEMENT = 'Home Improvement'
    FURNITURE = 'Furniture'
    JEWELRY = 'Jewelry'
    LUGGAGE = 'Luggage'
    Fruit = 'Fruit'
    OTHER = 'Other'


class User(UserMixin, db.Model):
    """User model for storing user data"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    shopping_list_items = db.relationship('GroceryItem',
                                          secondary=shopping_list_table,
                                          backref='in_shopping_lists')


class GroceryStore(db.Model):
    """Grocery Store model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')
    items = db.relationship('GroceryItem', back_populates='store')


class GroceryItem(db.Model):
    """Grocery Item model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.Enum(ItemCategory), default=ItemCategory.OTHER)

    photo_url = db.Column(db.String(200))
    store_id = db.Column(db.Integer,
                         db.ForeignKey('grocery_store.id'),
                         nullable=False)
    store = db.relationship('GroceryStore', back_populates='items')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')

