"""Database initialization and migration utilities"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

def init_db(app):
    """Initialize database"""
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            return True
        except Exception as e:
            print(f"❌ Error creating database tables: {str(e)}")
            return False

def drop_db(app):
    """Drop all tables (USE WITH CAUTION)"""
    with app.app_context():
        try:
            db.drop_all()
            print("✅ All database tables dropped!")
            return True
        except Exception as e:
            print(f"❌ Error dropping tables: {str(e)}")
            return False

def seed_db(app):
    """Seed database with sample data"""
    with app.app_context():
        from models.user import User
        from models.hotel import Hotel
        from models.menu import Menu
        from models.billing import Billing
        
        try:
            # Check if data already exists
            existing_user = User.query.first()
            if existing_user:
                print("⚠️  Database already contains data. Skipping seed.")
                return False
            
            # Create sample user
            user = User(
                username='hotelowner',
                phone_number='+919876543210',
                email='owner@hotel.com'
            )
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            print("✅ Sample user created: hotelowner")
            
            # Create sample hotel
            hotel = Hotel(
                name='Grand Plaza Hotel',
                description='5-star luxury hotel with world-class amenities',
                phone_number='+91-11-12345678',
                email='contact@grandplaza.com',
                address='123 Main Street',
                city='New Delhi',
                state='Delhi',
                zipcode='110001',
                country='India',
                total_rooms=100,
                check_in_time='14:00',
                check_out_time='11:00',
                currency='INR'
            )
            db.session.add(hotel)
            db.session.commit()
            print(f"✅ Sample hotel created: {hotel.name}")
            
            # Link hotel to user
            user.hotel_id = hotel.id
            user.is_verified = True
            db.session.commit()
            
            # Create sample menu items
            menu_items = [
                Menu(
                    hotel_id=hotel.id,
                    name='Butter Chicken',
                    description='Creamy tomato-based curry with tender chicken pieces',
                    category='Main Course',
                    price=450.00,
                    availability=True,
                    preparation_time=30,
                    is_vegetarian=False
                ),
                Menu(
                    hotel_id=hotel.id,
                    name='Paneer Tikka',
                    description='Marinated cottage cheese grilled to perfection',
                    category='Appetizer',
                    price=300.00,
                    availability=True,
                    preparation_time=25,
                    is_vegetarian=True,
                    is_vegan=False
                ),
                Menu(
                    hotel_id=hotel.id,
                    name='Vegetable Biryani',
                    description='Fragrant rice cooked with fresh vegetables',
                    category='Main Course',
                    price=350.00,
                    availability=True,
                    preparation_time=35,
                    is_vegetarian=True,
                    is_vegan=True
                ),
                Menu(
                    hotel_id=hotel.id,
                    name='Tandoori Chicken',
                    description='Succulent chicken marinated in spices and yogurt',
                    category='Main Course',
                    price=500.00,
                    availability=True,
                    preparation_time=40,
                    is_vegetarian=False
                ),
                Menu(
                    hotel_id=hotel.id,
                    name='Garlic Naan',
                    description='Traditional Indian bread with garlic and butter',
                    category='Bread',
                    price=80.00,
                    availability=True,
                    preparation_time=10,
                    is_vegetarian=True
                ),
                Menu(
                    hotel_id=hotel.id,
                    name='Mango Lassi',
                    description='Refreshing yogurt drink with fresh mango',
                    category='Beverage',
                    price=150.00,
                    availability=True,
                    preparation_time=5,
                    is_vegetarian=True,
                    is_vegan=False
                )
            ]
            
            for menu_item in menu_items:
                db.session.add(menu_item)
            db.session.commit()
            print(f"✅ {len(menu_items)} sample menu items created")
            
            print("\n🎉 Database seeded successfully!")
            print("\n📝 Sample Login Credentials:")
            print("   Username: hotelowner")
            print("   Password: password123")
            print("   Phone: +919876543210")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error seeding database: {str(e)}")
            return False

def get_db_stats(app):
    """Get database statistics"""
    with app.app_context():
        from models.user import User
        from models.hotel import Hotel
        from models.menu import Menu
        from models.billing import Billing, Invoice
        from models.otp import OTP
        
        stats = {
            'users': User.query.count(),
            'hotels': Hotel.query.count(),
            'menus': Menu.query.count(),
            'billings': Billing.query.count(),
            'invoices': Invoice.query.count(),
            'otps': OTP.query.count()
        }
        return stats
