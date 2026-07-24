from app import db
from datetime import datetime, timedelta
import random
import string

class OTP(db.Model):
    __tablename__ = 'otps'
    
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(15), nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    attempts = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=10))
    
    def is_expired(self):
        return datetime.utcnow() > self.expires_at
    
    @staticmethod
    def generate_otp():
        return ''.join(random.choices(string.digits, k=6))
    
    def to_dict(self):
        return {
            'id': self.id,
            'phone_number': self.phone_number,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat()
        }
