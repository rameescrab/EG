from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import Vendor, User, db
from sqlalchemy import or_, and_

marketplace_bp = Blueprint('marketplace', __name__)

@marketplace_bp.route('/marketplace/vendors', methods=['GET'])
@jwt_required()
def search_vendors():
    try:
        # Get query parameters
        query_text = request.args.get('query', '')
        category = request.args.get('category')
        location = request.args.get('location')
        min_rating = request.args.get('rating', type=float)
        page = request.args.get('page', 1, type=int)
        limit = min(request.args.get('limit', 20, type=int), 100)
        sort_by = request.args.get('sort', 'rating_desc')
        
        # Build query
        query = Vendor.query.filter_by(is_active=True)
        
        # Text search
        if query_text:
            query = query.filter(
                or_(
                    Vendor.business_name.ilike(f'%{query_text}%'),
                    Vendor.description.ilike(f'%{query_text}%'),
                    Vendor.category.ilike(f'%{query_text}%')
                )
            )
        
        # Category filter
        if category:
            query = query.filter_by(category=category)
        
        # Location filter (simplified - search in service areas)
        if location:
            query = query.filter(
                Vendor.service_areas.contains([location])
            )
        
        # Rating filter
        if min_rating:
            query = query.filter(Vendor.average_rating >= min_rating)
        
        # Sorting
        if sort_by == 'rating_desc':
            query = query.order_by(Vendor.average_rating.desc())
        elif sort_by == 'rating_asc':
            query = query.order_by(Vendor.average_rating.asc())
        elif sort_by == 'price_asc':
            query = query.order_by(Vendor.starting_price.asc())
        elif sort_by == 'price_desc':
            query = query.order_by(Vendor.starting_price.desc())
        elif sort_by == 'name_asc':
            query = query.order_by(Vendor.business_name.asc())
        else:
            query = query.order_by(Vendor.created_at.desc())
        
        # Paginate
        vendors = query.paginate(
            page=page, per_page=limit, error_out=False
        )
        
        # Get available categories for filters
        available_categories = db.session.query(Vendor.category.distinct()).filter_by(is_active=True).all()
        categories = [cat[0] for cat in available_categories if cat[0]]
        
        return jsonify({
            'success': True,
            'data': {
                'vendors': [vendor.to_dict() for vendor in vendors.items],
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'total': vendors.total,
                    'totalPages': vendors.pages
                },
                'filters': {
                    'appliedFilters': {
                        'query': query_text,
                        'category': category,
                        'location': location,
                        'minRating': min_rating
                    },
                    'availableFilters': {
                        'categories': categories,
                        'sortOptions': [
                            {'value': 'rating_desc', 'label': 'Highest Rated'},
                            {'value': 'rating_asc', 'label': 'Lowest Rated'},
                            {'value': 'price_asc', 'label': 'Price: Low to High'},
                            {'value': 'price_desc', 'label': 'Price: High to Low'},
                            {'value': 'name_asc', 'label': 'Name: A to Z'},
                            {'value': 'newest', 'label': 'Newest First'}
                        ]
                    }
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while searching vendors'
            }
        }), 500

@marketplace_bp.route('/marketplace/vendors/<vendor_id>', methods=['GET'])
@jwt_required()
def get_vendor_details(vendor_id):
    try:
        vendor = Vendor.query.filter_by(vendor_id=vendor_id, is_active=True).first()
        
        if not vendor:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VENDOR_NOT_FOUND',
                    'message': 'Vendor not found'
                }
            }), 404
        
        # Get vendor's user profile for additional details
        user = User.query.get(vendor.user_id)
        vendor_data = vendor.to_dict()
        
        if user and user.business_profile:
            vendor_data['businessProfile'].update({
                'website': user.business_profile.website,
                'phone': user.business_profile.phone,
                'address': user.business_profile.address
            })
        
        return jsonify({
            'success': True,
            'data': {
                'vendor': vendor_data
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while fetching vendor details'
            }
        }), 500

@marketplace_bp.route('/marketplace/categories', methods=['GET'])
@jwt_required()
def get_categories():
    try:
        # Get all unique categories from active vendors
        categories = db.session.query(Vendor.category.distinct()).filter_by(is_active=True).all()
        category_list = [cat[0] for cat in categories if cat[0]]
        
        # Get vendor count for each category
        category_data = []
        for category in category_list:
            count = Vendor.query.filter_by(category=category, is_active=True).count()
            category_data.append({
                'name': category,
                'count': count,
                'slug': category.lower().replace(' ', '_')
            })
        
        # Sort by count descending
        category_data.sort(key=lambda x: x['count'], reverse=True)
        
        return jsonify({
            'success': True,
            'data': {
                'categories': category_data
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while fetching categories'
            }
        }), 500

@marketplace_bp.route('/marketplace/featured', methods=['GET'])
@jwt_required()
def get_featured_vendors():
    try:
        # Get top-rated vendors with at least 5 reviews
        featured_vendors = Vendor.query.filter(
            and_(
                Vendor.is_active == True,
                Vendor.total_reviews >= 5,
                Vendor.average_rating >= 4.5
            )
        ).order_by(
            Vendor.average_rating.desc(),
            Vendor.total_reviews.desc()
        ).limit(12).all()
        
        return jsonify({
            'success': True,
            'data': {
                'vendors': [vendor.to_dict() for vendor in featured_vendors]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while fetching featured vendors'
            }
        }), 500

