"""Database migrations manager"""
from datetime import datetime
from pathlib import Path
from src.models.database import get_db


MIGRATIONS_DIR = Path("migrations")
MIGRATIONS_DIR.mkdir(exist_ok=True)


class Migration:
    """Base migration class"""
    
    version: str
    description: str
    
    def up(self):
        """Run migration forward"""
        raise NotImplementedError
    
    def down(self):
        """Run migration backward"""
        raise NotImplementedError


class MigrationManager:
    """Manage database migrations"""
    
    def __init__(self):
        self.db = get_db()
    
    def apply_migrations(self):
        """Apply all pending migrations"""
        if not self.db.is_connected():
            print("[WARNING] MongoDB not connected. Skipping migrations.")
            return
        
        try:
            # Create migrations collection if not exists
            migrations = self.db.db['_migrations']
            
            # Migration 001: Create indexes
            if not migrations.find_one({'version': '001'}):
                print("[MIGRATION] Applying 001: Create indexes...")
                
                self.db.db['recommendations'].create_index('user_id')
                self.db.db['recommendations'].create_index('timestamp')
                self.db.db['preferences'].create_index('user_id')
                
                migrations.insert_one({
                    'version': '001',
                    'description': 'Create indexes',
                    'applied_at': datetime.utcnow()
                })
                print("[OK] Migration 001 applied")
            
            # Migration 002: Add metadata fields
            if not migrations.find_one({'version': '002'}):
                print("[MIGRATION] Applying 002: Add metadata fields...")
                
                # Update existing recommendations
                self.db.db['recommendations'].update_many(
                    {'metadata': {'$exists': False}},
                    {'$set': {'metadata': {'created': datetime.utcnow()}}}
                )
                
                migrations.insert_one({
                    'version': '002',
                    'description': 'Add metadata fields',
                    'applied_at': datetime.utcnow()
                })
                print("[OK] Migration 002 applied")
            
            print("[OK] All migrations applied successfully")
            
        except Exception as e:
            print(f"[ERROR] Migration failed: {e}")
    
    def get_migration_history(self):
        """Get migration history"""
        if not self.db.is_connected():
            return []
        
        try:
            migrations = self.db.db['_migrations']
            return list(migrations.find().sort('applied_at', -1))
        except:
            return []


# Global manager
migrations_manager = MigrationManager()


def init_db():
    """Initialize database with migrations"""
    print("[DB] Initializing database...")
    migrations_manager.apply_migrations()
    print("[DB] Database initialized")
