from app import db
from datetime import datetime
import uuid

class Billing(db.Model):
    __tablename__ = 'billings'
    
    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'), nullable=False)
    guest_name = db.Column(db.String(150), nullable=False)
    guest_email = db.Column(db.String(120))
    guest_phone = db.Column(db.String(15))
    check_in_date = db.Column(db.DateTime)
    check_out_date = db.Column(db.DateTime)
    room_number = db.Column(db.String(20))
    total_amount = db.Column(db.Float, default=0)
    paid_amount = db.Column(db.Float, default=0)
    balance = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='pending')  # pending, paid, partial
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    invoices = db.relationship('Invoice', backref='billing', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'hotel_id': self.hotel_id,
            'guest_name': self.guest_name,
            'guest_email': self.guest_email,
            'guest_phone': self.guest_phone,
            'check_in_date': self.check_in_date.isoformat() if self.check_in_date else None,
            'check_out_date': self.check_out_date.isoformat() if self.check_out_date else None,
            'room_number': self.room_number,
            'total_amount': self.total_amount,
            'paid_amount': self.paid_amount,
            'balance': self.balance,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

class Invoice(db.Model):
    __tablename__ = 'invoices'
    
    id = db.Column(db.Integer, primary_key=True)
    billing_id = db.Column(db.Integer, db.ForeignKey('billings.id'), nullable=False)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    item_description = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'billing_id': self.billing_id,
            'invoice_number': self.invoice_number,
            'item_description': self.item_description,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total_price': self.total_price,
            'created_at': self.created_at.isoformat()
        }
