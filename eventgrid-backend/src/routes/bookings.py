from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import Booking, Event, Vendor, Venue, User, db
import uuid
from datetime import datetime

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/bookings', methods=['GET'])
@jwt_required()
def get_bookings():
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
        status = request.args.get('status')
        event_id = request.args.get('eventId')
        page = request.args.get('page', 1, type=int)
        limit = min(request.args.get('limit', 20, type=int), 100)
        
        # Build query - get bookings for user's events
        query = Booking.query.join(Event).filter(Event.organizer_id == user.id)
        
        if status:
            query = query.filter(Booking.status == status)
        if event_id:
            event = Event.query.filter_by(event_id=event_id, organizer_id=user.id).first()
            if event:
                query = query.filter(Booking.event_id == event.id)
        
        # Paginate
        bookings = query.order_by(Booking.created_at.desc()).paginate(
            page=page, per_page=limit, error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': {
                'bookings': [booking.to_dict() for booking in bookings.items],
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'total': bookings.total,
                    'totalPages': bookings.pages
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while fetching bookings'
            }
        }), 500

@bookings_bp.route('/bookings', methods=['POST'])
@jwt_required()
def create_booking():
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
        required_fields = ['eventId', 'serviceDetails']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': f'Missing required field: {field}'
                    }
                }), 400
        
        # Verify event belongs to user
        event = Event.query.filter_by(event_id=data['eventId'], organizer_id=user.id).first()
        if not event:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'EVENT_NOT_FOUND',
                    'message': 'Event not found or access denied'
                }
            }), 404
        
        # Verify vendor or venue exists
        vendor = None
        venue = None
        
        if 'vendorId' in data:
            vendor = Vendor.query.filter_by(vendor_id=data['vendorId'], is_active=True).first()
            if not vendor:
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'VENDOR_NOT_FOUND',
                        'message': 'Vendor not found'
                    }
                }), 404
        
        if 'venueId' in data:
            venue = Venue.query.filter_by(venue_id=data['venueId'], is_active=True).first()
            if not venue:
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'VENUE_NOT_FOUND',
                        'message': 'Venue not found'
                    }
                }), 404
        
        if not vendor and not venue:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Either vendorId or venueId is required'
                }
            }), 400
        
        # Parse service date
        schedule = data.get('schedule', {})
        service_date = None
        start_time = None
        end_time = None
        
        if 'serviceDate' in schedule:
            try:
                service_date = datetime.fromisoformat(schedule['serviceDate'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': 'Invalid service date format'
                    }
                }), 400
        else:
            # Default to event start date
            service_date = event.start_date
        
        if 'startTime' in schedule:
            try:
                start_time = datetime.fromisoformat(schedule['startTime'].replace('Z', '+00:00'))
            except ValueError:
                pass
        
        if 'endTime' in schedule:
            try:
                end_time = datetime.fromisoformat(schedule['endTime'].replace('Z', '+00:00'))
            except ValueError:
                pass
        
        # Create booking
        booking_id = f"bkg_{uuid.uuid4().hex[:12]}"
        service_details = data['serviceDetails']
        
        booking = Booking(
            booking_id=booking_id,
            event_id=event.id,
            vendor_id=vendor.id if vendor else None,
            venue_id=venue.id if venue else None,
            service_name=service_details.get('serviceName', ''),
            service_details=service_details.get('specifications', {}),
            service_date=service_date,
            start_time=start_time,
            end_time=end_time,
            message=data.get('message', '')
        )
        
        db.session.add(booking)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': booking.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while creating the booking'
            }
        }), 500

@bookings_bp.route('/bookings/<booking_id>', methods=['GET'])
@jwt_required()
def get_booking(booking_id):
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
        
        # Get booking for user's events
        booking = Booking.query.join(Event).filter(
            Booking.booking_id == booking_id,
            Event.organizer_id == user.id
        ).first()
        
        if not booking:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'BOOKING_NOT_FOUND',
                    'message': 'Booking not found'
                }
            }), 404
        
        return jsonify({
            'success': True,
            'data': booking.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while fetching the booking'
            }
        }), 500

@bookings_bp.route('/bookings/<booking_id>/status', methods=['PUT'])
@jwt_required()
def update_booking_status(booking_id):
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
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Status is required'
                }
            }), 400
        
        valid_statuses = ['inquiry', 'quoted', 'negotiating', 'confirmed', 'in_progress', 'completed', 'cancelled']
        if new_status not in valid_statuses:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
                }
            }), 400
        
        # Get booking for user's events
        booking = Booking.query.join(Event).filter(
            Booking.booking_id == booking_id,
            Event.organizer_id == user.id
        ).first()
        
        if not booking:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'BOOKING_NOT_FOUND',
                    'message': 'Booking not found'
                }
            }), 404
        
        booking.status = new_status
        booking.updated_at = datetime.utcnow()
        
        # Update pricing if provided
        if 'quotedPrice' in data:
            booking.quoted_price = data['quotedPrice']
        if 'finalPrice' in data:
            booking.final_price = data['finalPrice']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': booking.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while updating the booking'
            }
        }), 500

