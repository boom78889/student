from flask import Blueprint, request, jsonify
from app import db
from models.menu import Menu
from models.hotel import Hotel
from utils.auth import token_required

bp = Blueprint('menu', __name__, url_prefix='/api/menu')

@bp.route('/create', methods=['POST'])
@token_required
def create_menu_item(current_user):
    """Create menu item"""
    try:
        if not current_user.hotel_id:
            return jsonify({'error': 'Hotel not found for user'}), 404
        
        data = request.get_json()
        
        if not data.get('name') or not data.get('price'):
            return jsonify({'error': 'Name and price are required'}), 400
        
        menu = Menu(
            hotel_id=current_user.hotel_id,
            name=data['name'],
            description=data.get('description'),
            category=data.get('category'),
            price=data['price'],
            availability=data.get('availability', True),
            image_url=data.get('image_url'),
            preparation_time=data.get('preparation_time'),
            is_vegetarian=data.get('is_vegetarian', False),
            is_vegan=data.get('is_vegan', False)
        )
        
        db.session.add(menu)
        db.session.commit()
        
        return jsonify({
            'message': 'Menu item created successfully',
            'menu': menu.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/list', methods=['GET'])
@token_required
def list_menu(current_user):
    """List all menu items for hotel"""
    try:
        if not current_user.hotel_id:
            return jsonify({'error': 'Hotel not found for user'}), 404
        
        menus = Menu.query.filter_by(hotel_id=current_user.hotel_id).all()
        
        return jsonify({
            'menus': [menu.to_dict() for menu in menus]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:menu_id>', methods=['PUT'])
@token_required
def update_menu(current_user, menu_id):
    """Update menu item"""
    try:
        menu = Menu.query.get(menu_id)
        
        if not menu:
            return jsonify({'error': 'Menu item not found'}), 404
        
        if menu.hotel_id != current_user.hotel_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        for key, value in data.items():
            if hasattr(menu, key) and key not in ['id', 'hotel_id', 'created_at', 'updated_at']:
                setattr(menu, key, value)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Menu item updated successfully',
            'menu': menu.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:menu_id>', methods=['DELETE'])
@token_required
def delete_menu(current_user, menu_id):
    """Delete menu item"""
    try:
        menu = Menu.query.get(menu_id)
        
        if not menu:
            return jsonify({'error': 'Menu item not found'}), 404
        
        if menu.hotel_id != current_user.hotel_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        db.session.delete(menu)
        db.session.commit()
        
        return jsonify({'message': 'Menu item deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
