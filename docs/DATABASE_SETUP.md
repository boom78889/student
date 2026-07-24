# Database Setup Guide

## Prerequisites

- PostgreSQL 12 or higher
- Python 3.9+
- pip (Python package manager)

## Step 1: Install PostgreSQL

### On Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### On macOS (using Homebrew):
```bash
brew install postgresql
brew services start postgresql
```

### On Windows:
Download from: https://www.postgresql.org/download/windows/

## Step 2: Create Database User

```bash
sudo -u postgres psql
```

Then in PostgreSQL:
```sql
CREATE USER hotelapp WITH PASSWORD 'your_secure_password';
ALTER ROLE hotelapp SET client_encoding TO 'utf8';
ALTER ROLE hotelapp SET default_transaction_isolation TO 'read committed';
ALTER ROLE hotelapp SET default_transaction_deferrable TO on;
ALTER ROLE hotelapp SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE hotel_management TO hotelapp;
\q
```

## Step 3: Create Database

```bash
sudo -u postgres createdb hotel_management
sudo -u postgres psql -d hotel_management -c "GRANT ALL PRIVILEGES ON SCHEMA public TO hotelapp;"
```

## Step 4: Configure Environment

Copy the example env file:
```bash
cd backend
cp .env.example .env
```

Edit `.env` with your database credentials:
```
DATABASE_URL=postgresql://hotelapp:your_secure_password@localhost:5432/hotel_management
SECRET_KEY=your_secret_key_here_change_this_in_production
JWT_EXPIRATION_HOURS=24
FLASK_ENV=development
FLASK_DEBUG=True
```

## Step 5: Install Python Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

## Step 6: Initialize Database

### Option 1: Using Management Script (Recommended)

```bash
# Initialize (create tables)
python manage.py init

# Seed database with sample data
python manage.py seed

# View database statistics
python manage.py stats
```

### Option 2: Direct Flask Command

```bash
python app.py
```

This will automatically create all tables on first run.

## Step 7: Verify Database Setup

### Check tables were created:
```bash
psql -U hotelapp -d hotel_management -c "\\dt"
```

You should see these tables:
- users
- hotels
- menus
- billings
- invoices
- otps

### Check table structure:
```bash
psql -U hotelapp -d hotel_management -c "\\d users;"
```

## Management Commands

### Initialize Database
```bash
python manage.py init
```
Creates all tables in the database.

### Seed Database
```bash
python manage.py seed
```
Adds sample data:
- 1 test user (username: hotelowner, password: password123)
- 1 sample hotel (Grand Plaza Hotel)
- 6 menu items

### Reset Database
```bash
python manage.py reset
```
Drops all tables and recreates them (removes all data!).

### Drop Database
```bash
python manage.py drop
```
Removes all tables (WARNING: Data loss!).

### View Statistics
```bash
python manage.py stats
```
Shows count of records in each table.

### Migrate
```bash
python manage.py migrate
```
Creates tables if they don't exist.

## Backup & Restore

### Backup Database
```bash
pg_dump -U hotelapp -d hotel_management -f hotel_management_backup.sql
```

### Restore Database
```bash
psql -U hotelapp -d hotel_management < hotel_management_backup.sql
```

## Database Schema Overview

### Users Table
- Stores user accounts
- Fields: id, username, email, phone_number, password_hash, is_verified, hotel_id, created_at, updated_at

### Hotels Table
- Stores hotel information
- Fields: id, name, description, address, city, state, country, total_rooms, check_in_time, check_out_time, currency, created_at, updated_at

### Menus Table
- Stores menu items
- Fields: id, hotel_id, name, description, category, price, availability, preparation_time, is_vegetarian, is_vegan, created_at, updated_at

### Billings Table
- Stores guest billing records
- Fields: id, hotel_id, guest_name, guest_email, guest_phone, check_in_date, check_out_date, room_number, total_amount, paid_amount, balance, status, created_at, updated_at

### Invoices Table
- Stores individual invoice items
- Fields: id, billing_id, invoice_number, item_description, quantity, unit_price, total_price, created_at

### OTPs Table
- Stores OTP records for verification
- Fields: id, phone_number, otp_code, is_verified, attempts, created_at, expires_at

## Troubleshooting

### Connection Refused
```
Error: could not connect to server: Connection refused
```
**Solution:** Make sure PostgreSQL is running:
```bash
sudo systemctl start postgresql
```

### Database Does Not Exist
```
Error: database "hotel_management" does not exist
```
**Solution:** Create the database:
```bash
sudo -u postgres createdb hotel_management
```

### Permission Denied
```
Error: permission denied for schema public
```
**Solution:** Grant privileges:
```bash
sudo -u postgres psql -d hotel_management -c "GRANT ALL PRIVILEGES ON SCHEMA public TO hotelapp;"
```

### Port Already in Use (5432)
```bash
lsof -i :5432
kill -9 <PID>
```

### Wrong Password
```bash
# Reset user password
sudo -u postgres psql
ALTER USER hotelapp WITH PASSWORD 'new_password';
\\q
```

## Testing the Setup

### 1. Start Flask Server
```bash
cd backend
python app.py
```

### 2. Test Health Endpoint
```bash
curl http://localhost:5000/health
```

Should return:
```json
{"status": "healthy", "environment": "development"}
```

### 3. Test Database Connection
```bash
curl http://localhost:5000/db-stats
```

Should return table statistics:
```json
{
  "users": 1,
  "hotels": 1,
  "menus": 6,
  "billings": 0,
  "invoices": 0,
  "otps": 0
}
```

### 4. Test Registration API
```bash
curl -X POST http://localhost:5000/api/auth/register \\
  -H "Content-Type: application/json" \\
  -d '{
    "username": "testuser",
    "password": "testpass123",
    "phone_number": "+919999999999",
    "email": "test@example.com"
  }'
```

## Performance Tips

1. **Add Indexes**: Indexes are already added to frequently queried columns
2. **Connection Pooling**: Consider using pgBouncer for production
3. **Backup Regularly**: Set up automated PostgreSQL backups
4. **Monitor Queries**: Use `pg_stat_statements` to find slow queries

## Next Steps

1. ✅ Database is set up and running
2. 🔌 Test API endpoints
3. 📱 Build Android UI
4. 🚀 Deploy to production
