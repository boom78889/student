from flask import Blueprint, request, jsonify
from app import db
from models.user import User
from models.otp import OTP
from models.hotel import Hotel
import jwt
import os
from datetime import datetime, timedelta

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password') or not data.get('phone_number'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 409
        
        if User.query.filter_by(phone_number=data['phone_number']).first():
            return jsonify({'error': 'Phone number already registered'}), 409
        
        user = User(
            username=data['username'],
            phone_number=data['phone_number'],
            email=data.get('email')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/send-otp', methods=['POST'])
def send_otp():
    """Send OTP to phone number"""
    try:
        data = request.get_json()
        phone_number = data.get('phone_number')
        
        if not phone_number:
            return jsonify({'error': 'Phone number is required'}), 400
        
        # Generate OTP
        otp_code = OTP.generate_otp()
        
        # Delete previous OTPs for this number
        OTP.query.filter_by(phone_number=phone_number).delete()
        
        otp = OTP(phone_number=phone_number, otp_code=otp_code)
        db.session.add(otp)
        db.session.commit()
        
        # TODO: Send OTP via Twilio or Firebase
        # send_sms(phone_number, f"Your OTP is: {otp_code}")
        
        return jsonify({
            'message': 'OTP sent successfully',
            'otp_id': otp.id
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    """Verify OTP"""
    try:
        data = request.get_json()
        phone_number = data.get('phone_number')
        otp_code = data.get('otp_code')
        
        if not phone_number or not otp_code:
            return jsonify({'error': 'Phone number and OTP code required'}), 400
        
        otp = OTP.query.filter_by(phone_number=phone_number).order_by(OTP.created_at.desc()).first()
        
        if not otp:
            return jsonify({'error': 'OTP not found'}), 404
        
        if otp.is_expired():
            return jsonify({'error': 'OTP expired'}), 400
        
        if otp.attempts >= 3:
            return jsonify({'error': 'Too many attempts. Request a new OTP'}), 400
        
        if otp.otp_code != otp_code:
            otp.attempts += 1
            db.session.commit()
            return jsonify({'error': 'Invalid OTP'}), 400
        
        otp.is_verified = True
        
        # Update user verification status
        user = User.query.filter_by(phone_number=phone_number).first()
        if user:
            user.is_verified = True
        
        db.session.commit()
        
        return jsonify({
            'message': 'OTP verified successfully',
            'phone_number': phone_number
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        if not user.is_verified:
            return jsonify({'error': 'Phone number not verified'}), 403
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, os.getenv('SECRET_KEY', 'dev-secret-key'), algorithm='HS256')
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
