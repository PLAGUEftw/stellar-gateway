"""
Stellar Gateway - Main Application
Complete Flask app with MongoDB integration
"""
import requests
import os

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps

from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["stellar_gateway"]

from database import (
    Database, 
    UserManager, 
    ActivityManager, 
    FavoritesManager,
    PlanetManager,
    MissionManager
)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'stellar-gateway-default-key')
app.permanent_session_lifetime = timedelta(days=7)

# Initialize managers
user_manager = UserManager()
activity_manager = ActivityManager()
favorites_manager = FavoritesManager()
planet_manager = PlanetManager()
mission_manager = MissionManager()


# ==================== DECORATORS ====================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ==================== ROUTES ====================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not all([username, email, password, confirm_password]):
            flash('All fields are required!', 'error')
            return render_template('register.html')
        
        if len(username) < 3:
            flash('Username must be at least 3 characters long', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')
        
        # Check if user exists
        existing_user = user_manager.find_by_username_or_email(username)
        if existing_user:
            flash('Username already exists!', 'error')
            return render_template('register.html')
        
        existing_email = user_manager.find_user({'email': email})
        if existing_email:
            flash('Email already registered!', 'error')
            return render_template('register.html')
        
        # Create user
        user_data = {
            'username': username,
            'email': email,
            'password': generate_password_hash(password)
        }
        
        result = user_manager.create_user(user_data)
        
        if result['success']:
            activity_manager.log_activity(
                result['user_id'],
                'user_registered',
                {'username': username, 'ip': request.remote_addr}
            )
            flash('🚀 Account created successfully! Welcome to Stellar Gateway!', 'success')
            return redirect(url_for('login'))
        else:
            flash(f'Error: {result["error"]}', 'error')
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'
        
        if not username or not password:
            flash('Please enter both username and password', 'error')
            return render_template('login.html')
        
        user = user_manager.find_by_username_or_email(username)
        
        if user and check_password_hash(user['password'], password):
            session.permanent = remember
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            session['email'] = user['email']
            session['rank'] = user.get('rank', 'Cadet')
            
            user_manager.update_last_login(user['_id'])
            activity_manager.log_activity(
                str(user['_id']),
                'user_login',
                {'ip': request.remote_addr}
            )
            
            flash(f'🌟 Welcome back, Commander {user["username"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    username = session.get('username', 'Explorer')
    if 'user_id' in session:
        activity_manager.log_activity(
            session['user_id'],
            'user_logout',
            {'ip': request.remote_addr}
        )
    session.clear()
    flash(f'👋 Safe travels, Commander {username}!', 'info')
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    user = user_manager.find_by_id(session['user_id'])
    planets = planet_manager.get_all_planets()[:4]
    missions = mission_manager.get_all_missions()[:3]
    activities = activity_manager.get_user_activities(session['user_id'], 5)
    favorites_count = len(favorites_manager.get_user_favorites(session['user_id']))
    
    stats = {
        'explorations': user.get('explorations', 0) if user else 0,
        'rank': user.get('rank', 'Cadet') if user else 'Cadet',
        'favorites': favorites_count,
        'login_count': user.get('login_count', 0) if user else 0
    }
    
    return render_template('dashboard.html',
                         username=session.get('username'),
                         planets=planets,
                         missions=missions,
                         activities=activities,
                         stats=stats)


@app.route('/planets')
@login_required
def planets():
    planets_list = planet_manager.get_all_planets()
    user_favorites = favorites_manager.get_user_favorites(
        session['user_id'], 'planet'
    )
    favorite_names = [f['item_name'] for f in user_favorites]
    
    user_manager.increment_exploration(session['user_id'])
    activity_manager.log_activity(
        session['user_id'],
        'viewed_planets',
        {'ip': request.remote_addr}
    )
    
    return render_template('planets.html', 
                         planets=planets_list,
                         favorites=favorite_names)


@app.route('/missions')
@login_required
def missions():
    missions_list = mission_manager.get_all_missions()
    user_manager.increment_exploration(session['user_id'])
    activity_manager.log_activity(
        session['user_id'],
        'viewed_missions',
        {'ip': request.remote_addr}
    )
    return render_template('missions.html', missions=missions_list)


@app.route('/gallery')
@login_required
def gallery():
    user_manager.increment_exploration(session['user_id'])
    activity_manager.log_activity(
        session['user_id'],
        'viewed_gallery',
        {'ip': request.remote_addr}
    )

    # ✅ USE MONGODB
    gallery_items = list(db.gallery.find())

    return render_template('gallery.html', gallery_items=gallery_items)


@app.route('/planet-surfaces')
@login_required
def planet_surfaces():
    planet_items = list(db.planet_surface.find())   # ✅ FIX HERE
    return render_template("planet_surfaces.html", planet_items=planet_items)

@app.route('/nasa-gallery')
@login_required
def nasa_gallery():
    API_KEY = os.getenv("NASA_API_KEY")

    url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&count=20"

    try:
        response = requests.get(url, timeout=5)

        # 🔥 Check if response is OK
        if response.status_code != 200:
            print("NASA API ERROR:", response.status_code)
            return render_template("nasa_gallery.html", gallery_items=[])

        # 🔥 Safe JSON parsing
        try:
            data = response.json()
        except:
            print("Invalid JSON from NASA API")
            return render_template("nasa_gallery.html", gallery_items=[])

        gallery_items = []

        # Handle single object
        if isinstance(data, dict):
            data = [data]

        for item in data:
            if isinstance(item, dict) and item.get("media_type") == "image":
                gallery_items.append({
                    "title": item.get("title"),
                    "desc": item.get("explanation", "")[:100] + "...",
                    "image": item.get("url")
                })

        return render_template("nasa_gallery.html", gallery_items=gallery_items)

    except Exception as e:
        print("NASA FETCH ERROR:", e)
        return render_template("nasa_gallery.html", gallery_items=[])
    

@app.route('/space-news')
@login_required
def space_news():
    url = "https://api.spaceflightnewsapi.net/v4/articles/?limit=20"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
        else:
            data = {}

        articles = []

        for item in data.get("results", []):
            articles.append({
                "title": item.get("title", "No title"),
                "desc": item.get("summary", "No description"),
                "image": item.get("image_url", ""),
                "link": item.get("url", "#")
            })

    except Exception as e:
        print("Error fetching news:", e)
        articles = []

    return render_template("space_news.html", articles=articles)

# ==================== API ROUTES ====================

@app.route('/api/planet/<name>')
@login_required
def api_planet(name):
    planet = planet_manager.get_planet(name)
    if planet:
        planet['_id'] = str(planet['_id'])
        return jsonify(planet)
    return jsonify({'error': 'Planet not found'}), 404


@app.route('/api/mission/<name>')
@login_required
def api_mission(name):
    mission = mission_manager.get_mission(name)
    if mission:
        mission['_id'] = str(mission['_id'])
        return jsonify(mission)
    return jsonify({'error': 'Mission not found'}), 404


@app.route('/api/favorite/toggle', methods=['POST'])
@login_required
def toggle_favorite():
    data = request.get_json()
    item_type = data.get('type')
    item_name = data.get('name')
    
    if not item_type or not item_name:
        return jsonify({'success': False, 'error': 'Invalid data'}), 400
    
    user_id = session['user_id']
    
    if favorites_manager.is_favorited(user_id, item_type, item_name):
        favorites_manager.remove_favorite(user_id, item_type, item_name)
        action = 'removed'
    else:
        favorites_manager.add_favorite(user_id, item_type, item_name)
        action = 'added'
    
    activity_manager.log_activity(
        user_id,
        f'favorite_{action}',
        {'type': item_type, 'name': item_name}
    )
    
    return jsonify({'success': True, 'action': action})


@app.route('/api/favorites')
@login_required
def get_favorites():
    favorites = favorites_manager.get_user_favorites(session['user_id'])
    for fav in favorites:
        fav['_id'] = str(fav['_id'])
        fav['added_at'] = fav['added_at'].isoformat()
    return jsonify({'favorites': favorites})


@app.route('/api/stats')
@login_required
def get_stats():
    user = user_manager.find_by_id(session['user_id'])
    if user:
        return jsonify({
            'explorations': user.get('explorations', 0),
            'rank': user.get('rank', 'Cadet'),
            'login_count': user.get('login_count', 0),
            'member_since': user.get('created_at').isoformat() if user.get('created_at') else None
        })
    return jsonify({'error': 'User not found'}), 404


@app.route('/api/activities')
@login_required
def get_activities():
    activities = activity_manager.get_user_activities(session['user_id'], 20)
    for act in activities:
        act['_id'] = str(act['_id'])
        act['timestamp'] = act['timestamp'].isoformat()
    return jsonify({'activities': activities})


# ==================== PROFILE ROUTES ====================

@app.route('/profile')
@login_required
def profile():
    user = user_manager.find_by_id(session['user_id'])
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('logout'))
    
    user['_id'] = str(user['_id'])
    user.pop('password', None)
    
    favorites = favorites_manager.get_user_favorites(session['user_id'])
    activities = activity_manager.get_user_activities(session['user_id'], 10)
    
    return render_template('profile.html',
                         user=user,
                         favorites=favorites,
                         activities=activities)


@app.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    bio = request.form.get('bio', '').strip()
    avatar = request.form.get('avatar', '👨‍🚀')
    favorite_planet = request.form.get('favorite_planet', '')
    
    update_data = {
        'profile.bio': bio,
        'profile.avatar': avatar,
        'profile.favorite_planet': favorite_planet
    }
    
    if user_manager.update_user(session['user_id'], update_data):
        flash('✨ Profile updated successfully!', 'success')
    else:
        flash('Failed to update profile', 'error')
    
    return redirect(url_for('profile'))


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


# ==================== CONTEXT PROCESSORS ====================

@app.context_processor
def inject_user():
    """Make user info available in all templates"""
    return {
        'current_year': datetime.utcnow().year,
        'app_name': 'Stellar Gateway'
    }


if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 STELLAR GATEWAY SERVER STARTING...")
    print("="*50)
    print("📡 Server: http://localhost:5000")
    print("🗄️  Database: MongoDB")
    print("="*50 + "\n")
    
    app.run(
        debug=os.getenv('FLASK_DEBUG', 'True') == 'True',
        host='0.0.0.0',
        port=5000
    )