package com.newsverifier.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.newsverifier.models.ApiResult
import com.newsverifier.models.VerifyResponse
import com.newsverifier.repository.NewsVerificationRepository
import kotlinx.coroutines.launch

/**
 * ViewModel for News Verification Screen
 * Manages UI state and handles business logic
 */
class NewsVerificationViewModel : ViewModel() {
    
    private val repository = NewsVerificationRepository()
    
    // LiveData for verification result
    private val _verificationResult = MutableLiveData<ApiResult<VerifyResponse>>()
    val verificationResult: LiveData<ApiResult<VerifyResponse>> = _verificationResult
    
    // LiveData for API health status
    private val _apiHealthy = MutableLiveData<Boolean>()
    val apiHealthy: LiveData<Boolean> = _apiHealthy
    
    /**
     * Verify news content
     * 
     * @param content News content to verify (text or URL)
     */
    fun verifyNews(content: String) {
        // Validate input
        if (content.isBlank()) {
            _verificationResult.value = ApiResult.Error("Please enter content to verify")
            return
        }
        
        if (content.length < 10) {
            _verificationResult.value = ApiResult.Error("Content is too short (minimum 10 characters)")
            return
        }
        
        // Set loading state
        _verificationResult.value = ApiResult.Loading
        
        // Make API call
        viewModelScope.launch {
            val result = repository.verifyNews(content)
            _verificationResult.value = result
        }
    }
    
    /**
     * Check if API is reachable
     */
    fun checkApiHealth() {
        viewModelScope.launch {
            val isHealthy = repository.checkHealth()
            _apiHealthy.value = isHealthy
        }
    }
    
    /**
     * Clear verification result
     */
    fun clearResult() {
        _verificationResult.value = null
    }
}
