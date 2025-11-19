package com.newsverifier.ui

import android.content.Intent
import android.graphics.Color
import android.net.Uri
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.ViewModelProvider
import com.google.android.material.chip.Chip
import com.newsverifier.databinding.ActivityMainBinding
import com.newsverifier.models.ApiResult
import com.newsverifier.models.VerifyResponse
import com.newsverifier.viewmodel.NewsVerificationViewModel

/**
 * Main Activity for News Verification App
 */
class MainActivity : AppCompatActivity() {
    
    private lateinit var binding: ActivityMainBinding
    private lateinit var viewModel: NewsVerificationViewModel
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Initialize ViewBinding
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        // Initialize ViewModel
        viewModel = ViewModelProvider(this)[NewsVerificationViewModel::class.java]
        
        // Setup UI
        setupListeners()
        observeViewModel()
        
        // Check API health on start
        viewModel.checkApiHealth()
    }
    
    /**
     * Setup click listeners
     */
    private fun setupListeners() {
        // Verify button click
        binding.btnVerify.setOnClickListener {
            val content = binding.etContent.text.toString()
            viewModel.verifyNews(content)
        }
        
        // Clear button click
        binding.btnClear.setOnClickListener {
            clearUI()
            viewModel.clearResult()
        }
    }
    
    /**
     * Observe ViewModel LiveData
     */
    private fun observeViewModel() {
        // Observe verification results
        viewModel.verificationResult.observe(this) { result ->
            when (result) {
                is ApiResult.Loading -> {
                    showLoading(true)
                    hideResults()
                }
                is ApiResult.Success -> {
                    showLoading(false)
                    displayResults(result.data)
                }
                is ApiResult.Error -> {
                    showLoading(false)
                    hideResults()
                    showError(result.message)
                }
                null -> {
                    showLoading(false)
                    hideResults()
                }
            }
        }
        
        // Observe API health
        viewModel.apiHealthy.observe(this) { isHealthy ->
            binding.tvApiStatus.text = if (isHealthy) {
                binding.tvApiStatus.setTextColor(Color.GREEN)
                "API: Connected ✓"
            } else {
                binding.tvApiStatus.setTextColor(Color.RED)
                "API: Disconnected ✗"
            }
        }
    }
    
    /**
     * Display verification results
     */
    private fun displayResults(response: VerifyResponse) {
        binding.resultsContainer.visibility = View.VISIBLE
        
        // Display verdict with colored badge
        binding.tvVerdict.text = response.verdict
        binding.tvVerdict.setBackgroundColor(getVerdictColor(response.verdict))
        
        // Display confidence
        binding.tvConfidence.text = "Confidence: ${response.confidence}%"
        binding.progressConfidence.progress = response.confidence
        
        // Display summary
        binding.tvSummary.text = response.summary
        
        // Display evidence links
        displayEvidenceLinks(response.evidenceLinks)
    }
    
    /**
     * Get color for verdict badge
     */
    private fun getVerdictColor(verdict: String): Int {
        return when (verdict.lowercase()) {
            "true" -> Color.parseColor("#4CAF50")  // Green
            "false" -> Color.parseColor("#F44336")  // Red
            "misleading" -> Color.parseColor("#FF9800")  // Orange
            "unverified" -> Color.parseColor("#9E9E9E")  // Gray
            else -> Color.parseColor("#2196F3")  // Blue (default)
        }
    }
    
    /**
     * Display evidence links as clickable chips
     */
    private fun displayEvidenceLinks(links: List<String>) {
        binding.chipGroupEvidence.removeAllViews()
        
        if (links.isEmpty()) {
            binding.tvEvidenceLabel.visibility = View.GONE
            binding.chipGroupEvidence.visibility = View.GONE
            return
        }
        
        binding.tvEvidenceLabel.visibility = View.VISIBLE
        binding.chipGroupEvidence.visibility = View.VISIBLE
        
        links.forEachIndexed { index, link ->
            val chip = Chip(this).apply {
                text = "Source ${index + 1}"
                isClickable = true
                setOnClickListener {
                    openUrl(link)
                }
            }
            binding.chipGroupEvidence.addView(chip)
        }
    }
    
    /**
     * Open URL in browser
     */
    private fun openUrl(url: String) {
        try {
            val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
            startActivity(intent)
        } catch (e: Exception) {
            Toast.makeText(this, "Could not open link", Toast.LENGTH_SHORT).show()
        }
    }
    
    /**
     * Show/hide loading state
     */
    private fun showLoading(show: Boolean) {
        binding.progressBar.visibility = if (show) View.VISIBLE else View.GONE
        binding.btnVerify.isEnabled = !show
        binding.btnVerify.text = if (show) "Verifying..." else "Verify News"
    }
    
    /**
     * Hide results container
     */
    private fun hideResults() {
        binding.resultsContainer.visibility = View.GONE
    }
    
    /**
     * Show error message
     */
    private fun showError(message: String) {
        Toast.makeText(this, "Error: $message", Toast.LENGTH_LONG).show()
    }
    
    /**
     * Clear all UI fields
     */
    private fun clearUI() {
        binding.etContent.text?.clear()
        hideResults()
    }
}
