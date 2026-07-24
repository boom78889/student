# Database Schema

## Tables

### Users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    hotel_id INTEGER REFERENCES hotels(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Hotels
```sql
CREATE TABLE hotels (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    phone_number VARCHAR(15),
    email VARCHAR(120),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    zipcode VARCHAR(10),
    country VARCHAR(100),
    logo_url VARCHAR(255),
    total_rooms INTEGER DEFAULT 0,
    check_in_time VARCHAR(10) DEFAULT '14:00',
    check_out_time VARCHAR(10) DEFAULT '11:00',
    currency VARCHAR(3) DEFAULT 'USD',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Menus
```sql
CREATE TABLE menus (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    price FLOAT NOT NULL,
    availability BOOLEAN DEFAULT TRUE,
    image_url VARCHAR(255),
    preparation_time INTEGER,
    is_vegetarian BOOLEAN DEFAULT FALSE,
    is_vegan BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Billings
```sql
CREATE TABLE billings (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    guest_name VARCHAR(150) NOT NULL,
    guest_email VARCHAR(120),
    guest_phone VARCHAR(15),
    check_in_date TIMESTAMP,
    check_out_date TIMESTAMP,
    room_number VARCHAR(20),
    total_amount FLOAT DEFAULT 0,
    paid_amount FLOAT DEFAULT 0,
    balance FLOAT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Invoices
```sql
CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,
    billing_id INTEGER NOT NULL REFERENCES billings(id) ON DELETE CASCADE,
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    item_description VARCHAR(255) NOT NULL,
    quantity INTEGER DEFAULT 1,
    unit_price FLOAT NOT NULL,
    total_price FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### OTPs
```sql
CREATE TABLE otps (
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(15) NOT NULL,
    otp_code VARCHAR(6) NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    attempts INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP + INTERVAL '10 minutes'
);
```

## Relationships

```
Hotel (1) ──── (N) User
Hotel (1) ──── (N) Menu
Hotel (1) ──── (N) Billing
Billing (1) ──── (N) Invoice
```
