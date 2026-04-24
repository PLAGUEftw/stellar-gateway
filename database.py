"""
MongoDB Database Module for Stellar Gateway
Handles all database connections and operations
"""

from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, DuplicateKeyError, OperationFailure
from datetime import datetime
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    """MongoDB Database Handler Class"""
    
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._connect()
        return cls._instance
    
    def _connect(self):
    """Establish connection to MongoDB"""
    try:
        mongo_uri = os.getenv('MONGO_URI')

        print("Mongo URI:", mongo_uri)

        if not mongo_uri:
            raise Exception("MONGO_URI not found in environment variables")

        db_name = os.getenv('DATABASE_NAME', 'stellar_gateway')

        self._client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
            socketTimeoutMS=10000,
            maxPoolSize=50,
            retryWrites=True
        )

        # Test connection
        self._client.admin.command('ping')
        self._db = self._client[db_name]

        print("✅ MongoDB Connected Successfully")

    except Exception as e:
        print("❌ Mongo Error:", e)   # ✅ ADD HERE
        raise
            
            # Setup indexes
            self._setup_indexes()
            
            print(f"✅ MongoDB Connected Successfully → Database: {db_name}")
            return True
            
        except ConnectionFailure as e:
            print(f"❌ MongoDB Connection Failed: {e}")
            self._client = None
            self._db = None
            return False
        except Exception as e:
            print(f"❌ MongoDB Error: {e}")
            self._client = None
            self._db = None
            return False
    
    def _setup_indexes(self):
        """Create database indexes for performance"""
        try:
            # Users collection indexes
            self._db.users.create_index([("username", ASCENDING)], unique=True)
            self._db.users.create_index([("email", ASCENDING)], unique=True)
            
            # Activities collection indexes
            self._db.activities.create_index([("user_id", ASCENDING)])
            self._db.activities.create_index([("timestamp", DESCENDING)])
            
            # Favorites collection indexes
            self._db.favorites.create_index([("user_id", ASCENDING), ("item_type", ASCENDING)])
            
            # Planets collection indexes
            self._db.planets.create_index([("name", ASCENDING)], unique=True)
            
            # Missions collection indexes
            self._db.missions.create_index([("name", ASCENDING)])
            self._db.missions.create_index([("year", DESCENDING)])
            
            print("✅ Database indexes created successfully")
        except Exception as e:
            print(f"⚠️ Index setup warning: {e}")
    
    def is_connected(self):
        """Check if database is connected"""
        return self._db is not None
    
    def get_db(self):
        """Return database instance"""
        return self._db
    
    def get_collection(self, collection_name):
        """Return a specific collection"""
        if self._db is not None:
            return self._db[collection_name]
        return None
    
    def close(self):
        """Close database connection"""
        if self._client:
            self._client.close()
            print("🔌 MongoDB connection closed")


# ==================== USER OPERATIONS ====================

class UserManager:
    """Handle all user-related database operations"""
    
    def __init__(self):
        self.db = Database()
        self.collection = self.db.get_collection('users') if self.db.is_connected() else None
    
    def create_user(self, user_data):
        """Create a new user"""
        if self.collection is None:
            return {'success': False, 'error': 'Database not connected'}
        
        try:
            user_data['created_at'] = datetime.utcnow()
            user_data['last_login'] = None
            user_data['login_count'] = 0
            user_data['explorations'] = 0
            user_data['rank'] = 'Cadet'
            user_data['is_active'] = True
            user_data['profile'] = {
                'avatar': '👨‍🚀',
                'bio': '',
                'favorite_planet': None,
                'joined_missions': []
            }
            
            result = self.collection.insert_one(user_data)
            return {'success': True, 'user_id': str(result.inserted_id)}
            
        except DuplicateKeyError:
            return {'success': False, 'error': 'Username or email already exists'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def find_user(self, query):
        """Find a user by query"""
        if self.collection is None:
            return None
        try:
            return self.collection.find_one(query)
        except Exception as e:
            print(f"Error finding user: {e}")
            return None
    
    def find_by_username_or_email(self, identifier):
        """Find user by username or email"""
        if self.collection is None:
            return None
        try:
            return self.collection.find_one({
                '$or': [
                    {'username': identifier},
                    {'email': identifier.lower()}
                ]
            })
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def find_by_id(self, user_id):
        """Find user by ObjectId"""
        if self.collection is None:
            return None
        try:
            return self.collection.find_one({'_id': ObjectId(user_id)})
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def update_user(self, user_id, update_data):
        """Update user information"""
        if self.collection is None:
            return False
        try:
            update_data['updated_at'] = datetime.utcnow()
            result = self.collection.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    def update_last_login(self, user_id):
        """Update user's last login time"""
        if self.collection is None:
            return False
        try:
            self.collection.update_one(
                {'_id': ObjectId(user_id)},
                {
                    '$set': {'last_login': datetime.utcnow()},
                    '$inc': {'login_count': 1}
                }
            )
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def increment_exploration(self, user_id):
        """Increment user's exploration count"""
        if self.collection is None:
            return False
        try:
            result = self.collection.update_one(
                {'_id': ObjectId(user_id)},
                {'$inc': {'explorations': 1}}
            )
            # Update rank based on explorations
            user = self.find_by_id(user_id)
            if user:
                explorations = user.get('explorations', 0) + 1
                new_rank = self._calculate_rank(explorations)
                if new_rank != user.get('rank'):
                    self.update_user(user_id, {'rank': new_rank})
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def _calculate_rank(self, explorations):
        """Calculate user rank based on explorations"""
        if explorations >= 100:
            return 'Galactic Commander'
        elif explorations >= 50:
            return 'Star Captain'
        elif explorations >= 25:
            return 'Space Explorer'
        elif explorations >= 10:
            return 'Astronaut'
        elif explorations >= 5:
            return 'Pilot'
        else:
            return 'Cadet'
    
    def delete_user(self, user_id):
        """Delete a user account"""
        if self.collection is None:
            return False
        try:
            result = self.collection.delete_one({'_id': ObjectId(user_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def get_all_users(self, limit=100):
        """Get all users (admin function)"""
        if self.collection is None:
            return []
        try:
            return list(self.collection.find({}, {'password': 0}).limit(limit))
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def get_user_count(self):
        """Get total user count"""
        if self.collection is None:
            return 0
        try:
            return self.collection.count_documents({})
        except:
            return 0


# ==================== ACTIVITY OPERATIONS ====================

class ActivityManager:
    """Handle user activity logging"""
    
    def __init__(self):
        self.db = Database()
        self.collection = self.db.get_collection('activities') if self.db.is_connected() else None
    
    def log_activity(self, user_id, action, details=None):
        """Log user activity"""
        if self.collection is None:
            return False
        try:
            activity = {
                'user_id': str(user_id),
                'action': action,
                'details': details or {},
                'timestamp': datetime.utcnow(),
                'ip_address': details.get('ip') if details else None
            }
            self.collection.insert_one(activity)
            return True
        except Exception as e:
            print(f"Error logging activity: {e}")
            return False
    
    def get_user_activities(self, user_id, limit=20):
        """Get recent activities for a user"""
        if self.collection is None:
            return []
        try:
            return list(
                self.collection.find({'user_id': str(user_id)})
                .sort('timestamp', DESCENDING)
                .limit(limit)
            )
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def get_recent_activities(self, limit=50):
        """Get all recent activities"""
        if self.collection is None:
            return []
        try:
            return list(
                self.collection.find({})
                .sort('timestamp', DESCENDING)
                .limit(limit)
            )
        except Exception as e:
            print(f"Error: {e}")
            return []


# ==================== FAVORITES OPERATIONS ====================

class FavoritesManager:
    """Handle user favorites"""
    
    def __init__(self):
        self.db = Database()
        self.collection = self.db.get_collection('favorites') if self.db.is_connected() else None
    
    def add_favorite(self, user_id, item_type, item_name, item_data=None):
        """Add item to favorites"""
        if self.collection is None:
            return False
        try:
            existing = self.collection.find_one({
                'user_id': str(user_id),
                'item_type': item_type,
                'item_name': item_name
            })
            
            if existing:
                return False  # Already favorited
            
            favorite = {
                'user_id': str(user_id),
                'item_type': item_type,  # 'planet', 'mission', 'gallery'
                'item_name': item_name,
                'item_data': item_data or {},
                'added_at': datetime.utcnow()
            }
            self.collection.insert_one(favorite)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def remove_favorite(self, user_id, item_type, item_name):
        """Remove item from favorites"""
        if self.collection is None:
            return False
        try:
            result = self.collection.delete_one({
                'user_id': str(user_id),
                'item_type': item_type,
                'item_name': item_name
            })
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def get_user_favorites(self, user_id, item_type=None):
        """Get user's favorites"""
        if self.collection is None:
            return []
        try:
            query = {'user_id': str(user_id)}
            if item_type:
                query['item_type'] = item_type
            return list(self.collection.find(query).sort('added_at', DESCENDING))
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def is_favorited(self, user_id, item_type, item_name):
        """Check if item is favorited"""
        if self.collection is None:
            return False
        try:
            return self.collection.find_one({
                'user_id': str(user_id),
                'item_type': item_type,
                'item_name': item_name
            }) is not None
        except:
            return False


# ==================== PLANET OPERATIONS ====================

class PlanetManager:
    """Handle planet data operations"""
    
    def __init__(self):
        self.db = Database()
        self.collection = self.db.get_collection('planets') if self.db.is_connected() else None
    
    def get_all_planets(self):
        """Get all planets"""
        if self.collection is None:
            return []
        try:
            return list(self.collection.find({}))
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def get_planet(self, name):
        """Get specific planet"""
        if self.collection is None:
            return None
        try:
            return self.collection.find_one({'name': name})
        except:
            return None
    
    def add_planet(self, planet_data):
        """Add a planet"""
        if self.collection is None:
            return False
        try:
            self.collection.insert_one(planet_data)
            return True
        except DuplicateKeyError:
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def update_planet(self, name, update_data):
        """Update planet information"""
        if self.collection is None:
            return False
        try:
            result = self.collection.update_one(
                {'name': name},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error: {e}")
            return False


# ==================== MISSION OPERATIONS ====================

class MissionManager:
    """Handle mission data operations"""
    
    def __init__(self):
        self.db = Database()
        self.collection = self.db.get_collection('missions') if self.db.is_connected() else None
    
    def get_all_missions(self):
        """Get all missions"""
        if self.collection is None:
            return []
        try:
            return list(self.collection.find({}).sort('year', DESCENDING))
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def get_mission(self, name):
        """Get specific mission"""
        if self.collection is None:
            return None
        try:
            return self.collection.find_one({'name': name})
        except:
            return None
    
    def add_mission(self, mission_data):
        """Add a mission"""
        if self.collection is None:
            return False
        try:
            self.collection.insert_one(mission_data)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def get_missions_by_status(self, status):
        """Get missions filtered by status"""
        if self.collection is None:
            return []
        try:
            return list(self.collection.find({'status': status}).sort('year', DESCENDING))
        except:
            return []


# Initialize database on module import
db_instance = Database()