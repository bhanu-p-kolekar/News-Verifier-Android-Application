package com.newsverifier.repository

import com.newsverifier.api.NewsVerificationApi
import com.newsverifier.api.RetrofitClient
import com.newsverifier.models.ApiResult
import com.newsverifier.models.VerifyRequest
import com.newsverifier.models.VerifyResponse
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/**
 * Repository for handling news verification API calls
 * Provides a clean interface between UI and network layer
 */
class NewsVerificationRepository {
    
    private val api: NewsVerificationApi = RetrofitClient.getInstance()
    
    /**
     * Verify news content
     * 
     * @param content News content to verify (text or URL)
     * @return ApiResult with VerifyResponse or error
     */
    suspend fun verifyNews(content: String): ApiResult<VerifyResponse> {
        return withContext(Dispatchers.IO) {
            try {
                val request = VerifyRequest(content)
                val response = api.verifyNews(request)
                
                if (response.isSuccessful && response.body() != null) {
                    ApiResult.Success(response.body()!!)
                } else {
                    val errorMessage = response.errorBody()?.string() 
                        ?: "Unknown error occurred"
                    ApiResult.Error(errorMessage, response.code())
                }
            } catch (e: Exception) {
                ApiResult.Error(e.message ?: "Network error occurred")
            }
        }
    }
    
    /**
     * Check API health status
     * 
     * @return True if API is healthy, false otherwise
     */
    suspend fun checkHealth(): Boolean {
        return withContext(Dispatchers.IO) {
            try {
                val response = api.healthCheck()
                response.isSuccessful
            } catch (e: Exception) {
                false
            }
        }
    }
}
