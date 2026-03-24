"""MongoDB database connection and operations"""
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class MongoDB:
    """MongoDB database manager for storing recommendations and preferences"""
    
    def __init__(self):
        self.uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        self.db_name = os.getenv("MONGODB_DB_NAME", "healthy_food_ai")
        self.client = None
        self.db = None
        self._connect()
    
    def _connect(self):
        """Connect to MongoDB"""
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            print(f"[OK] Connected to MongoDB: {self.db_name}")
        except ConnectionFailure:
            print(f"[WARNING] Could not connect to MongoDB at {self.uri}")
            print("MongoDB features will be offline. Running in demo mode.")
            self.client = None
            self.db = None
    
    def is_connected(self):
        """Check if MongoDB is connected"""
        return self.db is not None
    
    # Recommendations collection
    def save_recommendation(self, dietary_needs: str, calories: int, recommendation: str, user_id: str = "default"):
        """Save recommendation to database"""
        if not self.is_connected():
            return False
        
        try:
            collection = self.db["recommendations"]
            collection.insert_one({
                "user_id": user_id,
                "dietary_needs": dietary_needs,
                "calories": calories,
                "recommendation": recommendation,
                "timestamp": __import__("datetime").datetime.utcnow()
            })
            return True
        except Exception as e:
            print(f"[ERROR] Failed to save recommendation: {e}")
            return False
    
    def get_recommendations(self, user_id: str = "default", limit: int = 10):
        """Get user recommendations from database"""
        if not self.is_connected():
            return []
        
        try:
            collection = self.db["recommendations"]
            results = list(collection.find({"user_id": user_id}).sort("_id", -1).limit(limit))
            return results
        except Exception as e:
            print(f"[ERROR] Failed to retrieve recommendations: {e}")
            return []
    
    # Preferences collection
    def save_preferences(self, user_id: str, dietary_needs: list, target_calories: int, allergies: list = None):
        """Save user preferences to database"""
        if not self.is_connected():
            return False
        
        try:
            collection = self.db["preferences"]
            collection.replace_one(
                {"user_id": user_id},
                {
                    "user_id": user_id,
                    "dietary_needs": dietary_needs,
                    "target_calories": target_calories,
                    "allergies": allergies or [],
                    "updated_at": __import__("datetime").datetime.utcnow()
                },
                upsert=True
            )
            return True
        except Exception as e:
            print(f"[ERROR] Failed to save preferences: {e}")
            return False
    
    def get_preferences(self, user_id: str = "default"):
        """Get user preferences from database"""
        if not self.is_connected():
            return None
        
        try:
            collection = self.db["preferences"]
            return collection.find_one({"user_id": user_id})
        except Exception as e:
            print(f"[ERROR] Failed to retrieve preferences: {e}")
            return None
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()


# Global MongoDB instance
db = None


def get_db():
    """Get or create MongoDB instance"""
    global db
    if db is None:
        db = MongoDB()
    return db
