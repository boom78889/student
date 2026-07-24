# Setup Guide

## Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Android Studio (for Android development)
- Git
- Node.js 16+ (optional, for frontend build tools)

## Backend Setup

### 1. Clone the Repository
```bash
git clone https://github.com/boom78889/Student.git
cd Student/backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Database

#### Create PostgreSQL Database
```bash
psql -U postgres
CREATE DATABASE hotel_management;
\q
```

#### Update .env file
```bash
cp .env.example .env
```

Edit `.env` with your database credentials:
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/hotel_management
SECRET_KEY=your_secret_key_here
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

### 5. Run Migrations
```bash
python app.py
```

This will create all tables automatically.

### 6. Start Backend Server
```bash
python app.py
```

Server will run on `http://localhost:5000`

---

## Android Setup

### 1. Open Android Project
```bash
cd android
./gradlew build
```

### 2. Configure API Base URL

Edit `app/src/main/java/com/hotelmanagement/app/network/ApiClient.kt`:

```kotlin
const val BASE_URL = "http://your_backend_url/api/"
```

### 3. Run Application

- Open Android Studio
- Select "Run" → "Run 'app'"
- Choose emulator or connected device

---

## Configuration

### Environment Variables

Create `.env` file in backend root:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/hotel_management

# JWT
SECRET_KEY=your_secret_key_here
JWT_EXPIRATION_HOURS=24

# Twilio SMS
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Environment
ENVIRONMENT=development
```

### Database Initialization

The app automatically creates tables on first run.

---

## Testing

### Backend Tests
```bash
pytest tests/
```

### Android Tests
```bash
./gradlew test
```

---

## Deployment

### Backend Deployment (DigitalOcean/AWS)

1. Set up Ubuntu server
2. Install Python, PostgreSQL, Nginx
3. Clone repository
4. Configure systemd service
5. Deploy with Gunicorn

### Android Deployment (Play Store)

1. Generate signed APK
2. Create Google Play Developer account
3. Upload APK to Play Store
4. Submit for review

---

## Troubleshooting

### Database Connection Error
```
Check PostgreSQL is running:
sudo systemctl status postgresql
```

### Port Already in Use
```bash
lsof -i :5000
kill -9 <PID>
```

### OTP Not Sending
```
Check Twilio credentials in .env
Ensure phone number format is correct (+91...)
```
