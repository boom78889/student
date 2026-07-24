package com.hotelmanagement.app.ui.hotel

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ProgressBar
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.hotelmanagement.app.R
import com.hotelmanagement.app.network.ApiClient
import com.hotelmanagement.app.network.HotelRequest
import com.hotelmanagement.app.utils.SharedPrefManager

class HotelActivity : AppCompatActivity() {
    
    private lateinit var hotelNameEdit: EditText
    private lateinit var descriptionEdit: EditText
    private lateinit var addressEdit: EditText
    private lateinit var cityEdit: EditText
    private lateinit var stateEdit: EditText
    private lateinit var zipcodeEdit: EditText
    private lateinit var phoneEdit: EditText
    private lateinit var emailEdit: EditText
    private lateinit var totalRoomsEdit: EditText
    private lateinit var checkInEdit: EditText
    private lateinit var checkOutEdit: EditText
    private lateinit var currencyEdit: EditText
    private lateinit var saveBtn: Button
    private lateinit var progressBar: ProgressBar
    private lateinit var prefManager: SharedPrefManager
    private var hotelId: Int? = null
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_hotel)
        
        prefManager = SharedPrefManager(this)
        hotelId = prefManager.getHotelId()
        
        initViews()
        setupListeners()
        
        if (hotelId != null) {
            loadHotelData()
        }
    }
    
    private fun initViews() {
        hotelNameEdit = findViewById(R.id.hotelNameEdit)
        descriptionEdit = findViewById(R.id.descriptionEdit)
        addressEdit = findViewById(R.id.addressEdit)
        cityEdit = findViewById(R.id.cityEdit)
        stateEdit = findViewById(R.id.stateEdit)
        zipcodeEdit = findViewById(R.id.zipcodeEdit)
        phoneEdit = findViewById(R.id.phoneEdit)
        emailEdit = findViewById(R.id.emailEdit)
        totalRoomsEdit = findViewById(R.id.totalRoomsEdit)
        checkInEdit = findViewById(R.id.checkInEdit)
        checkOutEdit = findViewById(R.id.checkOutEdit)
        currencyEdit = findViewById(R.id.currencyEdit)
        saveBtn = findViewById(R.id.saveBtn)
        progressBar = findViewById(R.id.progressBar)
    }
    
    private fun setupListeners() {
        saveBtn.setOnClickListener {
            saveHotel()
        }
    }
    
    private fun loadHotelData() {
        progressBar.visibility = android.view.View.VISIBLE
        
        hotelId?.let { id ->
            val apiService = ApiClient.getApiService()
            
            apiService.getHotel(id).enqueue(object : retrofit2.Callback<com.hotelmanagement.app.network.ApiResponse<com.hotelmanagement.app.network.Hotel>> {
                override fun onResponse(
                    call: retrofit2.Call<com.hotelmanagement.app.network.ApiResponse<com.hotelmanagement.app.network.Hotel>>,
                    response: retrofit2.Response<com.hotelmanagement.app.network.ApiResponse<com.hotelmanagement.app.network.Hotel>>
                ) {
                    progressBar.visibility = android.view.View.GONE
                    
                    if (response.isSuccessful) {
                        response.body()?.hotel?.let { hotel ->
                            hotelNameEdit.setText(hotel.name)
                            descriptionEdit.setText(hotel.description)
                            addressEdit.setText(hotel.address)
                            cityEdit.setText(hotel.city)
                            stateEdit.setText(hotel.state)
                            zipcodeEdit.setText(hotel.zipcode)
                            phoneEdit.setText(hotel.phone_number)
                            emailEdit.setText(hotel.email)
                            totalRoomsEdit.setText(hotel.total_rooms.toString())
                            checkInEdit.setText(hotel.check_in_time)
                            checkOutEdit.setText(hotel.check_out_time)
                            currencyEdit.setText(hotel.currency)
                        }
                    }
                }
                
                override fun onFailure(
                    call: retrofit2.Call<com.hotelmanagement.app.network.ApiResponse<com.hotelmanagement.app.network.Hotel>>,
                    t: Throwable
                ) {
                    progressBar.visibility = android.view.View.GONE
                    Toast.makeText(this@HotelActivity, "Error: ${t.message}", Toast.LENGTH_SHORT).show()
                }
            })
        }
    }
    
    private fun saveHotel() {
        val hotelName = hotelNameEdit.text.toString().trim()
        
        if (hotelName.isEmpty()) {
            hotelNameEdit.error = "Hotel name required"
            return
        }
        
        progressBar.visibility = android.view.View.VISIBLE
        saveBtn.isEnabled = false
        
        val request = HotelRequest(
            name = hotelName,
            description = descriptionEdit.text.toString(),
            address = addressEdit.text.toString(),
            city = cityEdit.text.toString(),
            state = stateEdit.text.toString(),
            zipcode = zipcodeEdit.text.toString(),
            phone_number = phoneEdit.text.toString(),
            email = emailEdit.text.toString(),
            total_rooms = totalRoomsEdit.text.toString().toIntOrNull() ?: 0,
            check_in_time = checkInEdit.text.toString(),
            check_out_time = checkOutEdit.text.toString(),
            currency = currencyEdit.text.toString()
        )
        
        val apiService = ApiClient.getApiService()
        
        if (hotelId != null) {
            // Update existing hotel
            apiService.updateHotel(hotelId!!, request).enqueue(object : retrofit2.Callback<com.hotelmanagement.app.network.ApiResponse<com.hotelmanagement.app.network.Hotel>> {
                override fun onResponse(
                    call: retrofit2.Call<com.hotelmanagement.app.network.ApiResponse<com.hotelmanagement.app.network.Hotel>>,
                    response: retrofit2.Response<com.hotelmanagement.app.network.ApiResponse<com.hotelmanagement.app.network.Hotel>>
                ) {
                    progressBar.visibility = android.view.View.GONE
                    saveBtn.isEnabled = true
                    
                    if (response.isSuccessful) {
                        Toast.makeText(this@HotelActivity, "Hotel updated successfully", Toast.LENGTH_SHORT).show()
                        finish()
                    }
                }
                
                override fun onFailure(
                    call: retrofit2.Call<com.hotelmanagement.app.network.ApiResponse<com.hotelmanagement.app.network.Hotel>>,
                    t: Throwable
                ) {
                    progressBar.visibility = android.view.View.GONE
                    saveBtn.isEnabled = true
                    Toast.makeText(this@HotelActivity, "Error: ${t.message}", Toast.LENGTH_SHORT).show()
                }
            })
        } else {
            // Create new hotel
            apiService.createHotel(request).enqueue(object : retrofit2.Callback<com.hotelmanagement.app.network.ApiResponse<com.hotelmanagement.app.network.Hotel>> {
                override fun onResponse(
                    call: retrofit2.Call<com.hotelmanagement.app.network.ApiResponse<com.hotelmanagement.app.network.Hotel>>,
                    response: retrofit2.Response<com.hotelmanagement.app.network.ApiResponse<com.hotelmanagement.app.network.Hotel>>
                ) {
                    progressBar.visibility = android.view.View.GONE
                    saveBtn.isEnabled = true
                    
                    if (response.isSuccessful) {
                        response.body()?.hotel?.let { hotel ->
                            prefManager.saveHotel(hotel.id ?: 0, hotel.name ?: "")
                            Toast.makeText(this@HotelActivity, "Hotel created successfully", Toast.LENGTH_SHORT).show()
                            finish()
                        }
                    }
                }
                
                override fun onFailure(
                    call: retrofit2.Call<com.hotelmanagement.app.network.ApiResponse<com.hotelmanagement.app.network.Hotel>>,
                    t: Throwable
                ) {
                    progressBar.visibility = android.view.View.GONE
                    saveBtn.isEnabled = true
                    Toast.makeText(this@HotelActivity, "Error: ${t.message}", Toast.LENGTH_SHORT).show()
                }
            })
        }
    }
}
