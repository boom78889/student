package com.hotelmanagement.app.network

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import okhttp3.OkHttpClient
import okhttp3.Interceptor
import java.util.concurrent.TimeUnit

object ApiClient {
    private const val BASE_URL = "http://10.0.2.2:5000/api/"  // For emulator
    // private const val BASE_URL = "http://your_server_ip:5000/api/"  // For real device
    
    private var retrofit: Retrofit? = null
    private var token: String? = null
    
    fun setToken(authToken: String?) {
        token = authToken
    }
    
    private fun getOkHttpClient(): OkHttpClient {
        return OkHttpClient.Builder()
            .addInterceptor(Interceptor { chain ->
                val originalRequest = chain.request()
                val requestBuilder = originalRequest.newBuilder()
                
                // Add token if available
                token?.let {
                    requestBuilder.header("Authorization", "Bearer $it")
                }
                
                requestBuilder.header("Content-Type", "application/json")
                chain.proceed(requestBuilder.build())
            })
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)
            .build()
    }
    
    fun getRetrofit(): Retrofit {
        if (retrofit == null) {
            retrofit = Retrofit.Builder()
                .baseUrl(BASE_URL)
                .client(getOkHttpClient())
                .addConverterFactory(GsonConverterFactory.create())
                .build()
        }
        return retrofit!!
    }
    
    fun getApiService(): ApiService {
        return getRetrofit().create(ApiService::class.java)
    }
}
