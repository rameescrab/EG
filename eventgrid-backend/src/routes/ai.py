from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User, Event, db
import json
from datetime import datetime

ai_bp = Blueprint('ai', __name__)

# Mock AI service for deployment (replace with actual OpenAI integration in production)

@ai_bp.route('/ai/event-designer', methods=['POST'])
@jwt_required()
def ai_event_designer():
    """AI-powered event design suggestions"""
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
        required_fields = ['eventType', 'attendeeCount', 'budget', 'vibe']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': f'Missing required field: {field}'
                    }
                }), 400
        
        # Build AI prompt
        prompt = f"""
        You are an expert event designer. Create a comprehensive event design recommendation based on the following requirements:
        
        Event Type: {data['eventType']}
        Expected Attendees: {data['attendeeCount']}
        Budget: ${data['budget']} {data.get('currency', 'USD')}
        Desired Vibe/Atmosphere: {data['vibe']}
        Additional Notes: {data.get('additionalNotes', 'None')}
        
        Please provide a detailed JSON response with the following structure:
        {{
            "theme": {{
                "name": "Theme name",
                "description": "Detailed theme description",
                "keywords": ["keyword1", "keyword2", "keyword3"]
            }},
            "colorPalette": {{
                "primary": "#hexcolor",
                "secondary": "#hexcolor",
                "accent": "#hexcolor",
                "neutral": "#hexcolor",
                "description": "Color palette explanation"
            }},
            "layout": {{
                "style": "Layout style (e.g., theater, cocktail, banquet)",
                "description": "Layout recommendations",
                "suggestions": ["suggestion1", "suggestion2", "suggestion3"]
            }},
            "decorElements": [
                {{
                    "category": "Category (e.g., lighting, flowers, furniture)",
                    "items": ["item1", "item2", "item3"],
                    "description": "Why these elements work"
                }}
            ],
            "timeline": [
                {{
                    "phase": "Phase name",
                    "timeframe": "Time before event",
                    "tasks": ["task1", "task2", "task3"]
                }}
            ],
            "budgetBreakdown": [
                {{
                    "category": "Category name",
                    "percentage": 25,
                    "estimatedCost": 1000,
                    "description": "What this covers"
                }}
            ],
            "vendorRecommendations": [
                {{
                    "category": "Vendor type",
                    "priority": "high/medium/low",
                    "description": "What to look for"
                }}
            ]
        }}
        
        Make sure all recommendations are practical, budget-appropriate, and align with the specified vibe and event type.
        """
        
        try:
            # Use a mock response for demonstration since we don't have a real OpenAI API key
            # In production, you would use: response = openai.ChatCompletion.create(...)
            
            # Mock AI response based on event type and vibe
            mock_response = generate_mock_ai_response(data)
            
            return jsonify({
                'success': True,
                'data': {
                    'designRecommendation': mock_response,
                    'generatedAt': datetime.utcnow().isoformat(),
                    'inputParameters': {
                        'eventType': data['eventType'],
                        'attendeeCount': data['attendeeCount'],
                        'budget': data['budget'],
                        'vibe': data['vibe']
                    }
                }
            }), 200
            
        except Exception as ai_error:
            # Fallback to mock response if AI service fails
            mock_response = generate_mock_ai_response(data)
            
            return jsonify({
                'success': True,
                'data': {
                    'designRecommendation': mock_response,
                    'generatedAt': datetime.utcnow().isoformat(),
                    'note': 'Generated using fallback recommendations',
                    'inputParameters': {
                        'eventType': data['eventType'],
                        'attendeeCount': data['attendeeCount'],
                        'budget': data['budget'],
                        'vibe': data['vibe']
                    }
                }
            }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while generating design recommendations'
            }
        }), 500

@ai_bp.route('/ai/vendor-recommendations', methods=['POST'])
@jwt_required()
def ai_vendor_recommendations():
    """AI-powered vendor recommendations based on event requirements"""
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
        
        # Get event details if event ID provided
        event = None
        if data.get('eventId'):
            event = Event.query.filter_by(event_id=data['eventId'], organizer_id=user.id).first()
        
        # Generate vendor recommendations
        recommendations = generate_vendor_recommendations(data, event)
        
        return jsonify({
            'success': True,
            'data': {
                'recommendations': recommendations,
                'generatedAt': datetime.utcnow().isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while generating vendor recommendations'
            }
        }), 500

@ai_bp.route('/ai/schedule-optimizer', methods=['POST'])
@jwt_required()
def ai_schedule_optimizer():
    """AI-powered event schedule optimization"""
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
        
        # Generate optimized schedule
        optimized_schedule = generate_optimized_schedule(data)
        
        return jsonify({
            'success': True,
            'data': {
                'optimizedSchedule': optimized_schedule,
                'generatedAt': datetime.utcnow().isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while optimizing schedule'
            }
        }), 500

def generate_mock_ai_response(data):
    """Generate mock AI response based on event parameters"""
    event_type = data['eventType'].lower()
    vibe = data['vibe'].lower()
    budget = data['budget']
    attendees = data['attendeeCount']
    
    # Theme suggestions based on event type and vibe
    themes = {
        'wedding': {
            'elegant': {
                'name': 'Timeless Elegance',
                'description': 'Classic sophistication with modern touches, featuring clean lines and luxurious details',
                'keywords': ['elegant', 'timeless', 'sophisticated', 'romantic']
            },
            'rustic': {
                'name': 'Rustic Romance',
                'description': 'Charming countryside aesthetic with natural elements and warm, inviting atmosphere',
                'keywords': ['rustic', 'natural', 'cozy', 'romantic']
            }
        },
        'conference': {
            'professional': {
                'name': 'Modern Professional',
                'description': 'Clean, contemporary design that promotes focus and networking',
                'keywords': ['professional', 'modern', 'clean', 'focused']
            },
            'innovative': {
                'name': 'Innovation Hub',
                'description': 'Cutting-edge design with tech-forward elements and dynamic spaces',
                'keywords': ['innovative', 'tech', 'dynamic', 'forward-thinking']
            }
        }
    }
    
    # Color palettes
    color_palettes = {
        'elegant': {
            'primary': '#2C3E50',
            'secondary': '#ECF0F1',
            'accent': '#E74C3C',
            'neutral': '#BDC3C7',
            'description': 'Sophisticated navy and silver with elegant red accents'
        },
        'rustic': {
            'primary': '#8B4513',
            'secondary': '#F5DEB3',
            'accent': '#228B22',
            'neutral': '#D2B48C',
            'description': 'Warm earth tones with natural green accents'
        },
        'professional': {
            'primary': '#34495E',
            'secondary': '#FFFFFF',
            'accent': '#3498DB',
            'neutral': '#95A5A6',
            'description': 'Clean corporate colors with professional blue accents'
        }
    }
    
    # Select appropriate theme and colors
    theme_key = 'elegant' if 'elegant' in vibe else ('rustic' if 'rustic' in vibe else 'professional')
    selected_theme = themes.get(event_type, {}).get(theme_key, themes['conference']['professional'])
    selected_colors = color_palettes[theme_key]
    
    return {
        'theme': selected_theme,
        'colorPalette': selected_colors,
        'layout': {
            'style': 'Banquet' if event_type == 'wedding' else 'Theater',
            'description': f'Optimized layout for {attendees} attendees with focus on {vibe} atmosphere',
            'suggestions': [
                'Create clear sight lines to main focal point',
                'Ensure adequate space for networking/mingling',
                'Position key elements for optimal flow'
            ]
        },
        'decorElements': [
            {
                'category': 'Lighting',
                'items': ['Ambient uplighting', 'Accent spotlights', 'String lights'],
                'description': 'Layered lighting to create the perfect atmosphere'
            },
            {
                'category': 'Centerpieces',
                'items': ['Floral arrangements', 'Candles', 'Decorative elements'],
                'description': 'Eye-catching centerpieces that complement the theme'
            }
        ],
        'timeline': [
            {
                'phase': 'Planning Phase',
                'timeframe': '8-12 weeks before',
                'tasks': ['Finalize venue', 'Book key vendors', 'Send invitations']
            },
            {
                'phase': 'Preparation Phase',
                'timeframe': '2-4 weeks before',
                'tasks': ['Confirm details', 'Final headcount', 'Setup timeline']
            }
        ],
        'budgetBreakdown': [
            {
                'category': 'Venue',
                'percentage': 40,
                'estimatedCost': budget * 0.4,
                'description': 'Venue rental and basic amenities'
            },
            {
                'category': 'Catering',
                'percentage': 30,
                'estimatedCost': budget * 0.3,
                'description': 'Food and beverage service'
            },
            {
                'category': 'Decor & Entertainment',
                'percentage': 20,
                'estimatedCost': budget * 0.2,
                'description': 'Decorations, music, and entertainment'
            },
            {
                'category': 'Miscellaneous',
                'percentage': 10,
                'estimatedCost': budget * 0.1,
                'description': 'Photography, transportation, and contingency'
            }
        ],
        'vendorRecommendations': [
            {
                'category': 'Catering',
                'priority': 'high',
                'description': 'Look for caterers with experience in your event type and dietary accommodations'
            },
            {
                'category': 'Photography',
                'priority': 'high',
                'description': 'Choose photographers whose style matches your event aesthetic'
            },
            {
                'category': 'Entertainment',
                'priority': 'medium',
                'description': 'Select entertainment that fits your audience and venue acoustics'
            }
        ]
    }

def generate_vendor_recommendations(data, event=None):
    """Generate vendor recommendations based on requirements"""
    return [
        {
            'category': 'Photography',
            'priority': 'high',
            'reasoning': 'Professional photography is essential for capturing memories',
            'suggestedBudget': '10-15% of total budget',
            'keyQuestions': [
                'What photography style do you prefer?',
                'Do you need both ceremony and reception coverage?',
                'How many edited photos do you expect?'
            ]
        },
        {
            'category': 'Catering',
            'priority': 'high',
            'reasoning': 'Food quality significantly impacts guest satisfaction',
            'suggestedBudget': '25-35% of total budget',
            'keyQuestions': [
                'Any dietary restrictions to accommodate?',
                'Preferred service style (buffet, plated, family-style)?',
                'Need bar service included?'
            ]
        },
        {
            'category': 'Entertainment',
            'priority': 'medium',
            'reasoning': 'Entertainment sets the mood and keeps guests engaged',
            'suggestedBudget': '8-12% of total budget',
            'keyQuestions': [
                'Live band or DJ preference?',
                'Any specific music genres or songs?',
                'Need microphone for speeches?'
            ]
        }
    ]

def generate_optimized_schedule(data):
    """Generate optimized event schedule"""
    return {
        'timeline': [
            {
                'time': '17:00',
                'duration': 30,
                'activity': 'Guest Arrival & Cocktails',
                'description': 'Welcome guests with signature cocktails and light appetizers'
            },
            {
                'time': '17:30',
                'duration': 45,
                'activity': 'Main Event/Ceremony',
                'description': 'Core event programming with optimal timing for guest attention'
            },
            {
                'time': '18:15',
                'duration': 60,
                'activity': 'Dinner Service',
                'description': 'Seated dinner with entertainment between courses'
            },
            {
                'time': '19:15',
                'duration': 90,
                'activity': 'Entertainment & Dancing',
                'description': 'Live entertainment and open dance floor'
            }
        ],
        'optimizationNotes': [
            'Schedule accounts for natural energy flow throughout the event',
            'Meal timing optimized for guest comfort and venue logistics',
            'Buffer time included between major activities'
        ]
    }

