package com.hotelmanagement.app.ui.auth

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.hotelmanagement.app.R
import com.hotelmanagement.app.network.ApiClient
import com.hotelmanagement.app.network.OtpRequest

class OtpActivity : AppCompatActivity() {
    
    private lateinit var otpEdit: EditText
    private lateinit var verifyBtn: Button
    private lateinit var resendBtn: Button
    private lateinit var progressBar: ProgressBar
    private lateinit var phoneText: TextView
    private var phoneNumber: String? = null
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_otp)
        
        phoneNumber = intent.getStringExtra("phone")
        
        initViews()
        setupListeners()
        
        phoneText.text = "OTP sent to $phoneNumber"
        sendOtp()
    }
    
    private fun initViews() {
        otpEdit = findViewById(R.id.otpEdit)
        verifyBtn = findViewById(R.id.verifyBtn)
        resendBtn = findViewById(R.id.resendBtn)
        progressBar = findViewById(R.id.progressBar)
        phoneText = findViewById(R.id.phoneText)
    }
    
    private fun setupListeners() {
        verifyBtn.setOnClickListener {
            val otp = otpEdit.text.toString().trim()
            if (otp.isEmpty()) {
                otpEdit.error = "OTP required"
            } else {
                verifyOtp(otp)
            }
        }
        
        resendBtn.setOnClickListener {
            sendOtp()
        }
    }
    
    private fun sendOtp() {
        phoneNumber?.let {
            val request = OtpRequest(it)
            val apiService = ApiClient.getApiService()
            
            apiService.sendOtp(request).enqueue(object : retrofit2.Callback<com.hotelmanagement.app.network.ApiResponse<Any>> {
                override fun onResponse(
                    call: retrofit2.Call<com.hotelmanagement.app.network.ApiResponse<Any>>,
                    response: retrofit2.Response<com.hotelmanagement.app.network.ApiResponse<Any>>
                ) {
                    if (response.isSuccessful) {
                        Toast.makeText(this@OtpActivity, "OTP sent successfully", Toast.LENGTH_SHORT).show()
                    }
                }
                
                override fun onFailure(
                    call: retrofit2.Call<com.hotelmanagement.app.network.ApiResponse<Any>>,
                    t: Throwable
                ) {
                    Toast.makeText(this@OtpActivity, "Error: ${t.message}", Toast.LENGTH_SHORT).show()
                }
            })
        }
    }
    
    private fun verifyOtp(otp: String) {
        progressBar.visibility = android.view.View.VISIBLE
        verifyBtn.isEnabled = false
        
        phoneNumber?.let {
            val request = OtpRequest(it, otp)
            val apiService = ApiClient.getApiService()
            
            apiService.verifyOtp(request).enqueue(object : retrofit2.Callback<com.hotelmanagement.app.network.ApiResponse<Any>> {
                override fun onResponse(
                    call: retrofit2.Call<com.hotelmanagement.app.network.ApiResponse<Any>>,
                    response: retrofit2.Response<com.hotelmanagement.app.network.ApiResponse<Any>>
                ) {
                    progressBar.visibility = android.view.View.GONE
                    verifyBtn.isEnabled = true
                    
                    if (response.isSuccessful) {
                        Toast.makeText(this@OtpActivity, "OTP verified! Please login.", Toast.LENGTH_SHORT).show()
                        finish()
                    } else {
                        Toast.makeText(this@OtpActivity, "Invalid OTP", Toast.LENGTH_SHORT).show()
                    }
                }
                
                override fun onFailure(
                    call: retrofit2.Call<com.hotelmanagement.app.network.ApiResponse<Any>>,
                    t: Throwable
                ) {
                    progressBar.visibility = android.view.View.GONE
                    verifyBtn.isEnabled = true
                    Toast.makeText(this@OtpActivity, "Error: ${t.message}", Toast.LENGTH_SHORT).show()
                }
            })
        }
    }
}
