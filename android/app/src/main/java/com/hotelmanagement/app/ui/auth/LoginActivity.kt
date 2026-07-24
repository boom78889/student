package com.hotelmanagement.app.ui.auth

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.ProgressBar
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.hotelmanagement.app.R
import com.hotelmanagement.app.network.ApiClient
import com.hotelmanagement.app.network.LoginRequest
import com.hotelmanagement.app.utils.SharedPrefManager
import kotlinx.coroutines.launch

class LoginActivity : AppCompatActivity() {
    
    private lateinit var usernameEdit: EditText
    private lateinit var passwordEdit: EditText
    private lateinit var loginBtn: Button
    private lateinit var registerBtn: Button
    private lateinit var progressBar: ProgressBar
    private lateinit var prefManager: SharedPrefManager
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)
        
        prefManager = SharedPrefManager(this)
        
        // Check if already logged in
        if (prefManager.isLoggedIn()) {
            navigateToDashboard()
            return
        }
        
        initViews()
        setupListeners()
    }
    
    private fun initViews() {
        usernameEdit = findViewById(R.id.usernameEdit)
        passwordEdit = findViewById(R.id.passwordEdit)
        loginBtn = findViewById(R.id.loginBtn)
        registerBtn = findViewById(R.id.registerBtn)
        progressBar = findViewById(R.id.progressBar)
    }
    
    private fun setupListeners() {
        loginBtn.setOnClickListener {
            val username = usernameEdit.text.toString().trim()
            val password = passwordEdit.text.toString().trim()
            
            if (validateInputs(username, password)) {
                loginUser(username, password)
            }
        }
        
        registerBtn.setOnClickListener {
            startActivity(android.content.Intent(this, RegisterActivity::class.java))
        }
    }
    
    private fun validateInputs(username: String, password: String): Boolean {
        return when {
            username.isEmpty() -> {
                usernameEdit.error = "Username is required"
                false
            }
            password.isEmpty() -> {
                passwordEdit.error = "Password is required"
                false
            }
            else -> true
        }
    }
    
    private fun loginUser(username: String, password: String) {
        progressBar.visibility = android.view.View.VISIBLE
        loginBtn.isEnabled = false
        
        val request = LoginRequest(username, password)
        val apiService = ApiClient.getApiService()
        
        apiService.login(request).enqueue(object : retrofit2.Callback<com.hotelmanagement.app.network.ApiResponse<com.hotelmanagement.app.network.User>> {
            override fun onResponse(
                call: retrofit2.Call<com.hotelmanagement.app.network.ApiResponse<com.hotelmanagement.app.network.User>>,
                response: retrofit2.Response<com.hotelmanagement.app.network.ApiResponse<com.hotelmanagement.app.network.User>>
            ) {
                progressBar.visibility = android.view.View.GONE
                loginBtn.isEnabled = true
                
                if (response.isSuccessful) {
                    val apiResponse = response.body()
                    if (apiResponse?.token != null && apiResponse.user != null) {
                        prefManager.saveToken(apiResponse.token)
                        prefManager.saveUser(
                            apiResponse.user.id ?: 0,
                            apiResponse.user.username ?: "",
                            apiResponse.user.email,
                            apiResponse.user.phone_number
                        )
                        ApiClient.setToken(apiResponse.token)
                        
                        Toast.makeText(this@LoginActivity, "Login successful!", Toast.LENGTH_SHORT).show()
                        navigateToDashboard()
                    }
                } else {
                    Toast.makeText(this@LoginActivity, "Login failed. Check credentials.", Toast.LENGTH_SHORT).show()
                }
            }
            
            override fun onFailure(
                call: retrofit2.Call<com.hotelmanagement.app.network.ApiResponse<com.hotelmanagement.app.network.User>>,
                t: Throwable
            ) {
                progressBar.visibility = android.view.View.GONE
                loginBtn.isEnabled = true
                Toast.makeText(this@LoginActivity, "Error: ${t.message}", Toast.LENGTH_SHORT).show()
            }
        })
    }
    
    private fun navigateToDashboard() {
        startActivity(android.content.Intent(this, DashboardActivity::class.java))
        finish()
    }
}
