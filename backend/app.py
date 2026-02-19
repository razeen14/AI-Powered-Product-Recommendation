from multiprocessing import Value
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel, validator, Field
from typing import List, Dict, Any, Optional
import os

from config import config
from services.llm_service import LLMService
from services.product_service import ProductService

# Validate config
config.validate()

app = FastAPI(title="AI Product Recommendation API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize services
product_service = ProductService()
llm_service = LLMService()

# Define request models
class UserPreferences(BaseModel):
    priceRange: str = Field(
        default="all",
        description="Price range filter: '0-50', '50-100', '100+', or 'all'"
    )
    categories: List[str] = Field(
        default_factory=list,
        description="List of preferred product categories"
    )
    brands: List[str] = Field(
        default_factory=list,
        description="List of preferred brands"
    )

    @validator('priceRange')
    def validate_price_range(cls, v):
        valid_ranges = ['0-50', '50-100', '100+', 'all']
        if v not in valid_ranges:
            raise ValueError(f'Price range must be one of: {", ".join(valid_ranges)}')
        return v
    
    @validator('brands')
    def validate_brands(cls, v):
        if len(v) > 10:
            raise ValueError('Maximum 10 brands are allowed')
        return v
    

class RecommendationRequest(BaseModel):
    preferences: UserPreferences
    browsing_history: List[str] = Field(
        default_factory=list,
        max_items=20,
        description="List of product IDs from browsing history"
    )

    @validator('browsing_history')
    def validate_browsing_history(cls, v):
        #Validate product ID format
        for product_id in v:
            if not product_id.startswith('prod') or not product_id[4:].isdigit():
                raise ValueError(f'Invalid product ID format: {product_id}. Expected format: prodXXX')
        
        return list(set(v))
    
    class Config:
        schema_extra = {
            "example": {
                "preferences": {
                    "priceRange": "50-100",
                    "categories": ["Electronics", "Audio"],
                    "brands": ["SoundWave"]
                },
                "browsing_history": ["prod001", "prod002"]
            }
        }

class ProductResponse(BaseModel):
    id: str
    name: str
    category: str
    subcategory: str
    price: float
    brand: str
    description: str
    features: List[str]
    rating: float
    inventory: int
    tags: List[str]

class RecommendationItem(BaseModel):
    product: ProductResponse
    explanation: str = Field(..., min_length=10, max_length=500)
    confidence_score: int = Field(..., ge=1, le=10)

class RecommendationResponse(BaseModel):
    recommendations: List[RecommendationItem]
    count: int = Field(..., ge=0)
    error: Optional[str] = None
    
    @validator('count', always=True)
    def validate_count(cls, v, values):
        if 'recommendations' in values:
            expected_count = len(values['recommendations'])
            if v != expected_count:
                raise ValueError(f'Count mismatch: {v} != {expected_count}')
        return v

@app.get("/api/products")
async def get_products():
    """
    Return the full product catalog
    """
    products = product_service.get_all_products()
    return products

@app.post("/api/recommendations", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """
    Generate personalized product recommendations based on user preferences
    and browsing history
    """
    try:
        # Extract user preferences and browsing history from request
        user_preferences = request.preferences.dict()
        browsing_history = request.browsing_history
        
        # Use the LLM service to generate recommendations
        recommendations = llm_service.generate_recommendations(
            user_preferences,
            browsing_history,
            product_service.get_all_products()
        )
        
        return RecommendationResponse(**recommendations)
    
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Custom exception handler for more user-friendly error messages
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return {
        "error": str(exc),
        "message": "An error occurred while processing your request"
    }

if __name__ == "__main__":
    # Run the API with uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)