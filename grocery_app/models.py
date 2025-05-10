from grocery_app.extensions import db
from grocery_app.utils import FormEnum


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


class GroceryStore(db.Model):
    """Grocery Store model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    items = db.relationship('GroceryItem', back_populates='store')


class GroceryItem(db.Model):
    """Grocery Item model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    category = db.Column(db.Enum(ItemCategory), default=ItemCategory.OTHER)
    photo_url = db.Column(db.String)
    store_id = db.Column(db.Integer,
                         db.ForeignKey('grocery_store.id'),
                         nullable=False)
    store = db.relationship('GroceryStore', back_populates='items')