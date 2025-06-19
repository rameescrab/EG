from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User, Event, db
import json
from datetime import datetime

payments_bp = Blueprint('payments', __name__)

# Mock payment service for deployment (replace with actual Stripe integration in production)

@payments_bp.route('/payments/create-payment-intent', methods=['POST'])
@jwt_required()
def create_payment_intent():
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
        if not data.get('amount') or not data.get('currency'):
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Amount and currency are required'
                }
            }), 400
        
        # Validate booking if provided
        booking_id = data.get('bookingId')
        booking = None
        if booking_id:
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
        
        # Create Stripe PaymentIntent
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(data['amount'] * 100),  # Convert to cents
                currency=data['currency'].lower(),
                metadata={
                    'user_id': user.user_id,
                    'booking_id': booking_id if booking_id else '',
                    'event_id': booking.event.event_id if booking else data.get('eventId', ''),
                    'description': data.get('description', 'EventGrid Payment')
                }
            )
            
            return jsonify({
                'success': True,
                'data': {
                    'clientSecret': intent.client_secret,
                    'paymentIntentId': intent.id,
                    'amount': data['amount'],
                    'currency': data['currency']
                }
            }), 200
            
        except stripe.error.StripeError as e:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'PAYMENT_ERROR',
                    'message': str(e)
                }
            }), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while creating payment intent'
            }
        }), 500

@payments_bp.route('/payments/confirm-payment', methods=['POST'])
@jwt_required()
def confirm_payment():
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
        payment_intent_id = data.get('paymentIntentId')
        
        if not payment_intent_id:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Payment intent ID is required'
                }
            }), 400
        
        # Retrieve payment intent from Stripe
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            if intent.status == 'succeeded':
                # Update booking status if applicable
                booking_id = intent.metadata.get('booking_id')
                if booking_id:
                    booking = Booking.query.join(Event).filter(
                        Booking.booking_id == booking_id,
                        Event.organizer_id == user.id
                    ).first()
                    
                    if booking:
                        booking.status = 'confirmed'
                        booking.final_price = intent.amount / 100  # Convert from cents
                        booking.updated_at = datetime.utcnow()
                        db.session.commit()
                
                return jsonify({
                    'success': True,
                    'data': {
                        'paymentStatus': 'succeeded',
                        'amount': intent.amount / 100,
                        'currency': intent.currency.upper(),
                        'paymentMethod': intent.payment_method
                    }
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'PAYMENT_FAILED',
                        'message': f'Payment status: {intent.status}'
                    }
                }), 400
                
        except stripe.error.StripeError as e:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'PAYMENT_ERROR',
                    'message': str(e)
                }
            }), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while confirming payment'
            }
        }), 500

@payments_bp.route('/payments/webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events"""
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET', 'whsec_...')  # Replace with actual webhook secret
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError:
        return jsonify({'error': 'Invalid signature'}), 400
    
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        
        # Update booking status
        booking_id = payment_intent['metadata'].get('booking_id')
        if booking_id:
            booking = Booking.query.filter_by(booking_id=booking_id).first()
            if booking:
                booking.status = 'confirmed'
                booking.final_price = payment_intent['amount'] / 100
                booking.updated_at = datetime.utcnow()
                db.session.commit()
    
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        
        # Handle failed payment
        booking_id = payment_intent['metadata'].get('booking_id')
        if booking_id:
            booking = Booking.query.filter_by(booking_id=booking_id).first()
            if booking:
                booking.status = 'cancelled'
                booking.updated_at = datetime.utcnow()
                db.session.commit()
    
    return jsonify({'status': 'success'}), 200

@payments_bp.route('/payments/history', methods=['GET'])
@jwt_required()
def get_payment_history():
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
        
        # Get confirmed bookings with payments
        bookings = Booking.query.join(Event).filter(
            Event.organizer_id == user.id,
            Booking.status.in_(['confirmed', 'completed']),
            Booking.final_price.isnot(None)
        ).order_by(Booking.updated_at.desc()).all()
        
        payment_history = []
        for booking in bookings:
            payment_history.append({
                'bookingId': booking.booking_id,
                'eventTitle': booking.event.title,
                'serviceName': booking.service_name,
                'amount': booking.final_price,
                'currency': booking.currency,
                'status': booking.status,
                'paymentDate': booking.updated_at.isoformat() if booking.updated_at else None,
                'vendorName': booking.vendor.business_name if booking.vendor else None,
                'venueName': booking.venue.name if booking.venue else None
            })
        
        return jsonify({
            'success': True,
            'data': {
                'payments': payment_history,
                'total': len(payment_history)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while fetching payment history'
            }
        }), 500

