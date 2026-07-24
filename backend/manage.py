#!/usr/bin/env python
"""Management script for database operations"""

import os
import sys
from app import create_app
from database import db, init_db, drop_db, seed_db, get_db_stats

def init_command():
    """Initialize the database"""
    app = create_app()
    print("🔄 Initializing database...")
    if init_db(app):
        print("✅ Database initialized successfully!")
    else:
        print("❌ Failed to initialize database")
        sys.exit(1)

def drop_command():
    """Drop all tables (WARNING: Data will be lost!)"""
    app = create_app()
    confirm = input("⚠️  WARNING: This will delete all data! Are you sure? (yes/no): ")
    if confirm.lower() == 'yes':
        if drop_db(app):
            print("✅ Database dropped successfully!")
        else:
            print("❌ Failed to drop database")
            sys.exit(1)
    else:
        print("❌ Operation cancelled")

def seed_command():
    """Seed database with sample data"""
    app = create_app()
    print("🌱 Seeding database with sample data...")
    if seed_db(app):
        print("✅ Database seeded successfully!")
    else:
        print("❌ Failed to seed database")
        sys.exit(1)

def reset_command():
    """Reset database (drop and recreate)"""
    app = create_app()
    confirm = input("⚠️  This will reset the entire database! Are you sure? (yes/no): ")
    if confirm.lower() == 'yes':
        print("🔄 Dropping database...")
        drop_db(app)
        print("🔄 Recreating database...")
        if init_db(app):
            print("✅ Database reset successfully!")
        else:
            print("❌ Failed to reset database")
            sys.exit(1)
    else:
        print("❌ Operation cancelled")

def stats_command():
    """Show database statistics"""
    app = create_app()
    stats = get_db_stats(app)
    print("\n📊 Database Statistics:")
    print("="*40)
    for key, value in stats.items():
        print(f"{key.capitalize():<15}: {value}")
    print("="*40)

def migrate_command():
    """Create tables if they don't exist"""
    app = create_app()
    with app.app_context():
        db.create_all()
        print("✅ Migration completed!")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python manage.py <command>")
        print("\nAvailable commands:")
        print("  init    - Initialize database (create tables)")
        print("  drop    - Drop all tables")
        print("  seed    - Seed database with sample data")
        print("  reset   - Reset database (drop and recreate)")
        print("  stats   - Show database statistics")
        print("  migrate - Create tables if they don't exist")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'init':
        init_command()
    elif command == 'drop':
        drop_command()
    elif command == 'seed':
        seed_command()
    elif command == 'reset':
        reset_command()
    elif command == 'stats':
        stats_command()
    elif command == 'migrate':
        migrate_command()
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)
