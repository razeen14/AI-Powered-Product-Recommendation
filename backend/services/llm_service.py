
from config import config
from groq import Groq

class LLMService:
    """
    Service to handle interactions with the LLM API
    """
    
    def __init__(self):
        """
        Initialize the LLM service with configuration
        """
        self.client = Groq(api_key=config.GROQ_API_KEY)
        self.model_name = config.MODEL_NAME
        self.max_tokens = config.MAX_TOKENS
        self.temperature = config.TEMPERATURE
    
    def generate_recommendations(self, user_preferences, browsing_history, all_products):
        """
        Generate personalized product recommendations based on user preferences and browsing history
        
        Parameters:
        - user_preferences (dict): User's stated preferences
        - browsing_history (list): List of product IDs the user has viewed
        - all_products (list): Full product catalog
        
        Returns:
        - dict: Recommended products with explanations
        """
        # TODO: Implement LLM-based recommendation logic
        # This is where your prompt engineering expertise will be evaluated
        
        # Get browsed products details
        browsed_products = []
        for product_id in browsing_history:
            for product in all_products:
                if product["id"] == product_id:
                    browsed_products.append(product)
                    break
        
        # Create a prompt for the LLM
        # IMPLEMENT YOUR PROMPT ENGINEERING HERE
        prompt = self._create_recommendation_prompt(user_preferences, browsed_products, all_products)
        
        # Call the LLM API
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a smart e-commerce recommendation system like those used by Myntra or Amazon. Write recommendations in a direct, engaging style without referring to 'the user' - speak directly as if describing why someone should buy this product. Always respond with valid JSON only, no additional text."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Parse the LLM response to extract recommendations
            # IMPLEMENT YOUR RESPONSE PARSING LOGIC HERE
            recommendations = self._parse_recommendation_response(response.choices[0].message.content, all_products)
            
            return recommendations
            
        except Exception as e:
            # Handle any errors from the LLM API
            print(f"Error calling LLM API: {str(e)}")
            raise Exception(f"Failed to generate recommendations: {str(e)}")
    
    def _create_recommendation_prompt(self, user_preferences, browsed_products, all_products):
        """
        Create a prompt for the LLM to generate recommendations
        
        Parameters:
        - user_preferences (dict): User's stated preferences
        - browsed_products (list): Products the user has viewed
        - all_products (list): Full product catalog
        
        Returns:
        - str: Prompt for the LLM
        """
        #Filter products based on preferences to reduce token usage
        filtered_products = self._filter_products_by_preferences(all_products, user_preferences)

        #Prompt
        prompt = """You are an expert e-commerce recommendation system similar to Myntra or Amazon. Analyze the preferences and browsing history to recommend exactly 5 products.

IMPORTANT: 
1. You must respond with a valid JSON array containing exactly 5 recommendations.
2. Write explanations in a direct, engaging style like real shopping apps do
3. NEVER mention "the user", "for the user", "the customer" etc.
4. Write as if you're describing why this product is great, not why it's great for someone

USER PREFERENCES:
"""
        # User Preferences
        price_range = user_preferences.get('priceRange', 'all')
        categories = user_preferences.get('categories', [])
        brands = user_preferences.get('brands', [])

        prompt += f"- Price Range: {price_range}\n"
        prompt += f"- Preferred categories: {', '.join(categories) if categories else 'No specific preference'}\n"
        prompt += f"- Preferred brands: {', '.join(brands) if brands else 'No specific preference'}\n"

        # Detailed Browsing history
        if browsed_products: 
            prompt += "\n BROWSING HISTORY (products user has viewed):\n"
            for product in browsed_products:
                prompt += f"- {product['name']} | Category: {product['category']} | Brand: {product['brand']} | Price: ${product['price']} | Tags: {', '.join(product.get('tags', []))}\n"
        else:
            prompt += "\nBROWSING HISTORY: No previous browsing history\n"

        # Available filtered products
        prompt += f"\nAVAILABLE PRODUCTS TO RECOMMEND FROM ({len(filtered_products)} products after filtering):\n"

        # Include upto 40 most relevant products
        for product in filtered_products[:40]:
            prompt += f"ID: {product['id']} | {product['name']} | Category: {product['category']} | Brand: {product['brand']} | Price: ${product['price']} | Rating: {product['rating']}\n"

        # Response format
        prompt += """TASK: Based on the user's preferences and browsing history, recommend exactly 5 products that would be most appealing to this user.

RECOMMENDATION CRITERIA:
1. Match user's price range preference
2. Align with preferred categories and brands
3. Consider patterns from browsing history (similar items, complementary products)
4. Prioritize highly-rated products
5. Suggest diverse but relevant options

RESPONSE FORMAT: Return ONLY a JSON array with this exact structure:
[
  {
    "product_id": "prod001",
    "explanation": "Direct, engaging 2-3 sentence explanation written like a real shopping app recommendation. Focus on product benefits and why it's a great choice.",
    "score": 9
  }
]

Each recommendation must include:
- product_id: The exact ID from the available products list
- explanation: Direct, engaging reason, how and why is this product recommended (NO mention of 'user' or 'customer')
- score: Confidence score from 1-10

Return ONLY the JSON array, no additional text."""
        
        return prompt
    
    def _filter_products_by_preferences(self, products, preferences):
        """
        Helper method to filter products based on user preferences

        Parameters: 
        - browsed_products (list): Products the user has viewed
        - user_preferences (dict): User's stated preferences

        Returns:
        - list: filtered products 
        """
        filtered = products.copy()

        # Filter by price range
        price_range = preferences.get('priceRange', 'all')
        if price_range == '0-50':
            filtered = [p for p in filtered if p['price'] <= 50]
        elif price_range == '50-100':
            filtered = [p for p in filtered if 50 < p['price'] <= 100]
        elif price_range == '100+':
            filtered = [p for p in filtered if p['price'] > 100]

        # Filter by categories if specified
        categories = preferences.get('categories', [])
        if categories:
            category_filtered = [p for p in filtered if p['category'] in categories]
            if len(category_filtered) >= 10:
                filtered = category_filtered
        
        # Priortize preferred brands but don't exclude others
        brands = preferences.get('brands', [])
        if brands:
            filtered.sort(key=lambda p: 0 if p['brand'] in brands else 1)

        return filtered
    
    def _parse_recommendation_response(self, llm_response, all_products):
        """
        Parse the LLM response to extract product recommendations
        
        Parameters:
        - llm_response (str): Raw response from the LLM
        - all_products (list): Full product catalog to match IDs with full product info
        
        Returns:
        - dict: Structured recommendations
        """
        try:
            import json
            import re

            # Clean response, remove markdown 
            cleaned_response = llm_response.strip()
            cleaned_response = re.sub(r'```json\s*', '', cleaned_response)
            cleaned_response = re.sub(r'```\s*', '', cleaned_response)

            json_match = re.search(r'```math[\s\S]*```', cleaned_response)

            if not json_match:
                # parse entire response
                rec_data = json.loads(cleaned_response)
            else:
                rec_data = json.loads(json_match.group())
            
            # Validate recommendations
            recommendations = []
            seen_products = set() # To avoid duplicates

            for rec in rec_data:
                product_id = rec.get('product_id')
                
                if product_id in seen_products:
                    continue

                product_details = None
                for product in all_products:
                    if product['id'] == product_id:
                        product_details = product
                        break
                
                if product_details:
                    seen_products.add(product_id)
                    recommendations.append({
                        "product": product_details,
                        "explanation": rec.get('explanation', 'This product matches your preferences.'),
                        "confidence_score": int(rec.get('score', '5'))
                    })
            
            if not recommendations:
                # Recommend top-rated products
                fallback_products = sorted(all_products, key=lambda p: p.get('rating', 0),reverse=True)[:5]
                for product in fallback_products:
                    recommendations.append({
                        "product": product,
                        "explanation": f"This highly-rated {product['category'].lower()} product might interest you.",
                        "confidence_score": 5
                    })
            
            return {
                "recommendations": recommendations[:5],
                "count": len(recommendations[:5])
            }
        
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {str(e)}")
            print(f"LLM Response: {llm_response[:500]}...")

            fallback_products = sorted(all_products, key=lambda p: p.get('rating', 0),reverse=True)[:5]
            fallback_recommendations = []

            for product in fallback_products:
                fallback_recommendations.append({
                    "product": product,
                    "explanation": f"This highly-rated {product['category'].lower()} product is popular with our customers.",
                    "confidence_score": 5
                })
            
            return {
                "recommendations": fallback_recommendations,
                "count": len(fallback_recommendations),
                "error": "Used fallback recommendations due to parsing error"
            }
        
        except Exception as e:
            print(f"Unexpected error parsing response: {str(e)}")
            return {
                "recommendations": [],
                "count": 0,
                "error": f"Failed to parse recommendations: {str(e)}"
            }