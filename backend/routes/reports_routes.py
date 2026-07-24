from flask import Blueprint, request, jsonify
from app import db
from models.billing import Billing
from models.menu import Menu
from utils.auth import token_required
from sqlalchemy import func
from datetime import datetime, timedelta

bp = Blueprint('reports', __name__, url_prefix='/api/reports')

@bp.route('/revenue', methods=['GET'])
@token_required
def revenue_report(current_user):
    """Get revenue report"""
    try:
        if not current_user.hotel_id:
            return jsonify({'error': 'Hotel not found for user'}), 404
        
        # Get date range from query params (default: last 30 days)
        days = request.args.get('days', 30, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        billings = Billing.query.filter(
            Billing.hotel_id == current_user.hotel_id,
            Billing.created_at >= start_date
        ).all()
        
        total_revenue = sum(b.paid_amount for b in billings)
        total_pending = sum(b.balance for b in billings if b.status in ['pending', 'partial'])
        completed_bookings = len([b for b in billings if b.status == 'paid'])
        
        return jsonify({
            'total_revenue': total_revenue,
            'total_pending': total_pending,
            'completed_bookings': completed_bookings,
            'period_days': days,
            'start_date': start_date.isoformat(),
            'end_date': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/menu-popular', methods=['GET'])
@token_required
def popular_menu_report(current_user):
    """Get popular menu items"""
    try:
        if not current_user.hotel_id:
            return jsonify({'error': 'Hotel not found for user'}), 404
        
        menus = Menu.query.filter_by(hotel_id=current_user.hotel_id).all()
        
        menu_data = [{
            'name': m.name,
            'price': m.price,
            'category': m.category,
            'availability': m.availability
        } for m in menus]
        
        return jsonify({
            'total_items': len(menus),
            'items': menu_data
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/occupancy', methods=['GET'])
@token_required
def occupancy_report(current_user):
    """Get occupancy report"""
    try:
        if not current_user.hotel_id:
            return jsonify({'error': 'Hotel not found for user'}), 404
        
        # Count active billings (check-in before today, check-out after today)
        today = datetime.utcnow().date()
        
        active_guests = Billing.query.filter(
            Billing.hotel_id == current_user.hotel_id,
            Billing.check_in_date <= datetime.combine(today, datetime.min.time()),
            Billing.check_out_date >= datetime.combine(today, datetime.min.time())
        ).count()
        
        return jsonify({
            'active_guests': active_guests,
            'date': today.isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
