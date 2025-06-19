from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User, Event, db
import json
from datetime import datetime
import random

live_bp = Blueprint('live', __name__)

@live_bp.route('/live/events/<event_id>/dashboard', methods=['GET'])
@jwt_required()
def get_live_dashboard(event_id):
    """Get real-time dashboard data for live event"""
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
        
        # Generate real-time dashboard data
        dashboard_data = generate_live_dashboard_data(event)
        
        return jsonify({
            'success': True,
            'data': {
                'eventId': event_id,
                'dashboard': dashboard_data,
                'lastUpdated': datetime.utcnow().isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while fetching dashboard data'
            }
        }), 500

@live_bp.route('/live/events/<event_id>/checkin', methods=['POST'])
@jwt_required()
def process_checkin(event_id):
    """Process guest check-in"""
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
        guest_id = data.get('guestId')
        
        if not guest_id:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Guest ID is required'
                }
            }), 400
        
        # Process check-in (mock implementation)
        checkin_result = process_guest_checkin(event, guest_id, data)
        
        return jsonify({
            'success': True,
            'data': checkin_result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while processing check-in'
            }
        }), 500

@live_bp.route('/live/events/<event_id>/vendors/status', methods=['GET'])
@jwt_required()
def get_vendor_status(event_id):
    """Get real-time vendor arrival and setup status"""
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
        
        # Get vendor status data
        vendor_status = get_event_vendor_status(event)
        
        return jsonify({
            'success': True,
            'data': {
                'eventId': event_id,
                'vendorStatus': vendor_status,
                'lastUpdated': datetime.utcnow().isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while fetching vendor status'
            }
        }), 500

@live_bp.route('/live/events/<event_id>/alerts', methods=['POST'])
@jwt_required()
def create_alert(event_id):
    """Create emergency alert or notification"""
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
        
        # Create alert
        alert = create_event_alert(event, data)
        
        return jsonify({
            'success': True,
            'data': alert
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while creating alert'
            }
        }), 500

@live_bp.route('/live/events/<event_id>/controls', methods=['POST'])
@jwt_required()
def control_smart_devices(event_id):
    """Control IoT/Smart devices at the event"""
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
        
        # Control smart devices
        control_result = control_event_devices(event, data)
        
        return jsonify({
            'success': True,
            'data': control_result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while controlling devices'
            }
        }), 500

def generate_live_dashboard_data(event):
    """Generate real-time dashboard data"""
    expected_attendees = event.expected_attendees or 100
    
    return {
        'overview': {
            'eventStatus': 'in_progress',
            'startTime': event.start_date.isoformat() if event.start_date else None,
            'currentTime': datetime.utcnow().isoformat(),
            'duration': '2h 30m'
        },
        'attendance': {
            'checkedIn': random.randint(int(expected_attendees * 0.6), int(expected_attendees * 0.9)),
            'expected': expected_attendees,
            'checkinRate': random.randint(75, 95),
            'recentCheckins': [
                {
                    'guestName': 'John Smith',
                    'time': '14:32',
                    'status': 'checked_in'
                },
                {
                    'guestName': 'Sarah Johnson',
                    'time': '14:31',
                    'status': 'checked_in'
                },
                {
                    'guestName': 'Mike Chen',
                    'time': '14:29',
                    'status': 'checked_in'
                }
            ]
        },
        'vendors': {
            'total': 8,
            'arrived': 7,
            'setupComplete': 6,
            'issues': 1,
            'status': [
                {
                    'vendorName': 'Capture Moments Photography',
                    'category': 'photography',
                    'status': 'setup_complete',
                    'arrivalTime': '12:00',
                    'notes': 'Equipment ready, testing lighting'
                },
                {
                    'vendorName': 'Gourmet Catering Co',
                    'category': 'catering',
                    'status': 'in_progress',
                    'arrivalTime': '11:30',
                    'notes': 'Food prep 80% complete'
                },
                {
                    'vendorName': 'Sound & Vision AV',
                    'category': 'audio_visual',
                    'status': 'issue',
                    'arrivalTime': '10:45',
                    'notes': 'Microphone feedback issue - resolving'
                }
            ]
        },
        'environment': {
            'temperature': random.randint(20, 24),
            'humidity': random.randint(40, 60),
            'lighting': {
                'level': random.randint(70, 90),
                'mode': 'event_mode'
            },
            'sound': {
                'level': random.randint(65, 75),
                'status': 'optimal'
            }
        },
        'alerts': [
            {
                'id': 'alert_001',
                'type': 'info',
                'message': 'Catering setup 80% complete',
                'timestamp': '14:25',
                'resolved': False
            },
            {
                'id': 'alert_002',
                'type': 'warning',
                'message': 'AV equipment issue detected',
                'timestamp': '14:15',
                'resolved': False
            }
        ],
        'engagement': {
            'socialMentions': random.randint(15, 45),
            'photoShares': random.randint(8, 25),
            'feedbackScore': random.uniform(4.2, 4.8),
            'networkingConnections': random.randint(25, 75)
        }
    }

def process_guest_checkin(event, guest_id, data):
    """Process guest check-in"""
    return {
        'guestId': guest_id,
        'guestName': data.get('guestName', 'Unknown Guest'),
        'checkinTime': datetime.utcnow().isoformat(),
        'status': 'checked_in',
        'seatAssignment': data.get('seatAssignment'),
        'specialRequests': data.get('specialRequests', []),
        'qrCode': f'checkin_{guest_id}_{int(datetime.utcnow().timestamp())}',
        'welcomeMessage': f'Welcome to {event.title}!'
    }

def get_event_vendor_status(event):
    """Get vendor status for the event"""
    return [
        {
            'vendorId': 'vnd_001',
            'vendorName': 'Capture Moments Photography',
            'category': 'photography',
            'status': 'setup_complete',
            'arrivalTime': '12:00',
            'setupProgress': 100,
            'location': 'Main Hall - Corner A',
            'contact': '+1-555-0123',
            'notes': 'All equipment ready, backup cameras in place',
            'lastUpdate': '14:30'
        },
        {
            'vendorId': 'vnd_002',
            'vendorName': 'Gourmet Catering Co',
            'category': 'catering',
            'status': 'in_progress',
            'arrivalTime': '11:30',
            'setupProgress': 80,
            'location': 'Kitchen & Service Area',
            'contact': '+1-555-0456',
            'notes': 'Food prep on schedule, serving starts at 18:00',
            'lastUpdate': '14:25'
        },
        {
            'vendorId': 'vnd_003',
            'vendorName': 'Sound & Vision AV',
            'category': 'audio_visual',
            'status': 'issue',
            'arrivalTime': '10:45',
            'setupProgress': 75,
            'location': 'Stage Area',
            'contact': '+1-555-0789',
            'notes': 'Resolving microphone feedback - ETA 15 minutes',
            'lastUpdate': '14:20'
        }
    ]

def create_event_alert(event, data):
    """Create event alert"""
    alert_id = f"alert_{int(datetime.utcnow().timestamp())}"
    
    return {
        'alertId': alert_id,
        'eventId': event.event_id,
        'type': data.get('type', 'info'),
        'severity': data.get('severity', 'medium'),
        'title': data.get('title', 'Event Alert'),
        'message': data.get('message', ''),
        'category': data.get('category', 'general'),
        'recipients': data.get('recipients', ['event_staff']),
        'createdAt': datetime.utcnow().isoformat(),
        'status': 'active',
        'actions': data.get('actions', []),
        'autoResolve': data.get('autoResolve', False)
    }

def control_event_devices(event, data):
    """Control smart devices at the event"""
    device_type = data.get('deviceType')
    action = data.get('action')
    parameters = data.get('parameters', {})
    
    # Mock device control responses
    responses = {
        'lighting': {
            'deviceId': 'light_001',
            'type': 'lighting',
            'action': action,
            'status': 'success',
            'currentState': {
                'brightness': parameters.get('brightness', 80),
                'color': parameters.get('color', '#FFFFFF'),
                'mode': parameters.get('mode', 'event')
            }
        },
        'sound': {
            'deviceId': 'sound_001',
            'type': 'sound',
            'action': action,
            'status': 'success',
            'currentState': {
                'volume': parameters.get('volume', 75),
                'source': parameters.get('source', 'microphone'),
                'equalizer': parameters.get('equalizer', 'speech')
            }
        },
        'climate': {
            'deviceId': 'hvac_001',
            'type': 'climate',
            'action': action,
            'status': 'success',
            'currentState': {
                'temperature': parameters.get('temperature', 22),
                'humidity': parameters.get('humidity', 50),
                'airflow': parameters.get('airflow', 'medium')
            }
        },
        'screens': {
            'deviceId': 'display_001',
            'type': 'screens',
            'action': action,
            'status': 'success',
            'currentState': {
                'content': parameters.get('content', 'welcome_slide'),
                'brightness': parameters.get('brightness', 90),
                'mode': parameters.get('mode', 'presentation')
            }
        }
    }
    
    return {
        'controlId': f"ctrl_{int(datetime.utcnow().timestamp())}",
        'eventId': event.event_id,
        'timestamp': datetime.utcnow().isoformat(),
        'result': responses.get(device_type, {
            'deviceId': 'unknown',
            'type': device_type,
            'action': action,
            'status': 'error',
            'message': 'Device type not supported'
        })
    }

