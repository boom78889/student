import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from database import db, init_db
from config import config

load_dotenv()

def create_app(config_name=None):
    """Application factory"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    
    # Register blueprints
    from routes import auth_routes, hotel_routes, billing_routes, menu_routes, reports_routes
    
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(hotel_routes.bp)
    app.register_blueprint(billing_routes.bp)
    app.register_blueprint(menu_routes.bp)
    app.register_blueprint(reports_routes.bp)
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return {'status': 'healthy', 'environment': config_name}, 200
    
    # Database initialization
    @app.route('/init-db', methods=['POST'])
    def initialize_database():
        """Initialize database (run migrations)"""
        try:
            init_db(app)
            return {'message': 'Database initialized successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 500
    
    # Database stats endpoint
    @app.route('/db-stats', methods=['GET'])
    def db_stats():
        """Get database statistics"""
        from database import get_db_stats
        try:
            stats = get_db_stats(app)
            return stats, 200
        except Exception as e:
            return {'error': str(e)}, 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        # Create tables
        db.create_all()
        print("✅ Database tables created!")
    
    # Run the app
    app.run(
        debug=os.getenv('FLASK_DEBUG', True),
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000))
    )
