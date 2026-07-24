# Complete API Documentation

## Overview

The Hotel Management App API is a RESTful API built with Flask. All endpoints require JWT authentication (except registration and OTP endpoints).

## Base URL

```
http://localhost:5000/api
```

## Authentication

All protected endpoints require a JWT token in the `Authorization` header:

```
Authorization: Bearer <your_jwt_token>
```

## Response Format

All responses are in JSON format:

```json
{
  "message": "Success message",
  "data": {}
}
```

Errors:

```json
{
  "error": "Error message"
}
```

## Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict
- `500` - Server Error

---

# Authentication Endpoints

## 1. Register User

**Endpoint:** `POST /auth/register`

**Description:** Register a new hotel owner account

**Request Body:**
```json
{
  "username": "hotelowner",
  "password": "SecurePass@123",
  "phone_number": "+919876543210",
  "email": "owner@hotel.com"
}
```

**Response:** `201 Created`
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "hotelowner",
    "email": "owner@hotel.com",
    "phone_number": "+919876543210",
    "is_verified": false,
    "created_at": "2024-01-15T10:30:00"
  }
}
```

**Error:** `409 Conflict`
```json
{
  "error": "Username already exists"
}
```

---

## 2. Send OTP

**Endpoint:** `POST /auth/send-otp`

**Description:** Send OTP to phone number for verification

**Request Body:**
```json
{
  "phone_number": "+919876543210"
}
```

**Response:** `200 OK`
```json
{
  "message": "OTP sent successfully",
  "otp_id": 1
}
```

**Note:** In development, OTP is logged to console. Check server logs for the OTP code.

---

## 3. Verify OTP

**Endpoint:** `POST /auth/verify-otp`

**Description:** Verify OTP sent to phone number

**Request Body:**
```json
{
  "phone_number": "+919876543210",
  "otp_code": "123456"
}
```

**Response:** `200 OK`
```json
{
  "message": "OTP verified successfully",
  "phone_number": "+919876543210"
}
```

**Error:** `400 Bad Request`
```json
{
  "error": "Invalid OTP"
}
```

---

## 4. Login

**Endpoint:** `POST /auth/login`

**Description:** Login user and get JWT token

**Request Body:**
```json
{
  "username": "hotelowner",
  "password": "SecurePass@123"
}
```

**Response:** `200 OK`
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImhvdGVsb3duZXIiLCJleHAiOjE2NzA3NzEwMDB9.xyz",
  "user": {
    "id": 1,
    "username": "hotelowner",
    "email": "owner@hotel.com",
    "phone_number": "+919876543210",
    "is_verified": true,
    "created_at": "2024-01-15T10:30:00"
  }
}
```

---

# Hotel Endpoints

## 1. Create Hotel

**Endpoint:** `POST /hotel/create`

**Authentication:** Required

**Description:** Create a new hotel profile

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

**Response:** `201 Created`
```json
{
  "message": "Hotel created successfully",
  "hotel": {
    "id": 1,
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
    "currency": "INR",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

---

## 2. Get Hotel Details

**Endpoint:** `GET /hotel/{hotel_id}`

**Authentication:** Required

**Description:** Get hotel information by ID

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Grand Plaza Hotel",
  "description": "5-star luxury hotel",
  "city": "New Delhi",
  "total_rooms": 100,
  "currency": "INR",
  "created_at": "2024-01-15T10:30:00"
}
```

---

## 3. Update Hotel

**Endpoint:** `PUT /hotel/{hotel_id}`

**Authentication:** Required

**Description:** Update hotel information (partial update)

**Request Body:**
```json
{
  "name": "Grand Plaza Hotel - Updated",
  "total_rooms": 120,
  "description": "Updated 5-star luxury hotel"
}
```

**Response:** `200 OK`
```json
{
  "message": "Hotel updated successfully",
  "hotel": {}
}
```

---

# Menu Endpoints

## 1. Create Menu Item

**Endpoint:** `POST /menu/create`

**Authentication:** Required

**Description:** Add a new menu item to the hotel

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

**Response:** `201 Created`
```json
{
  "message": "Menu item created successfully",
  "menu": {
    "id": 1,
    "hotel_id": 1,
    "name": "Butter Chicken",
    "description": "Creamy tomato-based curry",
    "category": "Main Course",
    "price": 450.00,
    "availability": true,
    "preparation_time": 30,
    "is_vegetarian": false,
    "is_vegan": false,
    "created_at": "2024-01-15T10:30:00"
  }
}
```

---

## 2. List Menu Items

**Endpoint:** `GET /menu/list`

**Authentication:** Required

**Description:** Get all menu items for the hotel

**Response:** `200 OK`
```json
{
  "menus": [
    {
      "id": 1,
      "name": "Butter Chicken",
      "price": 450.00,
      "category": "Main Course",
      "availability": true,
      "preparation_time": 30
    },
    {
      "id": 2,
      "name": "Paneer Tikka",
      "price": 300.00,
      "category": "Appetizer",
      "availability": true,
      "preparation_time": 25
    }
  ]
}
```

---

## 3. Update Menu Item

**Endpoint:** `PUT /menu/{menu_id}`

**Authentication:** Required

**Description:** Update a menu item

**Request Body:**
```json
{
  "price": 500.00,
  "availability": false
}
```

**Response:** `200 OK`
```json
{
  "message": "Menu item updated successfully",
  "menu": {}
}
```

---

## 4. Delete Menu Item

**Endpoint:** `DELETE /menu/{menu_id}`

**Authentication:** Required

**Description:** Delete a menu item

**Response:** `200 OK`
```json
{
  "message": "Menu item deleted successfully"
}
```

---

# Billing Endpoints

## 1. Create Billing Record

**Endpoint:** `POST /billing/create`

**Authentication:** Required

**Description:** Create a new billing record for a guest

**Request Body:**
```json
{
  "guest_name": "John Doe",
  "guest_email": "john@example.com",
  "guest_phone": "+91-9999999999",
  "check_in_date": "2024-01-20T14:00:00",
  "check_out_date": "2024-01-25T11:00:00",
  "room_number": "301",
  "total_amount": 25000.00
}
```

**Response:** `201 Created`
```json
{
  "message": "Billing record created successfully",
  "billing": {
    "id": 1,
    "guest_name": "John Doe",
    "guest_phone": "+91-9999999999",
    "room_number": "301",
    "total_amount": 25000.00,
    "paid_amount": 0.00,
    "balance": 25000.00,
    "status": "pending",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

---

## 2. List Billing Records

**Endpoint:** `GET /billing/list`

**Authentication:** Required

**Description:** Get all billing records for the hotel

**Response:** `200 OK`
```json
{
  "billings": [
    {
      "id": 1,
      "guest_name": "John Doe",
      "room_number": "301",
      "total_amount": 25000.00,
      "paid_amount": 0.00,
      "balance": 25000.00,
      "status": "pending"
    }
  ]
}
```

---

## 3. Add Invoice to Billing

**Endpoint:** `POST /billing/{billing_id}/add-invoice`

**Authentication:** Required

**Description:** Add invoice item to a billing record

**Request Body:**
```json
{
  "invoice_number": "INV-001",
  "item_description": "Room Charges - 5 nights",
  "quantity": 5,
  "unit_price": 5000.00
}
```

**Response:** `201 Created`
```json
{
  "message": "Invoice added successfully",
  "invoice": {
    "id": 1,
    "invoice_number": "INV-001",
    "item_description": "Room Charges - 5 nights",
    "quantity": 5,
    "unit_price": 5000.00,
    "total_price": 25000.00,
    "created_at": "2024-01-15T10:30:00"
  }
}
```

---

## 4. Record Payment

**Endpoint:** `POST /billing/{billing_id}/payment`

**Authentication:** Required

**Description:** Record a payment for a billing record

**Request Body:**
```json
{
  "amount": 10000.00
}
```

**Response:** `200 OK`
```json
{
  "message": "Payment recorded successfully",
  "billing": {
    "id": 1,
    "guest_name": "John Doe",
    "total_amount": 25000.00,
    "paid_amount": 10000.00,
    "balance": 15000.00,
    "status": "partial"
  }
}
```

---

# Reports Endpoints

## 1. Revenue Report

**Endpoint:** `GET /reports/revenue?days=30`

**Authentication:** Required

**Query Parameters:**
- `days` (optional): Number of days to look back (default: 30)

**Description:** Get revenue statistics for the hotel

**Response:** `200 OK`
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

---

## 2. Menu Report

**Endpoint:** `GET /reports/menu-popular`

**Authentication:** Required

**Description:** Get menu items analysis

**Response:** `200 OK`
```json
{
  "total_items": 12,
  "items": [
    {
      "name": "Butter Chicken",
      "price": 450.00,
      "category": "Main Course",
      "availability": true
    }
  ]
}
```

---

## 3. Occupancy Report

**Endpoint:** `GET /reports/occupancy`

**Authentication:** Required

**Description:** Get current hotel occupancy

**Response:** `200 OK`
```json
{
  "active_guests": 12,
  "date": "2024-01-15"
}
```

---

# System Endpoints

## 1. Health Check

**Endpoint:** `GET /health`

**Authentication:** Not required

**Description:** Check if server is running

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "environment": "development"
}
```

---

## 2. Database Statistics

**Endpoint:** `GET /db-stats`

**Authentication:** Not required

**Description:** Get database statistics

**Response:** `200 OK`
```json
{
  "users": 5,
  "hotels": 2,
  "menus": 24,
  "billings": 15,
  "invoices": 30,
  "otps": 0
}
```

---

# Example Usage

## Complete Flow

### 1. Register and Login
```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "hotelowner",
    "password": "password123",
    "phone_number": "+919876543210",
    "email": "owner@hotel.com"
  }'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "hotelowner",
    "password": "password123"
  }'
```

### 2. Create Hotel
```bash
curl -X POST http://localhost:5000/api/hotel/create \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Hotel",
    "city": "Delhi",
    "total_rooms": 50
  }'
```

### 3. Add Menu Items
```bash
curl -X POST http://localhost:5000/api/menu/create \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Butter Chicken",
    "price": 450.00,
    "category": "Main Course"
  }'
```

---

# Error Handling

## Common Errors

### 400 Bad Request
```json
{
  "error": "Missing required fields"
}
```

### 401 Unauthorized
```json
{
  "error": "Token is missing"
}
```

### 403 Forbidden
```json
{
  "error": "Unauthorized"
}
```

### 404 Not Found
```json
{
  "error": "Hotel not found"
}
```

### 409 Conflict
```json
{
  "error": "Username already exists"
}
```

### 500 Server Error
```json
{
  "error": "Internal server error"
}
```

---

# Testing

Use the included API test script:

```bash
python test_api.py
```

This will test all endpoints automatically and provide colored output.
