from app import db
from datetime import datetime

class Menu(db.Model):
    __tablename__ = 'menus'
    
    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # e.g., Breakfast, Lunch, Dinner, Snacks
    price = db.Column(db.Float, nullable=False)
    availability = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(255))
    preparation_time = db.Column(db.Integer)  # in minutes
    is_vegetarian = db.Column(db.Boolean, default=False)
    is_vegan = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'hotel_id': self.hotel_id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'price': self.price,
            'availability': self.availability,
            'image_url': self.image_url,
            'preparation_time': self.preparation_time,
            'is_vegetarian': self.is_vegetarian,
            'is_vegan': self.is_vegan,
            'created_at': self.created_at.isoformat()
        }
