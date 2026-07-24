package com.hotelmanagement.app.network

import retrofit2.Call
import retrofit2.http.*

interface ApiService {
    
    // ===== AUTHENTICATION =====
    @POST("auth/register")
    fun register(@Body request: RegisterRequest): Call<ApiResponse<User>>
    
    @POST("auth/send-otp")
    fun sendOtp(@Body request: OtpRequest): Call<ApiResponse<Any>>
    
    @POST("auth/verify-otp")
    fun verifyOtp(@Body request: OtpRequest): Call<ApiResponse<Any>>
    
    @POST("auth/login")
    fun login(@Body request: LoginRequest): Call<ApiResponse<User>>
    
    // ===== HOTEL =====
    @POST("hotel/create")
    fun createHotel(@Body request: HotelRequest): Call<ApiResponse<Hotel>>
    
    @GET("hotel/{hotel_id}")
    fun getHotel(@Path("hotel_id") hotelId: Int): Call<ApiResponse<Hotel>>
    
    @PUT("hotel/{hotel_id}")
    fun updateHotel(
        @Path("hotel_id") hotelId: Int,
        @Body request: HotelRequest
    ): Call<ApiResponse<Hotel>>
    
    // ===== MENU =====
    @POST("menu/create")
    fun createMenu(@Body request: MenuRequest): Call<ApiResponse<Menu>>
    
    @GET("menu/list")
    fun listMenus(): Call<ApiResponse<List<Menu>>>
    
    @PUT("menu/{menu_id}")
    fun updateMenu(
        @Path("menu_id") menuId: Int,
        @Body request: MenuRequest
    ): Call<ApiResponse<Menu>>
    
    @DELETE("menu/{menu_id}")
    fun deleteMenu(@Path("menu_id") menuId: Int): Call<ApiResponse<Any>>
    
    // ===== BILLING =====
    @POST("billing/create")
    fun createBilling(@Body request: BillingRequest): Call<ApiResponse<Billing>>
    
    @GET("billing/list")
    fun listBillings(): Call<ApiResponse<List<Billing>>>
    
    @POST("billing/{billing_id}/add-invoice")
    fun addInvoice(
        @Path("billing_id") billingId: Int,
        @Body request: InvoiceRequest
    ): Call<ApiResponse<Invoice>>
    
    @POST("billing/{billing_id}/payment")
    fun recordPayment(
        @Path("billing_id") billingId: Int,
        @Body request: PaymentRequest
    ): Call<ApiResponse<Billing>>
    
    // ===== REPORTS =====
    @GET("reports/revenue")
    fun getRevenueReport(@Query("days") days: Int = 30): Call<ApiResponse<Report>>
    
    @GET("reports/menu-popular")
    fun getMenuReport(): Call<ApiResponse<Report>>
    
    @GET("reports/occupancy")
    fun getOccupancyReport(): Call<ApiResponse<Report>>
}
