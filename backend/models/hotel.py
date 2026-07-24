from app import db
from datetime import datetime

class Hotel(db.Model):
    __tablename__ = 'hotels'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    phone_number = db.Column(db.String(15))
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zipcode = db.Column(db.String(10))
    country = db.Column(db.String(100))
    logo_url = db.Column(db.String(255))
    total_rooms = db.Column(db.Integer, default=0)
    check_in_time = db.Column(db.String(10), default='14:00')
    check_out_time = db.Column(db.String(10), default='11:00')
    currency = db.Column(db.String(3), default='USD')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    menus = db.relationship('Menu', backref='hotel', cascade='all, delete-orphan')
    billings = db.relationship('Billing', backref='hotel', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'phone_number': self.phone_number,
            'email': self.email,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode,
            'country': self.country,
            'logo_url': self.logo_url,
            'total_rooms': self.total_rooms,
            'check_in_time': self.check_in_time,
            'check_out_time': self.check_out_time,
            'currency': self.currency,
            'created_at': self.created_at.isoformat()
        }
