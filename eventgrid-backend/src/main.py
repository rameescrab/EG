import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.models.user import db
from src.routes.auth import auth_bp
from src.routes.events import events_bp
from src.routes.marketplace import marketplace_bp
from src.routes.bookings import bookings_bp
from src.routes.payments import payments_bp
from src.routes.ai import ai_bp
from src.routes.ar import ar_bp
from src.routes.live import live_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configuration
app.config['SECRET_KEY'] = 'eventgrid_secret_key_2025'
app.config['JWT_SECRET_KEY'] = 'eventgrid_jwt_secret_key_2025'

# Enable CORS for all routes
CORS(app, origins="*")

# Initialize JWT
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(events_bp, url_prefix='/api')
app.register_blueprint(marketplace_bp, url_prefix='/api')
app.register_blueprint(bookings_bp, url_prefix='/api')
app.register_blueprint(payments_bp, url_prefix='/api')
app.register_blueprint(ai_bp, url_prefix='/api')
app.register_blueprint(ar_bp, url_prefix='/api')
app.register_blueprint(live_bp, url_prefix='/api')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create tables and seed data
with app.app_context():
    db.create_all()
    
    # Seed some sample data for testing
    from src.models.user import User, Vendor, Event, BusinessProfile, UserPreferences
    import uuid
    from datetime import datetime, timedelta
    
    # Check if we already have data
    if User.query.count() == 0:
        # Create sample users
        # Event Manager
        user1_id = f"usr_{uuid.uuid4().hex[:12]}"
        user1 = User(
            user_id=user1_id,
            email="sarah.chen@example.com",
            first_name="Sarah",
            last_name="Chen",
            role="event_manager"
        )
        user1.set_password("password123")
        db.session.add(user1)
        db.session.flush()
        
        # User preferences
        prefs1 = UserPreferences(
            user_id=user1.id,
            language="en",
            currency="USD",
            timezone="America/Los_Angeles"
        )
        db.session.add(prefs1)
        
        # Vendor User
        user2_id = f"usr_{uuid.uuid4().hex[:12]}"
        user2 = User(
            user_id=user2_id,
            email="mike.photo@example.com",
            first_name="Mike",
            last_name="Johnson",
            role="vendor"
        )
        user2.set_password("password123")
        db.session.add(user2)
        db.session.flush()
        
        # Business profile for vendor
        business2 = BusinessProfile(
            user_id=user2.id,
            business_name="Capture Moments Photography",
            business_type="photography",
            description="Professional wedding and event photography",
            website="https://capturemoments.com",
            phone="+1-555-0123",
            city="San Francisco",
            country="USA"
        )
        db.session.add(business2)
        
        # Vendor profile
        vendor1_id = f"vnd_{uuid.uuid4().hex[:12]}"
        vendor1 = Vendor(
            vendor_id=vendor1_id,
            user_id=user2.id,
            business_name="Capture Moments Photography",
            category="photography",
            description="Professional wedding and event photography with 10+ years experience",
            service_areas=["San Francisco", "Bay Area", "Napa Valley"],
            starting_price=2500.0,
            currency="USD",
            average_rating=4.8,
            total_reviews=127,
            response_time_hours=2.5,
            is_verified=True
        )
        db.session.add(vendor1)
        
        # Another vendor
        user3_id = f"usr_{uuid.uuid4().hex[:12]}"
        user3 = User(
            user_id=user3_id,
            email="chef.maria@example.com",
            first_name="Maria",
            last_name="Rodriguez",
            role="vendor"
        )
        user3.set_password("password123")
        db.session.add(user3)
        db.session.flush()
        
        business3 = BusinessProfile(
            user_id=user3.id,
            business_name="Gourmet Catering Co",
            business_type="catering",
            description="Fine dining catering for special events",
            city="San Francisco",
            country="USA"
        )
        db.session.add(business3)
        
        vendor2_id = f"vnd_{uuid.uuid4().hex[:12]}"
        vendor2 = Vendor(
            vendor_id=vendor2_id,
            user_id=user3.id,
            business_name="Gourmet Catering Co",
            category="catering",
            description="Award-winning catering service specializing in contemporary cuisine",
            service_areas=["San Francisco", "Peninsula", "East Bay"],
            starting_price=75.0,
            currency="USD",
            average_rating=4.9,
            total_reviews=89,
            response_time_hours=4.0,
            is_verified=True
        )
        db.session.add(vendor2)
        
        # Sample events
        event1_id = f"evt_{uuid.uuid4().hex[:12]}"
        event1 = Event(
            event_id=event1_id,
            organizer_id=user1.id,
            title="Tech Summit 2025",
            description="Annual technology conference featuring industry leaders",
            event_type="conference",
            category="technology",
            status="planning",
            start_date=datetime.now() + timedelta(days=90),
            end_date=datetime.now() + timedelta(days=90, hours=8),
            timezone="America/Los_Angeles",
            expected_attendees=500,
            max_capacity=600,
            total_budget=150000.0,
            currency="USD",
            visibility="public"
        )
        db.session.add(event1)
        
        event2_id = f"evt_{uuid.uuid4().hex[:12]}"
        event2 = Event(
            event_id=event2_id,
            organizer_id=user1.id,
            title="Wedding - Sarah & Mike",
            description="Beautiful outdoor wedding ceremony and reception",
            event_type="wedding",
            category="personal",
            status="confirmed",
            start_date=datetime.now() + timedelta(days=45),
            end_date=datetime.now() + timedelta(days=45, hours=6),
            timezone="America/Los_Angeles",
            expected_attendees=120,
            max_capacity=150,
            total_budget=45000.0,
            currency="USD",
            visibility="private"
        )
        db.session.add(event2)
        
        db.session.commit()
        print("Sample data seeded successfully!")

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return {
        'status': 'healthy',
        'service': 'EventGrid API',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat()
    }

# Serve static files (for frontend)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return {
                'message': 'EventGrid API is running',
                'endpoints': [
                    '/api/health',
                    '/api/auth/register',
                    '/api/auth/login',
                    '/api/events',
                    '/api/marketplace/vendors',
                    '/api/bookings',
                    '/api/payments/create-payment-intent',
                    '/api/ai/event-designer',
                    '/api/ar/venues/{venue_id}/ar-data'
                ]
            }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

