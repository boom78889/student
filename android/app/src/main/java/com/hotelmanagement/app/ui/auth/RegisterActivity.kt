package com.hotelmanagement.app.ui.auth

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.ProgressBar
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.hotelmanagement.app.R
import com.hotelmanagement.app.network.ApiClient
import com.hotelmanagement.app.network.OtpRequest
import com.hotelmanagement.app.network.RegisterRequest
import com.hotelmanagement.app.utils.SharedPrefManager

class RegisterActivity : AppCompatActivity() {
    
    private lateinit var usernameEdit: EditText
    private lateinit var phoneEdit: EditText
    private lateinit var emailEdit: EditText
    private lateinit var passwordEdit: EditText
    private lateinit var confirmPasswordEdit: EditText
    private lateinit var registerBtn: Button
    private lateinit var progressBar: ProgressBar
    private lateinit var prefManager: SharedPrefManager
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_register)
        
        prefManager = SharedPrefManager(this)
        initViews()
        setupListeners()
    }
    
    private fun initViews() {
        usernameEdit = findViewById(R.id.usernameEdit)
        phoneEdit = findViewById(R.id.phoneEdit)
        emailEdit = findViewById(R.id.emailEdit)
        passwordEdit = findViewById(R.id.passwordEdit)
        confirmPasswordEdit = findViewById(R.id.confirmPasswordEdit)
        registerBtn = findViewById(R.id.registerBtn)
        progressBar = findViewById(R.id.progressBar)
    }
    
    private fun setupListeners() {
        registerBtn.setOnClickListener {
            val username = usernameEdit.text.toString().trim()
            val phone = phoneEdit.text.toString().trim()
            val email = emailEdit.text.toString().trim()
            val password = passwordEdit.text.toString().trim()
            val confirmPassword = confirmPasswordEdit.text.toString().trim()
            
            if (validateInputs(username, phone, email, password, confirmPassword)) {
                registerUser(username, phone, email, password)
            }
        }
    }
    
    private fun validateInputs(
        username: String,
        phone: String,
        email: String,
        password: String,
        confirmPassword: String
    ): Boolean {
        return when {
            username.isEmpty() -> {
                usernameEdit.error = "Username required"
                false
            }
            phone.isEmpty() -> {
                phoneEdit.error = "Phone number required"
                false
            }
            password.isEmpty() -> {
                passwordEdit.error = "Password required"
                false
            }
            password != confirmPassword -> {
                confirmPasswordEdit.error = "Passwords don't match"
                false
            }
            password.length < 6 -> {
                passwordEdit.error = "Password must be at least 6 characters"
                false
            }
            else -> true
        }
    }
    
    private fun registerUser(username: String, phone: String, email: String, password: String) {
        progressBar.visibility = android.view.View.VISIBLE
        registerBtn.isEnabled = false
        
        val request = RegisterRequest(username, password, phone, email)
        val apiService = ApiClient.getApiService()
        
        apiService.register(request).enqueue(object : retrofit2.Callback<com.hotelmanagement.app.network.ApiResponse<com.hotelmanagement.app.network.User>> {
            override fun onResponse(
                call: retrofit2.Call<com.hotelmanagement.app.network.ApiResponse<com.hotelmanagement.app.network.User>>,
                response: retrofit2.Response<com.hotelmanagement.app.network.ApiResponse<com.hotelmanagement.app.network.User>>
            ) {
                progressBar.visibility = android.view.View.GONE
                registerBtn.isEnabled = true
                
                if (response.isSuccessful) {
                    Toast.makeText(this@RegisterActivity, "Registration successful! Please verify OTP.", Toast.LENGTH_SHORT).show()
                    // Navigate to OTP verification
                    val intent = android.content.Intent(this@RegisterActivity, OtpActivity::class.java)
                    intent.putExtra("phone", phone)
                    startActivity(intent)
                    finish()
                } else {
                    Toast.makeText(this@RegisterActivity, "Registration failed", Toast.LENGTH_SHORT).show()
                }
            }
            
            override fun onFailure(
                call: retrofit2.Call<com.hotelmanagement.app.network.ApiResponse<com.hotelmanagement.app.network.User>>,
                t: Throwable
            ) {
                progressBar.visibility = android.view.View.GONE
                registerBtn.isEnabled = true
                Toast.makeText(this@RegisterActivity, "Error: ${t.message}", Toast.LENGTH_SHORT).show()
            }
        })
    }
}
