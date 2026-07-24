from flask import Blueprint, request, jsonify
from app import db
from models.hotel import Hotel
from models.user import User
from utils.auth import token_required

bp = Blueprint('hotel', __name__, url_prefix='/api/hotel')

@bp.route('/create', methods=['POST'])
@token_required
def create_hotel(current_user):
    """Create hotel profile"""
    try:
        data = request.get_json()
        
        if not data.get('name'):
            return jsonify({'error': 'Hotel name is required'}), 400
        
        hotel = Hotel(
            name=data['name'],
            description=data.get('description'),
            phone_number=data.get('phone_number'),
            email=data.get('email'),
            address=data.get('address'),
            city=data.get('city'),
            state=data.get('state'),
            zipcode=data.get('zipcode'),
            country=data.get('country'),
            total_rooms=data.get('total_rooms', 0),
            check_in_time=data.get('check_in_time', '14:00'),
            check_out_time=data.get('check_out_time', '11:00'),
            currency=data.get('currency', 'USD')
        )
        
        db.session.add(hotel)
        db.session.commit()
        
        # Link hotel to user
        current_user.hotel_id = hotel.id
        db.session.commit()
        
        return jsonify({
            'message': 'Hotel created successfully',
            'hotel': hotel.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:hotel_id>', methods=['GET'])
@token_required
def get_hotel(current_user, hotel_id):
    """Get hotel details"""
    try:
        hotel = Hotel.query.get(hotel_id)
        
        if not hotel:
            return jsonify({'error': 'Hotel not found'}), 404
        
        return jsonify(hotel.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:hotel_id>', methods=['PUT'])
@token_required
def update_hotel(current_user, hotel_id):
    """Update hotel details"""
    try:
        hotel = Hotel.query.get(hotel_id)
        
        if not hotel:
            return jsonify({'error': 'Hotel not found'}), 404
        
        # Verify ownership
        if current_user.hotel_id != hotel_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        for key, value in data.items():
            if hasattr(hotel, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(hotel, key, value)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Hotel updated successfully',
            'hotel': hotel.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
