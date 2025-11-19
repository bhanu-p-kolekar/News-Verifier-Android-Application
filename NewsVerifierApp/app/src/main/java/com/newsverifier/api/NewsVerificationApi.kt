package com.newsverifier.api

import com.newsverifier.models.HealthResponse
import com.newsverifier.models.VerifyRequest
import com.newsverifier.models.VerifyResponse
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

/**
 * Retrofit API interface for News Verification API
 * 
 * Base URL should be set when creating Retrofit instance
 * Example: http://YOUR_SERVER_IP:8000/
 */
interface NewsVerificationApi {
    
    /**
     * Health check endpoint
     * 
     * @return Health status of the API
     */
    @GET("health")
    suspend fun healthCheck(): Response<HealthResponse>
    
    /**
     * Verify news content endpoint
     * 
     * @param request VerifyRequest containing content to verify
     * @return VerifyResponse with verdict, confidence, summary, and evidence
     */
    @POST("verify")
    suspend fun verifyNews(@Body request: VerifyRequest): Response<VerifyResponse>
}
