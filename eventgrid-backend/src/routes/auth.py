from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models.user import User, BusinessProfile, UserPreferences, db
import uuid
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'firstName', 'lastName', 'role']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': f'Missing required field: {field}'
                    }
                }), 400
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({
                'success': False,
                'error': {
                    'code': 'USER_EXISTS',
                    'message': 'User with this email already exists'
                }
            }), 409
        
        # Create new user
        user_id = f"usr_{uuid.uuid4().hex[:12]}"
        user = User(
            user_id=user_id,
            email=data['email'],
            first_name=data['firstName'],
            last_name=data['lastName'],
            role=data['role']
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.flush()  # Get the user ID
        
        # Create business profile if vendor or venue owner
        if data['role'] in ['vendor', 'venue_owner'] and 'businessInfo' in data:
            business_info = data['businessInfo']
            business_profile = BusinessProfile(
                user_id=user.id,
                business_name=business_info.get('companyName', ''),
                business_type=business_info.get('businessType', ''),
                city=business_info.get('location', '').split(',')[0] if business_info.get('location') else '',
                country=business_info.get('location', '').split(',')[-1].strip() if business_info.get('location') else ''
            )
            db.session.add(business_profile)
        
        # Create user preferences
        preferences_data = data.get('preferences', {})
        preferences = UserPreferences(
            user_id=user.id,
            language=preferences_data.get('language', 'en'),
            currency=preferences_data.get('currency', 'USD'),
            timezone=preferences_data.get('timezone', 'UTC')
        )
        db.session.add(preferences)
        
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(
            identity=user.user_id,
            expires_delta=timedelta(hours=1)
        )
        
        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict(),
                'tokens': {
                    'accessToken': access_token,
                    'expiresIn': 3600
                }
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred during registration'
            }
        }), 500

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Email and password are required'
                }
            }), 400
        
        # Find user
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({
                'success': False,
                'error': {
                    'code': 'INVALID_CREDENTIALS',
                    'message': 'Invalid email or password'
                }
            }), 401
        
        if not user.is_active:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'ACCOUNT_DISABLED',
                    'message': 'Account is disabled'
                }
            }), 401
        
        # Create access token
        access_token = create_access_token(
            identity=user.user_id,
            expires_delta=timedelta(hours=1)
        )
        
        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict(),
                'tokens': {
                    'accessToken': access_token,
                    'expiresIn': 3600
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred during login'
            }
        }), 500

@auth_bp.route('/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(user_id=current_user_id).first()
        
        if not user:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'USER_NOT_FOUND',
                    'message': 'User not found'
                }
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred'
            }
        }), 500

