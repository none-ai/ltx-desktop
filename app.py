import os
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request, g
import logging
import uuid
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['VERSION'] = '1.2.0'
app.config['APP_NAME'] = 'LTX Desktop'
app.config['RATE_LIMIT'] = os.environ.get('RATE_LIMIT', '100 per hour')

# Simple in-memory rate limiting
rate_limit_storage = {}

def rate_limit(limit=60, period=60):
    """Rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            now = datetime.utcnow()
            key = f"{client_ip}:{f.__name__}"
            
            if key not in rate_limit_storage:
                rate_limit_storage[key] = []
            
            # Clean old requests
            rate_limit_storage[key] = [
                t for t in rate_limit_storage[key] 
                if now - t < timedelta(seconds=period)
            ]
            
            if len(rate_limit_storage[key]) >= limit:
                return jsonify({
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Limit: {limit} per {period} seconds"
                }), 429
            
            rate_limit_storage[key].append(now)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Request ID middleware
@app.before_request
def before_request():
    g.request_id = str(uuid.uuid8())[:8]
    logger.info(f"[{g.request_id}] {request.method} {request.path}")

@app.after_request
def after_request(response):
    logger.info(f"[{g.request_id}] Status: {response.status_code}")
    response.headers['X-Request-ID'] = g.request_id
    return response


@app.route('/')
def home():
    """Home page with product information"""
    return render_template('home.html', title="Home")


@app.route('/features')
def features():
    """Features page showcasing product capabilities"""
    features_list = [
        {
            "icon": "🚀",
            "title": "Lightning Fast",
            "description": "Experience blazing fast performance with optimized code and efficient resource management."
        },
        {
            "icon": "🎨",
            "title": "Modern UI",
            "description": "Beautiful, intuitive interface designed for the modern user experience."
        },
        {
            "icon": "🔄",
            "title": "Real-time Sync",
            "description": "Keep your data synchronized across all devices in real-time."
        },
        {
            "icon": "🔒",
            "title": "Secure",
            "description": "Enterprise-grade security to protect your data and privacy."
        },
        {
            "icon": "⚙️",
            "title": "Customizable",
            "description": "Adapt the application to your workflow with extensive customization options."
        },
        {
            "icon": "📊",
            "title": "Analytics",
            "description": "Built-in analytics to help you understand and improve your productivity."
        }
    ]
    return render_template('features.html', title="Features", features=features_list)


@app.route('/about')
def about():
    """About page describing the product and mission"""
    return render_template('about.html', title="About")


@app.route('/contact')
def contact():
    """Contact page with contact information and form"""
    return render_template('contact.html', title="Contact")


@app.route('/api/info')
def api_info():
    """API endpoint returning application information"""
    return jsonify({
        "name": app.config['APP_NAME'],
        "version": app.config['VERSION'],
        "description": "A powerful desktop application for modern workflows",
        "product_hunt": True,
        "routes": {
            "/": "Home page",
            "/features": "Features page",
            "/about": "About page",
            "/contact": "Contact page",
            "/api/info": "API information",
            "/api/health": "Health check endpoint"
        },
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route('/api/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        "status": "healthy",
        "service": app.config['APP_NAME'],
        "version": app.config['VERSION'],
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": "operational"
    })


@app.route('/api/stats')
@rate_limit(limit=30, period=60)
def api_stats():
    """API endpoint returning application statistics"""
    return jsonify({
        "total_routes": len(list(app.url_map.iter_rules())),
        "version": app.config['VERSION'],
        "rate_limit": app.config['RATE_LIMIT'],
        "features": [
            "Lightning Fast",
            "Modern UI", 
            "Real-time Sync",
            "Secure",
            "Customizable",
            "Analytics"
        ],
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route('/api/features')
@rate_limit(limit=30, period=60)
def api_features():
    """API endpoint returning feature list"""
    features_list = [
        {
            "id": "fast",
            "icon": "🚀",
            "title": "Lightning Fast",
            "description": "Experience blazing fast performance with optimized code and efficient resource management.",
            "status": "active"
        },
        {
            "id": "ui",
            "icon": "🎨",
            "title": "Modern UI",
            "description": "Beautiful, intuitive interface designed for the modern user experience.",
            "status": "active"
        },
        {
            "id": "sync",
            "icon": "🔄",
            "title": "Real-time Sync",
            "description": "Keep your data synchronized across all devices in real-time.",
            "status": "active"
        },
        {
            "id": "security",
            "icon": "🔒",
            "title": "Secure",
            "description": "Enterprise-grade security to protect your data and privacy.",
            "status": "active"
        },
        {
            "id": "custom",
            "icon": "⚙️",
            "title": "Customizable",
            "description": "Adapt the application to your workflow with extensive customization options.",
            "status": "active"
        },
        {
            "id": "analytics",
            "icon": "📊",
            "title": "Analytics",
            "description": "Built-in analytics to help you understand and improve your productivity.",
            "status": "active"
        }
    ]
    return jsonify({
        "features": features_list,
        "total": len(features_list),
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route('/api/routes')
@rate_limit(limit=20, period=60)
def api_routes():
    """API endpoint listing all available routes"""
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            "path": rule.rule,
            "methods": list(rule.methods - {'HEAD', 'OPTIONS'}),
            "endpoint": rule.endpoint
        })
    return jsonify({
        "routes": routes,
        "total": len(routes),
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route('/api/contact', methods=['POST'])
def contact_submit():
    """Handle contact form submissions"""
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid request data"
        }), 400

    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    if not all([name, email, message]):
        return jsonify({
            "success": False,
            "message": "Missing required fields"
        }), 400

    # In production, you would save this to a database or send an email
    # For now, we'll just return a success response
    return jsonify({
        "success": True,
        "message": "Thank you for your message! We'll get back to you soon.",
        "data": {
            "name": name,
            "email": email,
            "received_at": datetime.utcnow().isoformat()
        }
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    logger.warning(f"404 Not Found: {request.path}")
    return jsonify({
        "error": "Not Found",
        "message": "The requested resource was not found",
        "status": 404,
        "request_id": g.request_id
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"500 Internal Error: {error}")
    return jsonify({
        "error": "Internal Server Error",
        "message": "Something went wrong on our end",
        "status": 500,
        "request_id": g.request_id
    }), 500


if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
