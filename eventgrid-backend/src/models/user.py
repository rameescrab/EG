from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # event_manager, vendor, venue_owner, artist, guest
    avatar = db.Column(db.String(255), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    business_profile = db.relationship('BusinessProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    preferences = db.relationship('UserPreferences', backref='user', uselist=False, cascade='all, delete-orphan')
    events = db.relationship('Event', backref='organizer', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def check_password(self, password):
        """Check if the provided password matches the stored hash"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest() == self.password_hash
    
    def to_dict(self):
        return {
            'userId': self.user_id,
            'email': self.email,
            'profile': {
                'firstName': self.first_name,
                'lastName': self.last_name,
                'avatar': self.avatar
            },
            'role': self.role,
            'isVerified': self.is_verified,
            'isActive': self.is_active,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }

class BusinessProfile(db.Model):
    __tablename__ = 'business_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    business_name = db.Column(db.String(100), nullable=False)
    business_type = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    website = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'businessName': self.business_name,
            'businessType': self.business_type,
            'description': self.description,
            'website': self.website,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'country': self.country
        }

class UserPreferences(db.Model):
    __tablename__ = 'user_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    language = db.Column(db.String(10), default='en')
    currency = db.Column(db.String(10), default='USD')
    timezone = db.Column(db.String(50), default='UTC')
    notifications_email = db.Column(db.Boolean, default=True)
    notifications_sms = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'language': self.language,
            'currency': self.currency,
            'timezone': self.timezone,
            'notifications': {
                'email': self.notifications_email,
                'sms': self.notifications_sms
            }
        }

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String(50), unique=True, nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    event_type = db.Column(db.String(50), nullable=False)  # corporate, wedding, conference, etc.
    category = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(20), default='draft')  # draft, planning, confirmed, in_progress, completed, cancelled
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    timezone = db.Column(db.String(50), nullable=False)
    expected_attendees = db.Column(db.Integer, nullable=True)
    max_capacity = db.Column(db.Integer, nullable=True)
    total_budget = db.Column(db.Float, nullable=True)
    currency = db.Column(db.String(10), default='USD')
    visibility = db.Column(db.String(20), default='private')  # public, private, unlisted
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'eventId': self.event_id,
            'organizerId': self.organizer.user_id if self.organizer else None,
            'basicInfo': {
                'title': self.title,
                'description': self.description,
                'type': self.event_type,
                'category': self.category
            },
            'schedule': {
                'startDate': self.start_date.isoformat() if self.start_date else None,
                'endDate': self.end_date.isoformat() if self.end_date else None,
                'timezone': self.timezone
            },
            'attendees': {
                'expectedCount': self.expected_attendees,
                'capacity': self.max_capacity
            },
            'budget': {
                'totalBudget': self.total_budget,
                'currency': self.currency
            },
            'status': self.status,
            'visibility': self.visibility,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }

class Vendor(db.Model):
    __tablename__ = 'vendors'
    
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    business_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # photography, catering, music, etc.
    description = db.Column(db.Text, nullable=True)
    service_areas = db.Column(db.JSON, nullable=True)  # List of cities/regions served
    starting_price = db.Column(db.Float, nullable=True)
    currency = db.Column(db.String(10), default='USD')
    average_rating = db.Column(db.Float, default=0.0)
    total_reviews = db.Column(db.Integer, default=0)
    response_time_hours = db.Column(db.Float, default=24.0)
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'vendorId': self.vendor_id,
            'businessProfile': {
                'businessName': self.business_name,
                'description': self.description,
                'category': self.category,
                'serviceAreas': self.service_areas or []
            },
            'ratings': {
                'averageRating': self.average_rating,
                'totalReviews': self.total_reviews
            },
            'pricing': {
                'startingPrice': self.starting_price,
                'currency': self.currency
            },
            'responseTime': self.response_time_hours,
            'isVerified': self.is_verified,
            'isActive': self.is_active
        }

class Venue(db.Model):
    __tablename__ = 'venues'
    
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.String(50), unique=True, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    venue_type = db.Column(db.String(50), nullable=False)  # hotel, conference_center, outdoor, etc.
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    capacity_min = db.Column(db.Integer, nullable=True)
    capacity_max = db.Column(db.Integer, nullable=True)
    hourly_rate = db.Column(db.Float, nullable=True)
    daily_rate = db.Column(db.Float, nullable=True)
    currency = db.Column(db.String(10), default='USD')
    amenities = db.Column(db.JSON, nullable=True)  # List of amenities
    average_rating = db.Column(db.Float, default=0.0)
    total_reviews = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'venueId': self.venue_id,
            'name': self.name,
            'description': self.description,
            'type': self.venue_type,
            'location': {
                'address': self.address,
                'city': self.city,
                'country': self.country,
                'coordinates': {
                    'latitude': self.latitude,
                    'longitude': self.longitude
                } if self.latitude and self.longitude else None
            },
            'capacity': {
                'min': self.capacity_min,
                'max': self.capacity_max
            },
            'pricing': {
                'hourlyRate': self.hourly_rate,
                'dailyRate': self.daily_rate,
                'currency': self.currency
            },
            'amenities': self.amenities or [],
            'ratings': {
                'averageRating': self.average_rating,
                'totalReviews': self.total_reviews
            },
            'isActive': self.is_active
        }

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.String(50), unique=True, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=True)
    service_name = db.Column(db.String(100), nullable=False)
    service_details = db.Column(db.JSON, nullable=True)
    status = db.Column(db.String(20), default='inquiry')  # inquiry, quoted, negotiating, confirmed, in_progress, completed, cancelled
    service_date = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    quoted_price = db.Column(db.Float, nullable=True)
    final_price = db.Column(db.Float, nullable=True)
    currency = db.Column(db.String(10), default='USD')
    message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    event = db.relationship('Event', backref='bookings')
    vendor = db.relationship('Vendor', backref='bookings')
    venue = db.relationship('Venue', backref='bookings')

    def to_dict(self):
        return {
            'bookingId': self.booking_id,
            'eventId': self.event.event_id if self.event else None,
            'vendorId': self.vendor.vendor_id if self.vendor else None,
            'venueId': self.venue.venue_id if self.venue else None,
            'serviceDetails': {
                'serviceName': self.service_name,
                'specifications': self.service_details or {}
            },
            'schedule': {
                'serviceDate': self.service_date.isoformat() if self.service_date else None,
                'startTime': self.start_time.isoformat() if self.start_time else None,
                'endTime': self.end_time.isoformat() if self.end_time else None
            },
            'pricing': {
                'quotedPrice': self.quoted_price,
                'finalPrice': self.final_price,
                'currency': self.currency
            },
            'status': self.status,
            'message': self.message,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }

