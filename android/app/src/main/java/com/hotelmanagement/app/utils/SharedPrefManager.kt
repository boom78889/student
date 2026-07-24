package com.hotelmanagement.app.utils

import android.content.Context
import android.content.SharedPreferences

class SharedPrefManager(context: Context) {
    private val sharedPref: SharedPreferences = context.getSharedPreferences(
        "hotel_app",
        Context.MODE_PRIVATE
    )
    private val editor = sharedPref.edit()
    
    companion object {
        private const val TOKEN = "token"
        private const val USER_ID = "user_id"
        private const val USERNAME = "username"
        private const val EMAIL = "email"
        private const val PHONE = "phone_number"
        private const val HOTEL_ID = "hotel_id"
        private const val HOTEL_NAME = "hotel_name"
    }
    
    fun saveToken(token: String) {
        editor.putString(TOKEN, token).apply()
    }
    
    fun getToken(): String? {
        return sharedPref.getString(TOKEN, null)
    }
    
    fun saveUser(userId: Int, username: String, email: String?, phone: String?) {
        editor.putInt(USER_ID, userId)
        editor.putString(USERNAME, username)
        editor.putString(EMAIL, email ?: "")
        editor.putString(PHONE, phone ?: "")
        editor.apply()
    }
    
    fun getUserId(): Int? {
        val id = sharedPref.getInt(USER_ID, -1)
        return if (id != -1) id else null
    }
    
    fun getUsername(): String? {
        return sharedPref.getString(USERNAME, null)
    }
    
    fun saveHotel(hotelId: Int, hotelName: String) {
        editor.putInt(HOTEL_ID, hotelId)
        editor.putString(HOTEL_NAME, hotelName)
        editor.apply()
    }
    
    fun getHotelId(): Int? {
        val id = sharedPref.getInt(HOTEL_ID, -1)
        return if (id != -1) id else null
    }
    
    fun getHotelName(): String? {
        return sharedPref.getString(HOTEL_NAME, null)
    }
    
    fun isLoggedIn(): Boolean {
        return sharedPref.getString(TOKEN, null) != null
    }
    
    fun logout() {
        editor.clear().apply()
    }
}
