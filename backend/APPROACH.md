# Product Recommendation Engine - Technical Approach

## Overview
This document outlines the technical approach and design decisions made in implementing the AI-powered product recommendation system for the i95dev internship assignment.

## Architecture Overview

### Backend Architecture
- **Framework**: FastAPI 
- **LLM Integration**: Groq API with Gemma2-9b-it model
- **Data Storage**: JSON file-based product catalog
- **API Design**: RESTful endpoints with proper validation

### Key Components

#### 1. Product Service (`services/product_service.py`)
- Handles all product data operations
- Loads and caches product catalog in memory
- Provides filtering methods for categories, brands, and price ranges
- Implements helper methods for retrieving products by various criteria

#### 2. LLM Service (`services/llm_service.py`)
- Core recommendation logic using prompt engineering
- Integrates with Groq API for LLM capabilities
- Implements robust response parsing with fallback mechanisms
- Handles context window limitations through intelligent filtering

#### 3. API Layer (`app.py`)
- FastAPI application with CORS support
- Input validation using Pydantic models
- Error handling with user-friendly messages
- Two main endpoints: `/api/products` and `/api/recommendations`

## Prompt Engineering Strategy

### 1. Context Optimization
```python
# Filter products before sending to LLM 
filtered_products = self._filter_products_by_preferences(all_products, user_preferences)
```
**Rationale:** Instead of sending all 50 products, we pre-filter based on user preferences to:
- Reduce token usage and costs
- Improve response quality by focusing on relevant products
- Ensure faster response times

### 2. Structured Prompt Design
The prompt is structured in clear sections:
1. System Context: Clear role definition as an e-commerce recommendation expert
2. User Preferences: Formatted list of price range, categories, and brands
3. Browsing History: Detailed product information for context
4. Available Products: Filtered catalog with key attributes
5. Task Instructions: Clear criteria and expected output format

### 3. Output Format Specification
``` json
[
  {
    "product_id": "prod001",
    "explanation": "Clear explanation...",
    "score": 9
  }
]
```
##### Key Design Decisions:
- JSON-only output requirement for reliable parsing
- Confidence scores (1-10) to indicate recommendation strength
- Personalized explanations connecting to user's specific context

### 4. Recommendation Criteria
The prompt explicitly defines ranking criteria:
1.  Price range compliance
2.  Category and brand alignment
1. Browsing history patterns
2.  Product ratings
3.  Diversity of recommendations

### Response Parsing Strategy
1. Robust JSON Extraction
    ```Python
    # Multiple fallback strategies for parsing
    cleaned_response = re.sub(r'```json\s*', '', cleaned_response)
    json_match = re.search(r'```math
    [\s\S]*```', cleaned_response)
    ```
2. Validation and Enrichment
    - Validate product IDs exist in catalog
    - Prevent duplicate recommendations
    - Enrich with full product details
    - Provide fallback recommendations if parsing fails
3. Error Handling
    - Graceful degradation with fallback recommendations
    - Detailed error logging for debugging
    - User-friendly error messages
    - 
### Performance Optimizations
1. Product Filtering
    - Pre-filter products based on preferences before LLM call
    - Limit to 40 products in prompt to balance context and token usage
2. Caching Strategy
    - Products loaded once at startup
    - In-memory storage for fast access
    - No database queries during recommendation generation
3. Concurrent Request Handling
    - FastAPI's async support for handling multiple requests
    - Stateless design for horizontal scalability

### Security Considerations
1. API Key Management
    - Environment variables for sensitive data
    - .gitignore to prevent accidental commits
    - Clear documentation on key setup
2. Input Validation
    - Pydantic models for request validation
    - Price range validation
    - Array bounds checking
3. Error Information
    - No sensitive information in error responses
    - Proper logging for debugging without exposing internals

### Conclusion
This implementation demonstrates:
- Effective prompt engineering for accurate recommendations
- Robust error handling for production readiness
- Clean architecture for maintainability
- Performance optimization for scalability
- Comprehensive testing for reliability

The system successfully generates personalized product recommendations by leveraging LLM capabilities while maintaining practical constraints around performance, cost, and user experience.