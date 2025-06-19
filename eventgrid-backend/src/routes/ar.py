from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User, Venue, db
import json
from datetime import datetime

ar_bp = Blueprint('ar', __name__)

@ar_bp.route('/ar/venues/<venue_id>/ar-data', methods=['GET'])
@jwt_required()
def get_venue_ar_data(venue_id):
    """Get AR visualization data for a venue"""
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
        
        venue = Venue.query.filter_by(venue_id=venue_id, is_active=True).first()
        
        if not venue:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VENUE_NOT_FOUND',
                    'message': 'Venue not found'
                }
            }), 404
        
        # Generate AR data for the venue
        ar_data = generate_venue_ar_data(venue)
        
        return jsonify({
            'success': True,
            'data': {
                'venueId': venue_id,
                'arData': ar_data,
                'generatedAt': datetime.utcnow().isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while fetching AR data'
            }
        }), 500

@ar_bp.route('/ar/venues/<venue_id>/layout-preview', methods=['POST'])
@jwt_required()
def generate_layout_preview(venue_id):
    """Generate AR layout preview for event setup"""
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
        
        venue = Venue.query.filter_by(venue_id=venue_id, is_active=True).first()
        
        if not venue:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VENUE_NOT_FOUND',
                    'message': 'Venue not found'
                }
            }), 404
        
        data = request.get_json()
        
        # Generate layout preview based on event requirements
        layout_preview = generate_ar_layout_preview(venue, data)
        
        return jsonify({
            'success': True,
            'data': {
                'venueId': venue_id,
                'layoutPreview': layout_preview,
                'generatedAt': datetime.utcnow().isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while generating layout preview'
            }
        }), 500

@ar_bp.route('/ar/venues/<venue_id>/virtual-tour', methods=['GET'])
@jwt_required()
def get_virtual_tour_data(venue_id):
    """Get virtual tour data for AR experience"""
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
        
        venue = Venue.query.filter_by(venue_id=venue_id, is_active=True).first()
        
        if not venue:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VENUE_NOT_FOUND',
                    'message': 'Venue not found'
                }
            }), 404
        
        # Generate virtual tour data
        tour_data = generate_virtual_tour_data(venue)
        
        return jsonify({
            'success': True,
            'data': {
                'venueId': venue_id,
                'virtualTour': tour_data,
                'generatedAt': datetime.utcnow().isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while fetching virtual tour data'
            }
        }), 500

@ar_bp.route('/ar/capacity-optimizer', methods=['POST'])
@jwt_required()
def optimize_capacity():
    """Optimize venue capacity using AR visualization"""
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
        venue_id = data.get('venueId')
        
        if not venue_id:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Venue ID is required'
                }
            }), 400
        
        venue = Venue.query.filter_by(venue_id=venue_id, is_active=True).first()
        
        if not venue:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VENUE_NOT_FOUND',
                    'message': 'Venue not found'
                }
            }), 404
        
        # Generate capacity optimization
        optimization = generate_capacity_optimization(venue, data)
        
        return jsonify({
            'success': True,
            'data': {
                'optimization': optimization,
                'generatedAt': datetime.utcnow().isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while optimizing capacity'
            }
        }), 500

def generate_venue_ar_data(venue):
    """Generate AR data for venue visualization"""
    return {
        'venue3DModel': {
            'modelUrl': f'/ar/models/venue_{venue.venue_id}.glb',
            'scale': [1.0, 1.0, 1.0],
            'position': [0.0, 0.0, 0.0],
            'rotation': [0.0, 0.0, 0.0]
        },
        'dimensions': {
            'length': 30.0,  # meters
            'width': 20.0,   # meters
            'height': 4.0,   # meters
            'area': 600.0    # square meters
        },
        'anchorPoints': [
            {
                'id': 'entrance',
                'position': [0.0, 0.0, -10.0],
                'label': 'Main Entrance',
                'type': 'entrance'
            },
            {
                'id': 'stage',
                'position': [0.0, 0.5, 10.0],
                'label': 'Stage Area',
                'type': 'stage'
            },
            {
                'id': 'bar',
                'position': [-8.0, 0.0, 0.0],
                'label': 'Bar Area',
                'type': 'service'
            }
        ],
        'lighting': {
            'ambientLight': {
                'intensity': 0.4,
                'color': '#FFFFFF'
            },
            'directionalLight': {
                'intensity': 0.8,
                'position': [10.0, 10.0, 5.0],
                'color': '#FFFFFF'
            }
        },
        'materials': {
            'floor': {
                'type': 'hardwood',
                'color': '#8B4513',
                'texture': '/ar/textures/hardwood.jpg'
            },
            'walls': {
                'type': 'painted',
                'color': '#F5F5F5',
                'texture': '/ar/textures/wall.jpg'
            }
        }
    }

def generate_ar_layout_preview(venue, event_data):
    """Generate AR layout preview based on event requirements"""
    attendee_count = event_data.get('attendeeCount', 100)
    event_type = event_data.get('eventType', 'conference')
    layout_style = event_data.get('layoutStyle', 'theater')
    
    # Calculate optimal layout
    if layout_style == 'theater':
        rows = max(8, attendee_count // 12)
        seats_per_row = min(12, attendee_count // rows)
    elif layout_style == 'banquet':
        tables = max(1, attendee_count // 8)
        seats_per_table = min(8, attendee_count // tables)
    else:  # cocktail
        standing_areas = max(3, attendee_count // 30)
    
    return {
        'layoutType': layout_style,
        'capacity': {
            'recommended': attendee_count,
            'maximum': venue.capacity_max,
            'optimal': min(attendee_count, int(venue.capacity_max * 0.85))
        },
        'furniture': generate_furniture_layout(layout_style, attendee_count),
        'pathways': [
            {
                'id': 'main_aisle',
                'width': 1.5,
                'points': [[0, 0, -10], [0, 0, 10]],
                'type': 'primary'
            },
            {
                'id': 'side_aisle',
                'width': 1.0,
                'points': [[-5, 0, -5], [5, 0, -5]],
                'type': 'secondary'
            }
        ],
        'emergencyExits': [
            {
                'position': [-10, 0, -8],
                'width': 2.0,
                'label': 'Emergency Exit 1'
            },
            {
                'position': [10, 0, -8],
                'width': 2.0,
                'label': 'Emergency Exit 2'
            }
        ],
        'accessibility': {
            'wheelchairAccessible': True,
            'accessibleSeating': max(2, attendee_count // 50),
            'accessiblePaths': ['main_aisle']
        }
    }

def generate_furniture_layout(layout_style, attendee_count):
    """Generate furniture layout for AR preview"""
    if layout_style == 'theater':
        return [
            {
                'type': 'chair',
                'count': attendee_count,
                'arrangement': 'rows',
                'spacing': 0.6,
                'positions': generate_theater_positions(attendee_count)
            },
            {
                'type': 'stage',
                'count': 1,
                'dimensions': [6.0, 1.0, 4.0],
                'position': [0, 0.5, 8]
            }
        ]
    elif layout_style == 'banquet':
        table_count = max(1, attendee_count // 8)
        return [
            {
                'type': 'round_table',
                'count': table_count,
                'diameter': 1.8,
                'positions': generate_banquet_positions(table_count)
            },
            {
                'type': 'chair',
                'count': attendee_count,
                'arrangement': 'around_tables',
                'positions': generate_banquet_chair_positions(table_count)
            }
        ]
    else:  # cocktail
        return [
            {
                'type': 'cocktail_table',
                'count': max(3, attendee_count // 15),
                'diameter': 0.8,
                'positions': generate_cocktail_positions(attendee_count // 15)
            },
            {
                'type': 'bar',
                'count': 1,
                'dimensions': [4.0, 1.2, 1.0],
                'position': [-8, 0, 0]
            }
        ]

def generate_theater_positions(attendee_count):
    """Generate theater seating positions"""
    positions = []
    rows = max(8, attendee_count // 12)
    seats_per_row = min(12, attendee_count // rows)
    
    for row in range(rows):
        for seat in range(seats_per_row):
            x = (seat - seats_per_row/2) * 0.6
            z = (row - rows/2) * 0.8
            positions.append([x, 0, z])
    
    return positions[:attendee_count]

def generate_banquet_positions(table_count):
    """Generate banquet table positions"""
    positions = []
    cols = int(table_count ** 0.5) + 1
    rows = (table_count + cols - 1) // cols
    
    for i in range(table_count):
        row = i // cols
        col = i % cols
        x = (col - cols/2) * 3.0
        z = (row - rows/2) * 3.0
        positions.append([x, 0, z])
    
    return positions

def generate_banquet_chair_positions(table_count):
    """Generate chair positions around banquet tables"""
    positions = []
    table_positions = generate_banquet_positions(table_count)
    
    for table_pos in table_positions:
        # 8 chairs around each table
        for i in range(8):
            angle = (i / 8) * 2 * 3.14159
            x = table_pos[0] + 1.2 * cos(angle)
            z = table_pos[2] + 1.2 * sin(angle)
            positions.append([x, 0, z])
    
    return positions

def generate_cocktail_positions(table_count):
    """Generate cocktail table positions"""
    positions = []
    for i in range(table_count):
        # Distribute tables randomly but with minimum spacing
        x = (i % 3 - 1) * 4.0
        z = (i // 3 - 1) * 4.0
        positions.append([x, 0, z])
    
    return positions

def generate_virtual_tour_data(venue):
    """Generate virtual tour waypoints and content"""
    return {
        'waypoints': [
            {
                'id': 'entrance',
                'position': [0, 1.7, -10],
                'title': 'Main Entrance',
                'description': 'Welcome to the venue. Notice the spacious foyer area.',
                'mediaUrl': f'/ar/tours/venue_{venue.venue_id}_entrance.jpg',
                'duration': 30
            },
            {
                'id': 'main_hall',
                'position': [0, 1.7, 0],
                'title': 'Main Event Space',
                'description': 'The main hall with flexible layout options.',
                'mediaUrl': f'/ar/tours/venue_{venue.venue_id}_main.jpg',
                'duration': 45
            },
            {
                'id': 'stage_area',
                'position': [0, 1.7, 8],
                'title': 'Stage & Presentation Area',
                'description': 'Professional stage with full AV capabilities.',
                'mediaUrl': f'/ar/tours/venue_{venue.venue_id}_stage.jpg',
                'duration': 30
            }
        ],
        'navigation': {
            'autoAdvance': True,
            'advanceDelay': 5000,
            'allowManualControl': True
        },
        'interactions': [
            {
                'type': 'hotspot',
                'position': [-8, 1.5, 0],
                'label': 'Bar Area',
                'action': 'show_info',
                'content': 'Full service bar with professional bartending staff available.'
            },
            {
                'type': 'measurement',
                'startPosition': [-10, 0, -10],
                'endPosition': [10, 0, 10],
                'label': 'Room Dimensions',
                'value': '20m x 20m'
            }
        ]
    }

def generate_capacity_optimization(venue, requirements):
    """Generate capacity optimization recommendations"""
    target_capacity = requirements.get('targetCapacity', 100)
    event_type = requirements.get('eventType', 'conference')
    accessibility_needs = requirements.get('accessibilityNeeds', False)
    
    # Calculate optimal capacity based on venue and requirements
    max_capacity = venue.capacity_max
    recommended_capacity = min(target_capacity, int(max_capacity * 0.85))
    
    return {
        'analysis': {
            'requestedCapacity': target_capacity,
            'venueMaximum': max_capacity,
            'recommendedCapacity': recommended_capacity,
            'utilizationRate': (recommended_capacity / max_capacity) * 100
        },
        'optimizations': [
            {
                'category': 'Layout',
                'recommendation': f'Use {get_optimal_layout(event_type)} layout for maximum efficiency',
                'impact': 'Increases usable capacity by 15%'
            },
            {
                'category': 'Flow',
                'recommendation': 'Position entrance and exits to minimize congestion',
                'impact': 'Improves guest experience and safety'
            },
            {
                'category': 'Accessibility',
                'recommendation': 'Reserve 2% of capacity for accessibility needs',
                'impact': 'Ensures compliance and inclusivity'
            }
        ],
        'warnings': generate_capacity_warnings(target_capacity, max_capacity),
        'alternatives': [
            {
                'layout': 'theater',
                'capacity': int(max_capacity * 0.9),
                'description': 'Maximum capacity with theater-style seating'
            },
            {
                'layout': 'banquet',
                'capacity': int(max_capacity * 0.7),
                'description': 'Comfortable dining with round tables'
            },
            {
                'layout': 'cocktail',
                'capacity': int(max_capacity * 1.2),
                'description': 'Standing reception with high-top tables'
            }
        ]
    }

def get_optimal_layout(event_type):
    """Get optimal layout for event type"""
    layouts = {
        'conference': 'theater',
        'wedding': 'banquet',
        'networking': 'cocktail',
        'presentation': 'theater',
        'gala': 'banquet'
    }
    return layouts.get(event_type, 'theater')

def generate_capacity_warnings(target, maximum):
    """Generate capacity warnings if needed"""
    warnings = []
    
    if target > maximum:
        warnings.append({
            'type': 'overcapacity',
            'message': f'Requested capacity ({target}) exceeds venue maximum ({maximum})',
            'severity': 'high'
        })
    
    if target > maximum * 0.9:
        warnings.append({
            'type': 'comfort',
            'message': 'High capacity may impact guest comfort and movement',
            'severity': 'medium'
        })
    
    return warnings

# Helper functions for math operations
def cos(angle):
    import math
    return math.cos(angle)

def sin(angle):
    import math
    return math.sin(angle)

