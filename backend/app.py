from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://user:password@localhost:5432/hotel_management'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import blueprints
from routes import auth_routes, hotel_routes, billing_routes, menu_routes, reports_routes

app.register_blueprint(auth_routes.bp)
app.register_blueprint(hotel_routes.bp)
app.register_blueprint(billing_routes.bp)
app.register_blueprint(menu_routes.bp)
app.register_blueprint(reports_routes.bp)

@app.route('/health', methods=['GET'])
def health_check():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
