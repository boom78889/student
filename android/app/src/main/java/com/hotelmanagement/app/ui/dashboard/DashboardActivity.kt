package com.hotelmanagement.app.ui.dashboard

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.hotelmanagement.app.R
import com.hotelmanagement.app.ui.auth.LoginActivity
import com.hotelmanagement.app.ui.billing.BillingActivity
import com.hotelmanagement.app.ui.hotel.HotelActivity
import com.hotelmanagement.app.ui.menu.MenuActivity
import com.hotelmanagement.app.ui.reports.ReportsActivity
import com.hotelmanagement.app.utils.SharedPrefManager

class DashboardActivity : AppCompatActivity() {
    
    private lateinit var prefManager: SharedPrefManager
    private lateinit var welcomeText: TextView
    private lateinit var hotelCardBtn: Button
    private lateinit var menuCardBtn: Button
    private lateinit var billingCardBtn: Button
    private lateinit var reportsCardBtn: Button
    private lateinit var logoutBtn: Button
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_dashboard)
        
        prefManager = SharedPrefManager(this)
        initViews()
        setupListeners()
        loadDashboardData()
    }
    
    private fun initViews() {
        welcomeText = findViewById(R.id.welcomeText)
        hotelCardBtn = findViewById(R.id.hotelCardBtn)
        menuCardBtn = findViewById(R.id.menuCardBtn)
        billingCardBtn = findViewById(R.id.billingCardBtn)
        reportsCardBtn = findViewById(R.id.reportsCardBtn)
        logoutBtn = findViewById(R.id.logoutBtn)
    }
    
    private fun setupListeners() {
        hotelCardBtn.setOnClickListener {
            startActivity(Intent(this, HotelActivity::class.java))
        }
        
        menuCardBtn.setOnClickListener {
            startActivity(Intent(this, MenuActivity::class.java))
        }
        
        billingCardBtn.setOnClickListener {
            startActivity(Intent(this, BillingActivity::class.java))
        }
        
        reportsCardBtn.setOnClickListener {
            startActivity(Intent(this, ReportsActivity::class.java))
        }
        
        logoutBtn.setOnClickListener {
            logout()
        }
    }
    
    private fun loadDashboardData() {
        val username = prefManager.getUsername() ?: "User"
        val hotelName = prefManager.getHotelName() ?: "No Hotel"
        welcomeText.text = "Welcome, $username!\n$hotelName"
    }
    
    private fun logout() {
        prefManager.logout()
        startActivity(Intent(this, LoginActivity::class.java))
        finish()
    }
}
