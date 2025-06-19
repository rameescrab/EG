from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import Event, User, db
import uuid
from datetime import datetime

events_bp = Blueprint('events', __name__)

@events_bp.route('/events', methods=['GET'])
@jwt_required()
def get_events():
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
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        limit = min(request.args.get('limit', 20, type=int), 100)
        status = request.args.get('status')
        event_type = request.args.get('type')
        
        # Build query
        query = Event.query.filter_by(organizer_id=user.id)
        
        if status:
            query = query.filter_by(status=status)
        if event_type:
            query = query.filter_by(event_type=event_type)
        
        # Paginate
        events = query.order_by(Event.start_date.desc()).paginate(
            page=page, per_page=limit, error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': {
                'events': [event.to_dict() for event in events.items],
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'total': events.total,
                    'totalPages': events.pages
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while fetching events'
            }
        }), 500

@events_bp.route('/events', methods=['POST'])
@jwt_required()
def create_event():
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
        
        data = request.get_json()
        
        # Validate required fields
        basic_info = data.get('basicInfo', {})
        schedule = data.get('schedule', {})
        
        if not basic_info.get('title') or not basic_info.get('type'):
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Title and type are required'
                }
            }), 400
        
        if not schedule.get('startDate') or not schedule.get('endDate'):
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Start date and end date are required'
                }
            }), 400
        
        # Parse dates
        try:
            start_date = datetime.fromisoformat(schedule['startDate'].replace('Z', '+00:00'))
            end_date = datetime.fromisoformat(schedule['endDate'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Invalid date format'
                }
            }), 400
        
        # Create event
        event_id = f"evt_{uuid.uuid4().hex[:12]}"
        attendees = data.get('attendees', {})
        budget = data.get('budget', {})
        
        event = Event(
            event_id=event_id,
            organizer_id=user.id,
            title=basic_info['title'],
            description=basic_info.get('description', ''),
            event_type=basic_info['type'],
            category=basic_info.get('category', ''),
            start_date=start_date,
            end_date=end_date,
            timezone=schedule.get('timezone', 'UTC'),
            expected_attendees=attendees.get('expectedCount'),
            max_capacity=attendees.get('capacity'),
            total_budget=budget.get('totalBudget'),
            currency=budget.get('currency', 'USD'),
            visibility=data.get('visibility', 'private')
        )
        
        db.session.add(event)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': event.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while creating the event'
            }
        }), 500

@events_bp.route('/events/<event_id>', methods=['GET'])
@jwt_required()
def get_event(event_id):
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
        
        event = Event.query.filter_by(event_id=event_id, organizer_id=user.id).first()
        
        if not event:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'EVENT_NOT_FOUND',
                    'message': 'Event not found'
                }
            }), 404
        
        return jsonify({
            'success': True,
            'data': event.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while fetching the event'
            }
        }), 500

@events_bp.route('/events/<event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
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
        
        event = Event.query.filter_by(event_id=event_id, organizer_id=user.id).first()
        
        if not event:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'EVENT_NOT_FOUND',
                    'message': 'Event not found'
                }
            }), 404
        
        data = request.get_json()
        
        # Update basic info
        if 'basicInfo' in data:
            basic_info = data['basicInfo']
            if 'title' in basic_info:
                event.title = basic_info['title']
            if 'description' in basic_info:
                event.description = basic_info['description']
            if 'category' in basic_info:
                event.category = basic_info['category']
        
        # Update schedule
        if 'schedule' in data:
            schedule = data['schedule']
            if 'startDate' in schedule:
                try:
                    event.start_date = datetime.fromisoformat(schedule['startDate'].replace('Z', '+00:00'))
                except ValueError:
                    return jsonify({
                        'success': False,
                        'error': {
                            'code': 'VALIDATION_ERROR',
                            'message': 'Invalid start date format'
                        }
                    }), 400
            if 'endDate' in schedule:
                try:
                    event.end_date = datetime.fromisoformat(schedule['endDate'].replace('Z', '+00:00'))
                except ValueError:
                    return jsonify({
                        'success': False,
                        'error': {
                            'code': 'VALIDATION_ERROR',
                            'message': 'Invalid end date format'
                        }
                    }), 400
        
        # Update budget
        if 'budget' in data:
            budget = data['budget']
            if 'totalBudget' in budget:
                event.total_budget = budget['totalBudget']
        
        # Update status
        if 'status' in data:
            event.status = data['status']
        
        event.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': event.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while updating the event'
            }
        }), 500

@events_bp.route('/events/<event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
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
        
        event = Event.query.filter_by(event_id=event_id, organizer_id=user.id).first()
        
        if not event:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'EVENT_NOT_FOUND',
                    'message': 'Event not found'
                }
            }), 404
        
        db.session.delete(event)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Event deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while deleting the event'
            }
        }), 500

