package com.newsverifier.api

import com.google.gson.Gson
import com.google.gson.GsonBuilder
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

/**
 * Retrofit client singleton for News Verification API
 */
object RetrofitClient {
    
    // IMPORTANT: Replace with your actual server URL
    // Examples:
    // - Local development: "http://10.0.2.2:8000/" (Android emulator)
    // - Same network: "http://192.168.1.100:8000/" (your computer's IP)
    // - Production: "https://your-domain.com/"
    private const val BASE_URL = "http://10.0.2.2:8000/"
    
    private var retrofit: Retrofit? = null
    private var api: NewsVerificationApi? = null
    
    /**
     * Configure and get Gson instance
     */
    private fun getGson(): Gson {
        return GsonBuilder()
            .setLenient()
            .create()
    }
    
    /**
     * Configure OkHttpClient with logging and timeouts
     */
    private fun getOkHttpClient(): OkHttpClient {
        val loggingInterceptor = HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BODY
        }
        
        return OkHttpClient.Builder()
            .addInterceptor(loggingInterceptor)
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(60, TimeUnit.SECONDS)
            .writeTimeout(60, TimeUnit.SECONDS)
            .build()
    }
    
    /**
     * Get Retrofit instance
     */
    private fun getRetrofit(): Retrofit {
        if (retrofit == null) {
            retrofit = Retrofit.Builder()
                .baseUrl(BASE_URL)
                .client(getOkHttpClient())
                .addConverterFactory(GsonConverterFactory.create(getGson()))
                .build()
        }
        return retrofit!!
    }
    
    /**
     * Get API instance
     * 
     * @return NewsVerificationApi instance
     */
    fun getInstance(): NewsVerificationApi {
        if (api == null) {
            api = getRetrofit().create(NewsVerificationApi::class.java)
        }
        return api!!
    }
    
    /**
     * Update base URL dynamically
     * 
     * @param newBaseUrl New base URL to use
     */
    fun updateBaseUrl(newBaseUrl: String) {
        retrofit = Retrofit.Builder()
            .baseUrl(newBaseUrl)
            .client(getOkHttpClient())
            .addConverterFactory(GsonConverterFactory.create(getGson()))
            .build()
        api = retrofit?.create(NewsVerificationApi::class.java)
    }
}
