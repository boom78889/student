from flask import Blueprint, request, jsonify
from app import db
from models.billing import Billing, Invoice
from models.user import User
from utils.auth import token_required
from datetime import datetime

bp = Blueprint('billing', __name__, url_prefix='/api/billing')

@bp.route('/create', methods=['POST'])
@token_required
def create_billing(current_user):
    """Create new billing record"""
    try:
        if not current_user.hotel_id:
            return jsonify({'error': 'Hotel not found for user'}), 404
        
        data = request.get_json()
        
        if not data.get('guest_name'):
            return jsonify({'error': 'Guest name is required'}), 400
        
        billing = Billing(
            hotel_id=current_user.hotel_id,
            guest_name=data['guest_name'],
            guest_email=data.get('guest_email'),
            guest_phone=data.get('guest_phone'),
            check_in_date=datetime.fromisoformat(data['check_in_date']) if data.get('check_in_date') else None,
            check_out_date=datetime.fromisoformat(data['check_out_date']) if data.get('check_out_date') else None,
            room_number=data.get('room_number'),
            total_amount=data.get('total_amount', 0),
            balance=data.get('total_amount', 0)
        )
        
        db.session.add(billing)
        db.session.commit()
        
        return jsonify({
            'message': 'Billing record created successfully',
            'billing': billing.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/list', methods=['GET'])
@token_required
def list_billings(current_user):
    """List all billing records for hotel"""
    try:
        if not current_user.hotel_id:
            return jsonify({'error': 'Hotel not found for user'}), 404
        
        billings = Billing.query.filter_by(hotel_id=current_user.hotel_id).all()
        
        return jsonify({
            'billings': [billing.to_dict() for billing in billings]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:billing_id>/add-invoice', methods=['POST'])
@token_required
def add_invoice(current_user, billing_id):
    """Add invoice to billing"""
    try:
        billing = Billing.query.get(billing_id)
        
        if not billing:
            return jsonify({'error': 'Billing record not found'}), 404
        
        if billing.hotel_id != current_user.hotel_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        invoice = Invoice(
            billing_id=billing_id,
            invoice_number=data.get('invoice_number'),
            item_description=data['item_description'],
            quantity=data.get('quantity', 1),
            unit_price=data['unit_price'],
            total_price=data.get('quantity', 1) * data['unit_price']
        )
        
        # Update billing total
        billing.total_amount += invoice.total_price
        billing.balance = billing.total_amount - billing.paid_amount
        
        db.session.add(invoice)
        db.session.commit()
        
        return jsonify({
            'message': 'Invoice added successfully',
            'invoice': invoice.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:billing_id>/payment', methods=['POST'])
@token_required
def record_payment(current_user, billing_id):
    """Record payment for billing"""
    try:
        billing = Billing.query.get(billing_id)
        
        if not billing:
            return jsonify({'error': 'Billing record not found'}), 404
        
        if billing.hotel_id != current_user.hotel_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        payment_amount = data.get('amount', 0)
        
        billing.paid_amount += payment_amount
        billing.balance = billing.total_amount - billing.paid_amount
        
        if billing.balance <= 0:
            billing.status = 'paid'
        else:
            billing.status = 'partial'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Payment recorded successfully',
            'billing': billing.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
