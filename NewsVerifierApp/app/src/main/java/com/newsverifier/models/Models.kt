package com.newsverifier.models

import com.google.gson.annotations.SerializedName

/**
 * Request model for news verification
 * 
 * @property content The news content to verify (can be text or URL)
 */
data class VerifyRequest(
    @SerializedName("content")
    val content: String
)

/**
 * Response model for news verification
 * 
 * @property verdict Verification verdict: True, False, Misleading, or Unverified
 * @property confidence Confidence score from 0 to 100
 * @property summary Brief summary of the verification analysis
 * @property evidenceLinks List of URLs used as evidence
 */
data class VerifyResponse(
    @SerializedName("verdict")
    val verdict: String,
    
    @SerializedName("confidence")
    val confidence: Int,
    
    @SerializedName("summary")
    val summary: String,
    
    @SerializedName("evidence_links")
    val evidenceLinks: List<String>
)

/**
 * Health check response model
 * 
 * @property status Service status
 * @property message Status message
 */
data class HealthResponse(
    @SerializedName("status")
    val status: String,
    
    @SerializedName("message")
    val message: String
)

/**
 * Error response model for API errors
 * 
 * @property detail Error detail message
 */
data class ErrorResponse(
    @SerializedName("detail")
    val detail: String
)

/**
 * Sealed class representing API Result states
 */
sealed class ApiResult<out T> {
    data class Success<out T>(val data: T) : ApiResult<T>()
    data class Error(val message: String, val code: Int? = null) : ApiResult<Nothing>()
    object Loading : ApiResult<Nothing>()
}
