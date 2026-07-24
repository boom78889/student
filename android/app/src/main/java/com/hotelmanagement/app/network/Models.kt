package com.hotelmanagement.app.network

import com.google.gson.annotations.SerializedName

// Response models
data class ApiResponse<T>(
    val message: String? = null,
    val data: T? = null,
    val error: String? = null,
    val token: String? = null,
    val user: User? = null,
    val hotel: Hotel? = null,
    val menu: Menu? = null,
    val billing: Billing? = null,
    val invoice: Invoice? = null,
    val menus: List<Menu>? = null,
    val billings: List<Billing>? = null,
    val otp_id: Int? = null
)

data class User(
    val id: Int? = null,
    val username: String? = null,
    val email: String? = null,
    val phone_number: String? = null,
    val is_verified: Boolean = false,
    val hotel_id: Int? = null,
    val created_at: String? = null
)

data class Hotel(
    val id: Int? = null,
    val name: String? = null,
    val description: String? = null,
    val phone_number: String? = null,
    val email: String? = null,
    val address: String? = null,
    val city: String? = null,
    val state: String? = null,
    val zipcode: String? = null,
    val country: String? = null,
    val logo_url: String? = null,
    val total_rooms: Int = 0,
    val check_in_time: String? = null,
    val check_out_time: String? = null,
    val currency: String? = null,
    val created_at: String? = null
)

data class Menu(
    val id: Int? = null,
    val hotel_id: Int? = null,
    val name: String? = null,
    val description: String? = null,
    val category: String? = null,
    val price: Double = 0.0,
    val availability: Boolean = true,
    val image_url: String? = null,
    val preparation_time: Int? = null,
    val is_vegetarian: Boolean = false,
    val is_vegan: Boolean = false,
    val created_at: String? = null
)

data class Billing(
    val id: Int? = null,
    val hotel_id: Int? = null,
    val guest_name: String? = null,
    val guest_email: String? = null,
    val guest_phone: String? = null,
    val check_in_date: String? = null,
    val check_out_date: String? = null,
    val room_number: String? = null,
    val total_amount: Double = 0.0,
    val paid_amount: Double = 0.0,
    val balance: Double = 0.0,
    val status: String? = null,
    val created_at: String? = null
)

data class Invoice(
    val id: Int? = null,
    val billing_id: Int? = null,
    val invoice_number: String? = null,
    val item_description: String? = null,
    val quantity: Int = 1,
    val unit_price: Double = 0.0,
    val total_price: Double = 0.0,
    val created_at: String? = null
)

data class Report(
    val total_revenue: Double? = null,
    val total_pending: Double? = null,
    val completed_bookings: Int? = null,
    val active_guests: Int? = null,
    val total_items: Int? = null,
    val items: List<Menu>? = null,
    val date: String? = null
)

// Request models
data class LoginRequest(
    val username: String,
    val password: String
)

data class RegisterRequest(
    val username: String,
    val password: String,
    val phone_number: String,
    val email: String? = null
)

data class OtpRequest(
    val phone_number: String,
    val otp_code: String? = null
)

data class HotelRequest(
    val name: String,
    val description: String? = null,
    val phone_number: String? = null,
    val email: String? = null,
    val address: String? = null,
    val city: String? = null,
    val state: String? = null,
    val zipcode: String? = null,
    val country: String? = null,
    val total_rooms: Int = 0,
    val check_in_time: String? = null,
    val check_out_time: String? = null,
    val currency: String? = null
)

data class MenuRequest(
    val name: String,
    val description: String? = null,
    val category: String? = null,
    val price: Double,
    val availability: Boolean = true,
    val image_url: String? = null,
    val preparation_time: Int? = null,
    val is_vegetarian: Boolean = false,
    val is_vegan: Boolean = false
)

data class BillingRequest(
    val guest_name: String,
    val guest_email: String? = null,
    val guest_phone: String? = null,
    val check_in_date: String? = null,
    val check_out_date: String? = null,
    val room_number: String? = null,
    val total_amount: Double = 0.0
)

data class InvoiceRequest(
    val invoice_number: String,
    val item_description: String,
    val quantity: Int = 1,
    val unit_price: Double
)

data class PaymentRequest(
    val amount: Double
)
