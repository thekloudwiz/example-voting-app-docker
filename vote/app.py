from flask import Flask, render_template, request, make_response, g, jsonify, send_from_directory, render_template_string
from redis import Redis
import os
import socket
import random
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
option_a = os.getenv('OPTION_A', "Cats")
option_b = os.getenv('OPTION_B', "Dogs")
hostname = socket.gethostname()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Security headers middleware
@app.after_request
def add_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://code.jquery.com https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
        "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
        "img-src 'self' data:; "
        "media-src 'self'; "
        "connect-src 'self';"
    )
    return response

def get_redis():
    """Get Redis connection with error handling"""
    if not hasattr(g, 'redis'):
        try:
            g.redis = Redis(host="redis", db=0, socket_timeout=5, socket_connect_timeout=5)
            # Test connection
            g.redis.ping()
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            g.redis = None
    return g.redis

def get_vote_stats():
    """Get current vote statistics from database"""
    try:
        # Try to get stats from database first (more accurate)
        import psycopg2
        conn = psycopg2.connect(
            host=os.environ.get('POSTGRES_HOST', 'db'),
            database=os.environ.get('POSTGRES_DB', 'postgres'),
            user=os.environ.get('POSTGRES_USER', 'postgres'),
            password=os.environ.get('POSTGRES_PASSWORD', 'postgres')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT vote, COUNT(*) FROM votes GROUP BY vote")
        results = cursor.fetchall()
        
        vote_counts = {'a': 0, 'b': 0}
        for vote, count in results:
            if vote in ['a', 'b']:
                vote_counts[vote] = count
        
        cursor.close()
        conn.close()
        
        total = vote_counts['a'] + vote_counts['b']
        return {
            'a': vote_counts['a'],
            'b': vote_counts['b'],
            'total': total
        }
    except Exception as e:
        logger.warning(f"Could not get stats from database: {e}")
        # Fallback to Redis (original logic)
        redis = get_redis()
        if not redis:
            return {'a': 0, 'b': 0, 'total': 0}
        
        try:
            # Get all votes from Redis
            votes = redis.lrange('votes', 0, -1)
            vote_counts = {'a': 0, 'b': 0}
            
            for vote_data in votes:
                try:
                    vote = json.loads(vote_data.decode('utf-8'))
                    if vote.get('vote') in ['a', 'b']:
                        vote_counts[vote['vote']] += 1
                except (json.JSONDecodeError, UnicodeDecodeError):
                    continue
            
            total = vote_counts['a'] + vote_counts['b']
            return {
                'a': vote_counts['a'],
                'b': vote_counts['b'],
                'total': total
            }
        except Exception as redis_error:
            logger.error(f"Error getting vote stats: {redis_error}")
            return {'a': 0, 'b': 0, 'total': 0}

@app.route("/", methods=['POST', 'GET'])
def vote():
    """Main voting route with modern UI"""
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None
    error_message = None

    if request.method == 'POST':
        redis = get_redis()
        if redis:
            try:
                vote_option = request.form.get('vote')
                if vote_option in ['a', 'b']:
                    vote = vote_option
                    data = json.dumps({
                        'voter_id': voter_id, 
                        'vote': vote,
                        'timestamp': datetime.utcnow().isoformat()
                    })
                    redis.rpush('votes', data)
                    logger.info(f"Vote recorded: {vote} from {voter_id}")
                else:
                    error_message = "Invalid vote option"
            except Exception as e:
                logger.error(f"Error recording vote: {e}")
                error_message = "Failed to record vote. Please try again."
        else:
            error_message = "Service temporarily unavailable. Please try again."

    # Check if request wants JSON response (for AJAX)
    if request.headers.get('Content-Type') == 'application/json' or request.args.get('format') == 'json':
        stats = get_vote_stats()
        return jsonify({
            'vote': vote,
            'error': error_message,
            'stats': stats,
            'hostname': hostname
        })

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
        error=error_message,
    ))
    resp.set_cookie('voter_id', voter_id, max_age=30*24*60*60)  # 30 days
    return resp

@app.route("/classic")
def classic_vote():
    """Original voting interface for comparison"""
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=None,
    ))
    resp.set_cookie('voter_id', voter_id, max_age=30*24*60*60)
    return resp

@app.route("/api/stats")
def api_stats():
    """API endpoint for vote statistics"""
    stats = get_vote_stats()
    return jsonify({
        'votes': stats,
        'options': {
            'a': option_a,
            'b': option_b
        },
        'hostname': hostname,
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route("/api/health")
def health_check():
    """Health check endpoint"""
    redis = get_redis()
    redis_status = "connected" if redis else "disconnected"
    
    return jsonify({
        'status': 'healthy',
        'redis': redis_status,
        'hostname': hostname,
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route("/sw.js")
def service_worker():
    """Serve service worker"""
    return send_from_directory('static', 'sw.js', mimetype='application/javascript')

@app.route("/manifest.json")
def manifest():
    """PWA manifest"""
    return jsonify({
        "name": "Modern Voting App",
        "short_name": "VoteApp",
        "description": "A modern voting application with real-time results",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#f9fafb",
        "theme_color": "#3b82f6",
        "icons": [
            {
                "src": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🗳️</text></svg>",
                "sizes": "192x192",
                "type": "image/svg+xml"
            },
            {
                "src": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🗳️</text></svg>",
                "sizes": "512x512",
                "type": "image/svg+xml"
            }
        ]
    })

@app.route("/offline.html")
def offline():
    """Offline page for PWA"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Offline - Voting App</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
                color: #374151;
            }
            .offline-container {
                text-align: center;
                padding: 2rem;
                background: white;
                border-radius: 1rem;
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
                max-width: 400px;
            }
            .offline-icon {
                font-size: 4rem;
                margin-bottom: 1rem;
            }
            h1 {
                margin-bottom: 0.5rem;
                color: #1f2937;
            }
            p {
                color: #6b7280;
                margin-bottom: 1.5rem;
            }
            .retry-btn {
                background: #3b82f6;
                color: white;
                border: none;
                padding: 0.75rem 1.5rem;
                border-radius: 0.5rem;
                cursor: pointer;
                font-weight: 600;
                transition: background-color 0.2s;
            }
            .retry-btn:hover {
                background: #2563eb;
            }
        </style>
    </head>
    <body>
        <div class="offline-container">
            <div class="offline-icon">📡</div>
            <h1>You're Offline</h1>
            <p>Please check your internet connection and try again.</p>
            <button class="retry-btn" onclick="window.location.reload()">
                Try Again
            </button>
        </div>
    </body>
    </html>
    """

@app.errorhandler(404)
def not_found(error):
    """Custom 404 page"""
    logger.warning(f"404 error: {request.url}")
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Page Not Found - Voting App</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
                color: #374151;
            }
            .error-container {
                text-align: center;
                padding: 2rem;
                background: white;
                border-radius: 1rem;
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
                max-width: 400px;
            }
            .error-code {
                font-size: 6rem;
                font-weight: 800;
                color: #3b82f6;
                margin-bottom: 1rem;
            }
            h1 {
                margin-bottom: 0.5rem;
                color: #1f2937;
            }
            p {
                color: #6b7280;
                margin-bottom: 1.5rem;
            }
            .home-btn {
                background: #3b82f6;
                color: white;
                border: none;
                padding: 0.75rem 1.5rem;
                border-radius: 0.5rem;
                cursor: pointer;
                font-weight: 600;
                text-decoration: none;
                display: inline-block;
                transition: background-color 0.2s;
            }
            .home-btn:hover {
                background: #2563eb;
            }
        </style>
    </head>
    <body>
        <main class="error-container" role="main">
            <div class="error-code" aria-label="Error code 404">404</div>
            <h1>Page Not Found</h1>
            <p>The page you're looking for doesn't exist.</p>
            <a href="/" class="home-btn" role="button">Go Home</a>
        </main>
    </body>
    </html>
    """), 404

@app.errorhandler(500)
def internal_error(error):
    """Custom 500 page"""
    logger.error(f"Internal server error: {error}")
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Server Error - Voting App</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
                color: #374151;
            }
            .error-container {
                text-align: center;
                padding: 2rem;
                background: white;
                border-radius: 1rem;
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
                max-width: 400px;
            }
            .error-code {
                font-size: 6rem;
                font-weight: 800;
                color: #ef4444;
                margin-bottom: 1rem;
            }
            h1 {
                margin-bottom: 0.5rem;
                color: #1f2937;
            }
            p {
                color: #6b7280;
                margin-bottom: 1.5rem;
            }
            .home-btn {
                background: #ef4444;
                color: white;
                border: none;
                padding: 0.75rem 1.5rem;
                border-radius: 0.5rem;
                cursor: pointer;
                font-weight: 600;
                text-decoration: none;
                display: inline-block;
                transition: background-color 0.2s;
            }
            .home-btn:hover {
                background: #dc2626;
            }
        </style>
    </head>
    <body>
        <main class="error-container" role="main">
            <div class="error-code" aria-label="Error code 500">500</div>
            <h1>Server Error</h1>
            <p>Something went wrong on our end. Please try again later.</p>
            <a href="/" class="home-btn" role="button">Go Home</a>
        </main>
    </body>
    </html>
    """), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
