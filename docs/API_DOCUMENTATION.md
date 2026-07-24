# Hotel Management App - API Documentation

## Base URL
```
https://api.hotelmanagement.app/api
```

## Authentication
All authenticated endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

---

## Auth Endpoints

### 1. Register User
**POST** `/auth/register`

**Request Body:**
```json
{
  "username": "hotelowner",
  "password": "secure_password",
  "phone_number": "+91987654321",
  "email": "owner@hotel.com"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "hotelowner",
    "phone_number": "+91987654321",
    "is_verified": false,
    "created_at": "2024-01-15T10:30:00"
  }
}
```

### 2. Send OTP
**POST** `/auth/send-otp`

**Request Body:**
```json
{
  "phone_number": "+91987654321"
}
```

**Response:**
```json
{
  "message": "OTP sent successfully",
  "otp_id": 1
}
```

### 3. Verify OTP
**POST** `/auth/verify-otp`

**Request Body:**
```json
{
  "phone_number": "+91987654321",
  "otp_code": "123456"
}
```

**Response:**
```json
{
  "message": "OTP verified successfully",
  "phone_number": "+91987654321"
}
```

### 4. Login
**POST** `/auth/login`

**Request Body:**
```json
{
  "username": "hotelowner",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "hotelowner",
    "phone_number": "+91987654321",
    "is_verified": true,
    "created_at": "2024-01-15T10:30:00"
  }
}
```

---

## Hotel Endpoints

### 1. Create Hotel
**POST** `/hotel/create`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "name": "Grand Plaza Hotel",
  "description": "5-star luxury hotel",
  "phone_number": "+91-11-12345678",
  "email": "contact@grandplaza.com",
  "address": "123 Main Street",
  "city": "New Delhi",
  "state": "Delhi",
  "zipcode": "110001",
  "country": "India",
  "total_rooms": 100,
  "check_in_time": "14:00",
  "check_out_time": "11:00",
  "currency": "INR"
}
```

**Response:**
```json
{
  "message": "Hotel created successfully",
  "hotel": {
    "id": 1,
    "name": "Grand Plaza Hotel",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

### 2. Get Hotel Details
**GET** `/hotel/<hotel_id>`

**Response:**
```json
{
  "id": 1,
  "name": "Grand Plaza Hotel",
  "description": "5-star luxury hotel",
  "city": "New Delhi",
  "total_rooms": 100,
  "created_at": "2024-01-15T10:30:00"
}
```

### 3. Update Hotel
**PUT** `/hotel/<hotel_id>`

**Headers:** `Authorization: Bearer <token>`

**Request Body:** (any fields you want to update)
```json
{
  "name": "Grand Plaza Hotel - Updated",
  "total_rooms": 120
}
```

---

## Menu Endpoints

### 1. Create Menu Item
**POST** `/menu/create`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "name": "Butter Chicken",
  "description": "Creamy tomato-based curry",
  "category": "Main Course",
  "price": 450.00,
  "availability": true,
  "preparation_time": 30,
  "is_vegetarian": false,
  "is_vegan": false
}
```

### 2. List Menu Items
**GET** `/menu/list`

**Response:**
```json
{
  "menus": [
    {
      "id": 1,
      "name": "Butter Chicken",
      "price": 450.00,
      "category": "Main Course",
      "availability": true
    }
  ]
}
```

### 3. Update Menu Item
**PUT** `/menu/<menu_id>`

### 4. Delete Menu Item
**DELETE** `/menu/<menu_id>`

---

## Billing Endpoints

### 1. Create Billing Record
**POST** `/billing/create`

**Request Body:**
```json
{
  "guest_name": "John Doe",
  "guest_email": "john@example.com",
  "guest_phone": "+91-98765-43210",
  "check_in_date": "2024-01-20T14:00:00",
  "check_out_date": "2024-01-25T11:00:00",
  "room_number": "301",
  "total_amount": 25000.00
}
```

### 2. List Billing Records
**GET** `/billing/list`

### 3. Add Invoice
**POST** `/billing/<billing_id>/add-invoice`

**Request Body:**
```json
{
  "invoice_number": "INV-001",
  "item_description": "Room Charges - 5 nights",
  "quantity": 1,
  "unit_price": 5000.00
}
```

### 4. Record Payment
**POST** `/billing/<billing_id>/payment`

**Request Body:**
```json
{
  "amount": 10000.00
}
```

---

## Reports Endpoints

### 1. Revenue Report
**GET** `/reports/revenue?days=30`

**Response:**
```json
{
  "total_revenue": 150000.00,
  "total_pending": 25000.00,
  "completed_bookings": 15,
  "period_days": 30,
  "start_date": "2024-01-15T10:30:00",
  "end_date": "2024-02-15T10:30:00"
}
```

### 2. Menu Report
**GET** `/reports/menu-popular`

### 3. Occupancy Report
**GET** `/reports/occupancy`

---

## Error Responses

All errors follow this format:
```json
{
  "error": "Error message here"
}
```

### Common Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict
- `500` - Server Error
