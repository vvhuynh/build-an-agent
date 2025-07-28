"""
Grocery Shopping Agent

This agent helps users find ingredients for recipes by searching multiple grocery stores
and optimizing for price and convenience.
"""

import json
import os
import random
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv("../variables.env")

class GroceryAgent:
    def __init__(self):
        """Initialize the grocery shopping agent."""
        nvidia_api_key = os.environ.get("NVIDIA_API_KEY")
        print(f"🔑 API Key found: {nvidia_api_key[:20] if nvidia_api_key else 'None'}...")
        if not nvidia_api_key:
            raise ValueError("NVIDIA_API_KEY environment variable not found")
        
        self.client = OpenAI(
            api_key=nvidia_api_key,
            base_url="https://integrate.api.nvidia.com/v1"
        )
        self.model_name = "meta/llama-3.3-70b-instruct"
        self.conversation_history = []
        
        # Simulated grocery stores with their locations and specialties
        self.grocery_stores = {
            "Walmart": {
                "locations": ["Downtown", "Westside", "Eastside", "North Mall"],
                "specialties": ["budget-friendly", "bulk items", "household goods"],
                "price_range": "budget"
            },
            "Target": {
                "locations": ["Downtown", "Westside", "Eastside"],
                "specialties": ["organic options", "household items", "convenience"],
                "price_range": "mid-range"
            },
            "Whole Foods": {
                "locations": ["Downtown", "Westside"],
                "specialties": ["organic", "premium ingredients", "specialty items"],
                "price_range": "premium"
            },
            "Kroger": {
                "locations": ["Downtown", "Eastside", "Southside"],
                "specialties": ["fresh produce", "dairy", "bakery"],
                "price_range": "mid-range"
            },
            "Trader Joe's": {
                "locations": ["Downtown", "Westside"],
                "specialties": ["unique products", "organic", "prepared foods"],
                "price_range": "mid-range"
            },
            "Aldi": {
                "locations": ["Eastside", "Southside"],
                "specialties": ["budget-friendly", "store brands", "efficiency"],
                "price_range": "budget"
            }
        }
        
        print(f"✅ Connected to {self.model_name}")
        print(f"🔑 API Key: {os.environ.get('NVIDIA_API_KEY')[:20]}...")
        print(f"🏪 Available stores: {', '.join(self.grocery_stores.keys())}")
    
    def _call_llm(self, messages: List[Dict[str, str]], tools: List[Dict] = None):
        """Call the Llama 3.3 70B model."""
        kwargs = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        if tools:
            kwargs["tools"] = tools
        
        try:
            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message
        except Exception as e:
            print(f"❌ Error calling LLM: {e}")
            return None
    
    def _generate_recipe_ingredients(self, food_item: str) -> List[Dict[str, Any]]:
        """Generate a list of ingredients needed for the food item."""
        # Common ingredients for popular dishes with realistic quantities
        recipe_ingredients = {
            "pizza": [
                {"name": "Pizza dough", "category": "Bakery", "quantity": "1 package (16oz)"},
                {"name": "Tomato sauce", "category": "Pantry", "quantity": "1 jar (24oz)"},
                {"name": "Mozzarella cheese", "category": "Dairy", "quantity": "8oz shredded"},
                {"name": "Pepperoni", "category": "Deli", "quantity": "1 package (6oz)"},
                {"name": "Olive oil", "category": "Pantry", "quantity": "2 tbsp"},
                {"name": "Italian seasoning", "category": "Spices", "quantity": "1 tsp"}
            ],
            "pasta": [
                {"name": "Spaghetti", "category": "Pantry", "quantity": "1 lb"},
                {"name": "Olive oil", "category": "Pantry", "quantity": "2 tbsp"},
                {"name": "Garlic", "category": "Produce", "quantity": "4 cloves"},
                {"name": "Parmesan cheese", "category": "Dairy", "quantity": "4oz grated"},
                {"name": "Salt", "category": "Spices", "quantity": "1 tsp"},
                {"name": "Black pepper", "category": "Spices", "quantity": "1/2 tsp"}
            ],
            "chicken curry": [
                {"name": "Chicken breast", "category": "Meat", "quantity": "1 lb"},
                {"name": "Onion", "category": "Produce", "quantity": "1 large"},
                {"name": "Garlic", "category": "Produce", "quantity": "3 cloves"},
                {"name": "Ginger", "category": "Produce", "quantity": "1 inch"},
                {"name": "Curry powder", "category": "Spices", "quantity": "2 tbsp"},
                {"name": "Coconut milk", "category": "Pantry", "quantity": "1 can (13.5oz)"},
                {"name": "Rice", "category": "Pantry", "quantity": "2 cups"},
                {"name": "Cilantro", "category": "Produce", "quantity": "1 bunch"}
            ],
            "salad": [
                {"name": "Mixed greens", "category": "Produce", "quantity": "1 bag (5oz)"},
                {"name": "Cherry tomatoes", "category": "Produce", "quantity": "1 pint"},
                {"name": "Cucumber", "category": "Produce", "quantity": "1 large"},
                {"name": "Red onion", "category": "Produce", "quantity": "1/2 medium"},
                {"name": "Olive oil", "category": "Pantry", "quantity": "2 tbsp"},
                {"name": "Balsamic vinegar", "category": "Pantry", "quantity": "1 tbsp"},
                {"name": "Feta cheese", "category": "Dairy", "quantity": "4oz crumbled"}
            ],
            "tacos": [
                {"name": "Ground beef", "category": "Meat", "quantity": "1 lb"},
                {"name": "Taco seasoning", "category": "Spices", "quantity": "1 packet"},
                {"name": "Tortillas", "category": "Bakery", "quantity": "1 package (10 count)"},
                {"name": "Lettuce", "category": "Produce", "quantity": "1 head"},
                {"name": "Tomatoes", "category": "Produce", "quantity": "2 large"},
                {"name": "Cheese", "category": "Dairy", "quantity": "8oz shredded"},
                {"name": "Sour cream", "category": "Dairy", "quantity": "8oz"}
            ],
            "stir fry": [
                {"name": "Chicken breast", "category": "Meat", "quantity": "1 lb"},
                {"name": "Broccoli", "category": "Produce", "quantity": "1 head"},
                {"name": "Bell peppers", "category": "Produce", "quantity": "2 large"},
                {"name": "Carrots", "category": "Produce", "quantity": "1 lb"},
                {"name": "Garlic", "category": "Produce", "quantity": "4 cloves"},
                {"name": "Ginger", "category": "Produce", "quantity": "1 inch"},
                {"name": "Soy sauce", "category": "Pantry", "quantity": "1/4 cup"},
                {"name": "Rice", "category": "Pantry", "quantity": "2 cups"},
                {"name": "Cooking oil", "category": "Pantry", "quantity": "2 tbsp"}
            ],
            "soup": [
                {"name": "Chicken breast", "category": "Meat", "quantity": "1 lb"},
                {"name": "Carrots", "category": "Produce", "quantity": "1 lb"},
                {"name": "Onion", "category": "Produce", "quantity": "1 large"},
                {"name": "Garlic", "category": "Produce", "quantity": "3 cloves"},
                {"name": "Celery", "category": "Produce", "quantity": "1 bunch"},
                {"name": "Chicken broth", "category": "Pantry", "quantity": "32oz"},
                {"name": "Salt", "category": "Spices", "quantity": "1 tsp"},
                {"name": "Black pepper", "category": "Spices", "quantity": "1/2 tsp"}
            ],
            "sandwich": [
                {"name": "Bread", "category": "Bakery", "quantity": "1 loaf"},
                {"name": "Turkey", "category": "Meat", "quantity": "1 lb"},
                {"name": "Cheese", "category": "Dairy", "quantity": "8oz"},
                {"name": "Lettuce", "category": "Produce", "quantity": "1 head"},
                {"name": "Tomatoes", "category": "Produce", "quantity": "2 large"},
                {"name": "Mayonnaise", "category": "Pantry", "quantity": "8oz"},
                {"name": "Mustard", "category": "Pantry", "quantity": "8oz"}
            ],
            "breakfast": [
                {"name": "Eggs", "category": "Dairy", "quantity": "1 dozen"},
                {"name": "Bacon", "category": "Meat", "quantity": "1 package (12oz)"},
                {"name": "Bread", "category": "Bakery", "quantity": "1 loaf"},
                {"name": "Butter", "category": "Dairy", "quantity": "1 lb"},
                {"name": "Milk", "category": "Dairy", "quantity": "1 gallon"},
                {"name": "Orange juice", "category": "Pantry", "quantity": "64oz"}
            ],
            "barbecue": [
                {"name": "Ground beef", "category": "Meat", "quantity": "2 lb"},
                {"name": "Hamburger buns", "category": "Bakery", "quantity": "1 package (8 count)"},
                {"name": "Cheese", "category": "Dairy", "quantity": "8oz"},
                {"name": "Lettuce", "category": "Produce", "quantity": "1 head"},
                {"name": "Tomatoes", "category": "Produce", "quantity": "2 large"},
                {"name": "Onion", "category": "Produce", "quantity": "1 large"},
                {"name": "Ketchup", "category": "Pantry", "quantity": "20oz"},
                {"name": "Mustard", "category": "Pantry", "quantity": "8oz"}
            ],
            "guacamole": [
                {"name": "Avocados", "category": "Produce", "quantity": "3 large"},
                {"name": "Lime", "category": "Produce", "quantity": "2 medium"},
                {"name": "Red onion", "category": "Produce", "quantity": "1/2 medium"},
                {"name": "Tomatoes", "category": "Produce", "quantity": "2 large"},
                {"name": "Cilantro", "category": "Produce", "quantity": "1 bunch"},
                {"name": "Salt", "category": "Spices", "quantity": "1 tsp"},
                {"name": "Black pepper", "category": "Spices", "quantity": "1/2 tsp"},
                {"name": "Garlic", "category": "Produce", "quantity": "2 cloves"}
            ],
            "guacemole": [
                {"name": "Avocados", "category": "Produce", "quantity": "3 large"},
                {"name": "Lime", "category": "Produce", "quantity": "2 medium"},
                {"name": "Red onion", "category": "Produce", "quantity": "1/2 medium"},
                {"name": "Tomatoes", "category": "Produce", "quantity": "2 large"},
                {"name": "Cilantro", "category": "Produce", "quantity": "1 bunch"},
                {"name": "Salt", "category": "Spices", "quantity": "1 tsp"},
                {"name": "Black pepper", "category": "Spices", "quantity": "1/2 tsp"},
                {"name": "Garlic", "category": "Produce", "quantity": "2 cloves"}
            ],
            "spaghetti carbonara": [
                {"name": "Spaghetti", "category": "Pantry", "quantity": "1 lb"},
                {"name": "Bacon", "category": "Meat", "quantity": "8 oz"},
                {"name": "Eggs", "category": "Dairy", "quantity": "4 large"},
                {"name": "Parmesan cheese", "category": "Dairy", "quantity": "1 cup grated"},
                {"name": "Black pepper", "category": "Spices", "quantity": "1 tsp"},
                {"name": "Salt", "category": "Spices", "quantity": "1 tsp"},
                {"name": "Olive oil", "category": "Pantry", "quantity": "2 tbsp"}
            ],
            "chicken alfredo": [
                {"name": "Fettuccine", "category": "Pantry", "quantity": "1 lb"},
                {"name": "Chicken breast", "category": "Meat", "quantity": "1 lb"},
                {"name": "Heavy cream", "category": "Dairy", "quantity": "1 cup"},
                {"name": "Parmesan cheese", "category": "Dairy", "quantity": "1 cup grated"},
                {"name": "Butter", "category": "Dairy", "quantity": "4 tbsp"},
                {"name": "Garlic", "category": "Produce", "quantity": "4 cloves"},
                {"name": "Black pepper", "category": "Spices", "quantity": "1 tsp"},
                {"name": "Salt", "category": "Spices", "quantity": "1 tsp"}
            ],
            "beef stir fry": [
                {"name": "Beef strips", "category": "Meat", "quantity": "1 lb"},
                {"name": "Broccoli", "category": "Produce", "quantity": "1 head"},
                {"name": "Bell peppers", "category": "Produce", "quantity": "2 large"},
                {"name": "Carrots", "category": "Produce", "quantity": "1 lb"},
                {"name": "Soy sauce", "category": "Pantry", "quantity": "1/4 cup"},
                {"name": "Sesame oil", "category": "Pantry", "quantity": "2 tbsp"},
                {"name": "Garlic", "category": "Produce", "quantity": "4 cloves"},
                {"name": "Ginger", "category": "Produce", "quantity": "1 inch"},
                {"name": "Rice", "category": "Pantry", "quantity": "2 cups"}
            ],
            "fish tacos": [
                {"name": "White fish fillets", "category": "Meat", "quantity": "1 lb"},
                {"name": "Tortillas", "category": "Bakery", "quantity": "1 package (10 count)"},
                {"name": "Cabbage", "category": "Produce", "quantity": "1 small head"},
                {"name": "Lime", "category": "Produce", "quantity": "3 medium"},
                {"name": "Cilantro", "category": "Produce", "quantity": "1 bunch"},
                {"name": "Sour cream", "category": "Dairy", "quantity": "8oz"},
                {"name": "Avocados", "category": "Produce", "quantity": "2 large"},
                {"name": "Olive oil", "category": "Pantry", "quantity": "2 tbsp"}
            ],
            "vegetarian lasagna": [
                {"name": "Lasagna noodles", "category": "Pantry", "quantity": "1 package"},
                {"name": "Ricotta cheese", "category": "Dairy", "quantity": "15oz"},
                {"name": "Mozzarella cheese", "category": "Dairy", "quantity": "16oz shredded"},
                {"name": "Spinach", "category": "Produce", "quantity": "1 bag (10oz)"},
                {"name": "Tomato sauce", "category": "Pantry", "quantity": "1 jar (24oz)"},
                {"name": "Onion", "category": "Produce", "quantity": "1 large"},
                {"name": "Garlic", "category": "Produce", "quantity": "4 cloves"},
                {"name": "Olive oil", "category": "Pantry", "quantity": "2 tbsp"}
            ],
            "chicken soup": [
                {"name": "Chicken breast", "category": "Meat", "quantity": "1 lb"},
                {"name": "Chicken broth", "category": "Pantry", "quantity": "32oz"},
                {"name": "Carrots", "category": "Produce", "quantity": "1 lb"},
                {"name": "Celery", "category": "Produce", "quantity": "1 bunch"},
                {"name": "Onion", "category": "Produce", "quantity": "1 large"},
                {"name": "Garlic", "category": "Produce", "quantity": "3 cloves"},
                {"name": "Rice", "category": "Pantry", "quantity": "1 cup"},
                {"name": "Salt", "category": "Spices", "quantity": "1 tsp"},
                {"name": "Black pepper", "category": "Spices", "quantity": "1/2 tsp"}
            ],
            "beef chili": [
                {"name": "Ground beef", "category": "Meat", "quantity": "1 lb"},
                {"name": "Kidney beans", "category": "Pantry", "quantity": "2 cans (15oz each)"},
                {"name": "Tomato sauce", "category": "Pantry", "quantity": "1 jar (24oz)"},
                {"name": "Onion", "category": "Produce", "quantity": "1 large"},
                {"name": "Bell peppers", "category": "Produce", "quantity": "2 large"},
                {"name": "Garlic", "category": "Produce", "quantity": "4 cloves"},
                {"name": "Chili powder", "category": "Spices", "quantity": "2 tbsp"},
                {"name": "Cumin", "category": "Spices", "quantity": "1 tbsp"},
                {"name": "Salt", "category": "Spices", "quantity": "1 tsp"}
            ],
            "shrimp scampi": [
                {"name": "Shrimp", "category": "Meat", "quantity": "1 lb"},
                {"name": "Linguine", "category": "Pantry", "quantity": "1 lb"},
                {"name": "Butter", "category": "Dairy", "quantity": "4 tbsp"},
                {"name": "Olive oil", "category": "Pantry", "quantity": "2 tbsp"},
                {"name": "Garlic", "category": "Produce", "quantity": "6 cloves"},
                {"name": "Lemon", "category": "Produce", "quantity": "2 medium"},
                {"name": "White wine", "category": "Pantry", "quantity": "1/2 cup"},
                {"name": "Parsley", "category": "Produce", "quantity": "1 bunch"},
                {"name": "Salt", "category": "Spices", "quantity": "1 tsp"},
                {"name": "Black pepper", "category": "Spices", "quantity": "1/2 tsp"}
            ],
            "vegetable stir fry": [
                {"name": "Broccoli", "category": "Produce", "quantity": "1 head"},
                {"name": "Bell peppers", "category": "Produce", "quantity": "2 large"},
                {"name": "Carrots", "category": "Produce", "quantity": "1 lb"},
                {"name": "Snow peas", "category": "Produce", "quantity": "8oz"},
                {"name": "Mushrooms", "category": "Produce", "quantity": "8oz"},
                {"name": "Soy sauce", "category": "Pantry", "quantity": "1/4 cup"},
                {"name": "Sesame oil", "category": "Pantry", "quantity": "2 tbsp"},
                {"name": "Garlic", "category": "Produce", "quantity": "4 cloves"},
                {"name": "Ginger", "category": "Produce", "quantity": "1 inch"},
                {"name": "Rice", "category": "Pantry", "quantity": "2 cups"}
            ],
            "chicken parmesan": [
                {"name": "Chicken breast", "category": "Meat", "quantity": "1 lb"},
                {"name": "Breadcrumbs", "category": "Pantry", "quantity": "1 cup"},
                {"name": "Eggs", "category": "Dairy", "quantity": "2 large"},
                {"name": "Mozzarella cheese", "category": "Dairy", "quantity": "8oz shredded"},
                {"name": "Parmesan cheese", "category": "Dairy", "quantity": "1/2 cup grated"},
                {"name": "Tomato sauce", "category": "Pantry", "quantity": "1 jar (24oz)"},
                {"name": "Spaghetti", "category": "Pantry", "quantity": "1 lb"},
                {"name": "Olive oil", "category": "Pantry", "quantity": "1/4 cup"},
                {"name": "Garlic", "category": "Produce", "quantity": "4 cloves"}
            ],
            "beef tacos": [
                {"name": "Ground beef", "category": "Meat", "quantity": "1 lb"},
                {"name": "Taco seasoning", "category": "Spices", "quantity": "1 packet"},
                {"name": "Tortillas", "category": "Bakery", "quantity": "1 package (10 count)"},
                {"name": "Lettuce", "category": "Produce", "quantity": "1 head"},
                {"name": "Tomatoes", "category": "Produce", "quantity": "2 large"},
                {"name": "Cheese", "category": "Dairy", "quantity": "8oz shredded"},
                {"name": "Sour cream", "category": "Dairy", "quantity": "8oz"},
                {"name": "Onion", "category": "Produce", "quantity": "1 large"}
            ],
            "salmon dinner": [
                {"name": "Salmon fillets", "category": "Meat", "quantity": "1 lb"},
                {"name": "Asparagus", "category": "Produce", "quantity": "1 bunch"},
                {"name": "Lemon", "category": "Produce", "quantity": "2 medium"},
                {"name": "Butter", "category": "Dairy", "quantity": "4 tbsp"},
                {"name": "Garlic", "category": "Produce", "quantity": "4 cloves"},
                {"name": "Rice", "category": "Pantry", "quantity": "2 cups"},
                {"name": "Olive oil", "category": "Pantry", "quantity": "2 tbsp"},
                {"name": "Dill", "category": "Produce", "quantity": "1 bunch"},
                {"name": "Salt", "category": "Spices", "quantity": "1 tsp"},
                {"name": "Black pepper", "category": "Spices", "quantity": "1/2 tsp"}
            ],
            "pasta primavera": [
                {"name": "Penne", "category": "Pantry", "quantity": "1 lb"},
                {"name": "Broccoli", "category": "Produce", "quantity": "1 head"},
                {"name": "Bell peppers", "category": "Produce", "quantity": "2 large"},
                {"name": "Cherry tomatoes", "category": "Produce", "quantity": "1 pint"},
                {"name": "Zucchini", "category": "Produce", "quantity": "2 medium"},
                {"name": "Olive oil", "category": "Pantry", "quantity": "1/4 cup"},
                {"name": "Garlic", "category": "Produce", "quantity": "4 cloves"},
                {"name": "Parmesan cheese", "category": "Dairy", "quantity": "1 cup grated"},
                {"name": "Basil", "category": "Produce", "quantity": "1 bunch"},
                {"name": "Salt", "category": "Spices", "quantity": "1 tsp"},
                {"name": "Black pepper", "category": "Spices", "quantity": "1/2 tsp"}
            ],
            "chicken fajitas": [
                {"name": "Chicken breast", "category": "Meat", "quantity": "1 lb"},
                {"name": "Bell peppers", "category": "Produce", "quantity": "3 large"},
                {"name": "Onion", "category": "Produce", "quantity": "1 large"},
                {"name": "Tortillas", "category": "Bakery", "quantity": "1 package (10 count)"},
                {"name": "Sour cream", "category": "Dairy", "quantity": "8oz"},
                {"name": "Cheese", "category": "Dairy", "quantity": "8oz shredded"},
                {"name": "Lime", "category": "Produce", "quantity": "2 medium"},
                {"name": "Cilantro", "category": "Produce", "quantity": "1 bunch"},
                {"name": "Olive oil", "category": "Pantry", "quantity": "2 tbsp"},
                {"name": "Fajita seasoning", "category": "Spices", "quantity": "1 packet"}
            ],
            "beef stew": [
                {"name": "Beef chuck", "category": "Meat", "quantity": "2 lb"},
                {"name": "Potatoes", "category": "Produce", "quantity": "2 lb"},
                {"name": "Carrots", "category": "Produce", "quantity": "1 lb"},
                {"name": "Onion", "category": "Produce", "quantity": "1 large"},
                {"name": "Beef broth", "category": "Pantry", "quantity": "32oz"},
                {"name": "Tomato paste", "category": "Pantry", "quantity": "6oz"},
                {"name": "Garlic", "category": "Produce", "quantity": "4 cloves"},
                {"name": "Worcestershire sauce", "category": "Pantry", "quantity": "2 tbsp"},
                {"name": "Flour", "category": "Pantry", "quantity": "1/4 cup"},
                {"name": "Olive oil", "category": "Pantry", "quantity": "2 tbsp"},
                {"name": "Salt", "category": "Spices", "quantity": "1 tsp"},
                {"name": "Black pepper", "category": "Spices", "quantity": "1/2 tsp"}
            ],
            "vegetable soup": [
                {"name": "Vegetable broth", "category": "Pantry", "quantity": "32oz"},
                {"name": "Carrots", "category": "Produce", "quantity": "1 lb"},
                {"name": "Celery", "category": "Produce", "quantity": "1 bunch"},
                {"name": "Onion", "category": "Produce", "quantity": "1 large"},
                {"name": "Potatoes", "category": "Produce", "quantity": "1 lb"},
                {"name": "Tomatoes", "category": "Produce", "quantity": "2 large"},
                {"name": "Green beans", "category": "Produce", "quantity": "1 lb"},
                {"name": "Garlic", "category": "Produce", "quantity": "4 cloves"},
                {"name": "Olive oil", "category": "Pantry", "quantity": "2 tbsp"},
                {"name": "Salt", "category": "Spices", "quantity": "1 tsp"},
                {"name": "Black pepper", "category": "Spices", "quantity": "1/2 tsp"},
                {"name": "Italian seasoning", "category": "Spices", "quantity": "1 tbsp"}
            ]
        }
        
        # Try to match the food item to known recipes
        food_lower = food_item.lower()
        for recipe, ingredients in recipe_ingredients.items():
            if recipe in food_lower or any(word in food_lower for word in recipe.split()):
                return ingredients
        
        # Generate generic ingredients for unknown recipes
        return [
            {"name": "Main protein", "category": "Meat", "quantity": "1 lb"},
            {"name": "Vegetables", "category": "Produce", "quantity": "2-3 varieties"},
            {"name": "Starch", "category": "Pantry", "quantity": "2 cups"},
            {"name": "Seasonings", "category": "Spices", "quantity": "as needed"},
            {"name": "Cooking oil", "category": "Pantry", "quantity": "2 tbsp"}
        ]
    
    def _simulate_store_prices(self, ingredient: Dict[str, Any], store: str, price_range: str = "mid-range") -> Dict[str, Any]:
        """Simulate pricing for ingredients at different stores with realistic price ranges."""
        
        # Store-specific pricing multipliers based on real market data
        store_multipliers = {
            "Walmart": {"budget": 0.75, "mid-range": 0.95, "premium": 1.15},
            "Target": {"budget": 0.85, "mid-range": 1.0, "premium": 1.1},
            "Whole Foods": {"budget": 1.4, "mid-range": 1.6, "premium": 1.8},
            "Kroger": {"budget": 0.8, "mid-range": 1.0, "premium": 1.2},
            "Trader Joe's": {"budget": 0.9, "mid-range": 1.05, "premium": 1.15},
            "Aldi": {"budget": 0.65, "mid-range": 0.75, "premium": 0.85}
        }
        
        # Realistic base prices for specific ingredients (2024 market rates)
        ingredient_prices = {
            # Meat & Protein
            "Chicken breast": {"base": 4.99, "category": "Meat", "unit": "lb"},
            "Ground beef": {"base": 5.99, "category": "Meat", "unit": "lb"},
            "Salmon": {"base": 12.99, "category": "Meat", "unit": "lb"},
            "Pork chops": {"base": 6.99, "category": "Meat", "unit": "lb"},
            "Turkey": {"base": 3.99, "category": "Meat", "unit": "lb"},
            "Bacon": {"base": 7.99, "category": "Meat", "unit": "package"},
            "Pepperoni": {"base": 4.99, "category": "Deli", "unit": "package"},
            
            # Produce
            "Onion": {"base": 1.49, "category": "Produce", "unit": "large"},
            "Garlic": {"base": 0.99, "category": "Produce", "unit": "head"},
            "Ginger": {"base": 2.99, "category": "Produce", "unit": "lb"},
            "Tomatoes": {"base": 2.99, "category": "Produce", "unit": "lb"},
            "Lettuce": {"base": 1.99, "category": "Produce", "unit": "head"},
            "Mixed greens": {"base": 3.99, "category": "Produce", "unit": "bag"},
            "Cherry tomatoes": {"base": 3.99, "category": "Produce", "unit": "pint"},
            "Cucumber": {"base": 1.49, "category": "Produce", "unit": "large"},
            "Red onion": {"base": 1.29, "category": "Produce", "unit": "medium"},
            "Cilantro": {"base": 1.99, "category": "Produce", "unit": "bunch"},
            "Bell peppers": {"base": 2.99, "category": "Produce", "unit": "lb"},
            "Carrots": {"base": 1.99, "category": "Produce", "unit": "lb"},
            "Broccoli": {"base": 2.49, "category": "Produce", "unit": "head"},
            "Spinach": {"base": 2.99, "category": "Produce", "unit": "bag"},
            
            # Dairy
            "Mozzarella cheese": {"base": 4.99, "category": "Dairy", "unit": "8oz"},
            "Parmesan cheese": {"base": 5.99, "category": "Dairy", "unit": "8oz"},
            "Cheese": {"base": 4.99, "category": "Dairy", "unit": "8oz"},
            "Feta cheese": {"base": 4.99, "category": "Dairy", "unit": "6oz"},
            "Sour cream": {"base": 2.99, "category": "Dairy", "unit": "16oz"},
            "Milk": {"base": 3.99, "category": "Dairy", "unit": "gallon"},
            "Eggs": {"base": 4.99, "category": "Dairy", "unit": "dozen"},
            "Butter": {"base": 4.99, "category": "Dairy", "unit": "lb"},
            
            # Pantry
            "Spaghetti": {"base": 1.99, "category": "Pantry", "unit": "16oz"},
            "Rice": {"base": 2.99, "category": "Pantry", "unit": "5lb"},
            "Olive oil": {"base": 8.99, "category": "Pantry", "unit": "16oz"},
            "Tomato sauce": {"base": 2.99, "category": "Pantry", "unit": "24oz"},
            "Coconut milk": {"base": 2.99, "category": "Pantry", "unit": "13.5oz"},
            "Pasta": {"base": 1.99, "category": "Pantry", "unit": "16oz"},
            "Bread": {"base": 3.99, "category": "Bakery", "unit": "loaf"},
            "Tortillas": {"base": 2.99, "category": "Bakery", "unit": "package"},
            "Pizza dough": {"base": 3.99, "category": "Bakery", "unit": "package"},
            
            # Spices & Seasonings
            "Salt": {"base": 1.99, "category": "Spices", "unit": "26oz"},
            "Black pepper": {"base": 2.99, "category": "Spices", "unit": "4oz"},
            "Italian seasoning": {"base": 3.99, "category": "Spices", "unit": "2oz"},
            "Curry powder": {"base": 3.99, "category": "Spices", "unit": "2oz"},
            "Taco seasoning": {"base": 1.99, "category": "Spices", "unit": "packet"},
            "Balsamic vinegar": {"base": 4.99, "category": "Pantry", "unit": "8oz"},
            
            # Additional ingredients for more recipes
            "Avocados": {"base": 2.99, "category": "Produce", "unit": "3 large"},
            "Lime": {"base": 0.99, "category": "Produce", "unit": "2 medium"},
            "Celery": {"base": 2.99, "category": "Produce", "unit": "1 bunch"},
            "Hamburger buns": {"base": 3.99, "category": "Bakery", "unit": "8 count"},
            "Mayonnaise": {"base": 3.99, "category": "Pantry", "unit": "16oz"},
            "Mustard": {"base": 2.99, "category": "Pantry", "unit": "8oz"},
            "Ketchup": {"base": 2.99, "category": "Pantry", "unit": "20oz"},
            "Orange juice": {"base": 4.99, "category": "Pantry", "unit": "64oz"},
            "Soy sauce": {"base": 3.99, "category": "Pantry", "unit": "16oz"},
            "Chicken broth": {"base": 2.99, "category": "Pantry", "unit": "32oz"},
            
            # Additional meat and seafood
            "Beef strips": {"base": 8.99, "category": "Meat", "unit": "lb"},
            "Beef chuck": {"base": 6.99, "category": "Meat", "unit": "lb"},
            "White fish fillets": {"base": 9.99, "category": "Meat", "unit": "lb"},
            "Shrimp": {"base": 12.99, "category": "Meat", "unit": "lb"},
            "Salmon fillets": {"base": 12.99, "category": "Meat", "unit": "lb"},
            "Turkey": {"base": 3.99, "category": "Meat", "unit": "lb"},
            
            # Additional produce
            "Asparagus": {"base": 4.99, "category": "Produce", "unit": "1 bunch"},
            "Zucchini": {"base": 2.99, "category": "Produce", "unit": "2 medium"},
            "Snow peas": {"base": 3.99, "category": "Produce", "unit": "8oz"},
            "Mushrooms": {"base": 3.99, "category": "Produce", "unit": "8oz"},
            "Cabbage": {"base": 1.99, "category": "Produce", "unit": "small head"},
            "Green beans": {"base": 2.99, "category": "Produce", "unit": "1 lb"},
            "Potatoes": {"base": 3.99, "category": "Produce", "unit": "5 lb"},
            "Lemon": {"base": 0.99, "category": "Produce", "unit": "2 medium"},
            "Parsley": {"base": 1.99, "category": "Produce", "unit": "1 bunch"},
            "Dill": {"base": 1.99, "category": "Produce", "unit": "1 bunch"},
            "Basil": {"base": 2.99, "category": "Produce", "unit": "1 bunch"},
            
            # Additional dairy
            "Heavy cream": {"base": 3.99, "category": "Dairy", "unit": "16oz"},
            "Ricotta cheese": {"base": 4.99, "category": "Dairy", "unit": "15oz"},
            
            # Additional pantry items
            "Fettuccine": {"base": 2.99, "category": "Pantry", "unit": "16oz"},
            "Linguine": {"base": 2.99, "category": "Pantry", "unit": "16oz"},
            "Penne": {"base": 2.99, "category": "Pantry", "unit": "16oz"},
            "Lasagna noodles": {"base": 3.99, "category": "Pantry", "unit": "1 package"},
            "Breadcrumbs": {"base": 2.99, "category": "Pantry", "unit": "15oz"},
            "Kidney beans": {"base": 1.99, "category": "Pantry", "unit": "15oz can"},
            "Tomato paste": {"base": 1.99, "category": "Pantry", "unit": "6oz"},
            "Beef broth": {"base": 2.99, "category": "Pantry", "unit": "32oz"},
            "Vegetable broth": {"base": 2.99, "category": "Pantry", "unit": "32oz"},
            "Sesame oil": {"base": 4.99, "category": "Pantry", "unit": "8oz"},
            "White wine": {"base": 8.99, "category": "Pantry", "unit": "750ml"},
            "Worcestershire sauce": {"base": 3.99, "category": "Pantry", "unit": "10oz"},
            "Flour": {"base": 2.99, "category": "Pantry", "unit": "5 lb"},
            
            # Additional spices and seasonings
            "Chili powder": {"base": 2.99, "category": "Spices", "unit": "2oz"},
            "Cumin": {"base": 2.99, "category": "Spices", "unit": "2oz"},
            "Fajita seasoning": {"base": 1.99, "category": "Spices", "unit": "1 packet"},
            
            # Generic categories for unknown ingredients
            "Main protein": {"base": 8.99, "category": "Meat", "unit": "lb"},
            "Vegetables": {"base": 3.99, "category": "Produce", "unit": "variety"},
            "Starch": {"base": 2.99, "category": "Pantry", "unit": "2 cups"},
            "Seasonings": {"base": 1.99, "category": "Spices", "unit": "as needed"},
            "Cooking oil": {"base": 4.99, "category": "Pantry", "unit": "16oz"}
        }
        
        # Get the specific ingredient price or use category default
        ingredient_name = ingredient["name"]
        if ingredient_name in ingredient_prices:
            base_price = ingredient_prices[ingredient_name]["base"]
            category = ingredient_prices[ingredient_name]["category"]
        else:
            # Fallback to category-based pricing
            category_defaults = {
                "Meat": 8.99,
                "Produce": 3.99,
                "Dairy": 4.99,
                "Pantry": 2.99,
                "Bakery": 3.99,
                "Deli": 6.99,
                "Spices": 1.99
            }
            base_price = category_defaults.get(ingredient["category"], 3.99)
            category = ingredient["category"]
        
        # Apply store-specific multiplier
        multiplier = store_multipliers.get(store, {"mid-range": 1.0}).get(price_range, 1.0)
        
        # Add realistic price variation (±15%)
        variation = random.uniform(0.85, 1.15)
        
        # Apply seasonal adjustments for produce
        if category == "Produce":
            seasonal_adjustment = random.uniform(0.8, 1.3)  # Seasonal variation
            final_price = round(base_price * multiplier * variation * seasonal_adjustment, 2)
        else:
            final_price = round(base_price * multiplier * variation, 2)
        
        # Ensure minimum price of $0.50
        final_price = max(0.50, final_price)
        
        return {
            "name": ingredient["name"],
            "category": ingredient["category"],
            "quantity": ingredient["quantity"],
            "price": final_price,
            "store": store,
            "location": random.choice(self.grocery_stores[store]["locations"])
        }
    
    def _optimize_shopping_list(self, all_prices: List[Dict[str, Any]], max_stores: int = 3, budget: float = None) -> Dict[str, Any]:
        """Optimize the shopping list to minimize stores and cost."""
        # Group by ingredient
        ingredient_options = {}
        for item in all_prices:
            name = item["name"]
            if name not in ingredient_options:
                ingredient_options[name] = []
            ingredient_options[name].append(item)
        
        # Find the best combination
        best_combination = self._find_best_combination(ingredient_options, max_stores, budget)
        
        # Organize by store
        store_groups = {}
        total_cost = 0
        
        for item in best_combination:
            store = item["store"]
            if store not in store_groups:
                store_groups[store] = []
            store_groups[store].append(item)
            total_cost += item["price"]
        
        return {
            "stores_used": list(store_groups.keys()),
            "total_cost": round(total_cost, 2),
            "shopping_list": store_groups
        }
    
    def _find_best_combination(self, ingredient_options: Dict[str, List[Dict]], max_stores: int, budget: float) -> List[Dict]:
        """Find the best combination of ingredients that balances cost, store variety, and budget utilization."""
        
        def calculate_score(combination, num_stores, total_cost):
            """Calculate a score for a combination (lower is better)."""
            if not combination:
                return float('inf')
            
            # Cost penalty (lower is better)
            cost_penalty = total_cost
            
            # Store variety bonus (more stores = better score, up to max_stores)
            variety_bonus = -30 * min(num_stores, max_stores)  # Negative because lower score is better
            
            # Budget utilization bonus (closer to budget = better, but don't exceed)
            budget_utilization = 0
            if budget:
                if total_cost > budget:
                    budget_utilization = 1000  # Heavy penalty for exceeding budget
                else:
                    # Bonus for using 70-95% of budget
                    utilization_ratio = total_cost / budget
                    if 0.7 <= utilization_ratio <= 0.95:
                        budget_utilization = -80  # Bonus for good utilization
                    elif utilization_ratio < 0.5:
                        budget_utilization = 40  # Penalty for under-utilization
                    elif utilization_ratio > 0.98:
                        budget_utilization = 20  # Small penalty for cutting it too close
            
            return cost_penalty + variety_bonus + budget_utilization
        
        # Generate all possible combinations
        all_combinations = []
        
        # For each ingredient, we can choose from any store
        ingredient_names = list(ingredient_options.keys())
        
        # Generate combinations by trying different store selections
        def generate_combinations(current_combination, ingredient_index):
            if ingredient_index >= len(ingredient_names):
                # We have a complete combination
                if current_combination:
                    stores_used = set(item["store"] for item in current_combination)
                    total_cost = sum(item["price"] for item in current_combination)
                    
                    # Only consider combinations within budget and store limit
                    if total_cost <= budget and len(stores_used) <= max_stores:
                        score = calculate_score(current_combination, len(stores_used), total_cost)
                        all_combinations.append((current_combination.copy(), score))
                return
            
            ingredient_name = ingredient_names[ingredient_index]
            options = ingredient_options[ingredient_name]
            
            # Try each option for this ingredient
            for option in options:
                current_combination.append(option)
                generate_combinations(current_combination, ingredient_index + 1)
                current_combination.pop()
        
        # Generate all combinations
        generate_combinations([], 0)
        
        # If no combinations found, try a simpler approach
        if not all_combinations:
            # Fallback to greedy approach but with store variety preference
            selected_items = []
            used_stores = set()
            
            for ingredient_name, options in ingredient_options.items():
                options.sort(key=lambda x: x["price"])
                
                # Try to pick from stores we're already using
                best_option = None
                for option in options:
                    if option["store"] in used_stores:
                        best_option = option
                        break
                
                # If no existing store has this item, pick the cheapest
                if not best_option:
                    best_option = options[0]
                    used_stores.add(best_option["store"])
                
                # Check budget constraint
                if budget:
                    current_total = sum(item["price"] for item in selected_items) + best_option["price"]
                    if current_total > budget:
                        # Try to find a cheaper alternative
                        for option in options[1:]:
                            current_total = sum(item["price"] for item in selected_items) + option["price"]
                            if current_total <= budget:
                                best_option = option
                                if option["store"] not in used_stores:
                                    used_stores.add(option["store"])
                                break
                        else:
                            continue  # Skip this ingredient if we can't afford it
                
                selected_items.append(best_option)
            
            return selected_items
        
        # Sort by score and return the best combination
        all_combinations.sort(key=lambda x: x[1])
        return all_combinations[0][0] if all_combinations else []
    
    def generate_shopping_list(self, food_item: str, max_stores: int = 3, budget: float = None, price_range: str = "mid-range") -> Dict[str, Any]:
        """Generate an optimized shopping list for the given food item."""
        print(f"🛒 Generating shopping list for: {food_item}")
        
        # Step 1: Generate ingredients needed
        ingredients = self._generate_recipe_ingredients(food_item)
        print(f"📋 Found {len(ingredients)} ingredients needed")
        
        # Step 2: Get prices from all stores
        all_prices = []
        for ingredient in ingredients:
            for store in self.grocery_stores.keys():
                price_info = self._simulate_store_prices(ingredient, store, price_range)
                all_prices.append(price_info)
        
        # Step 3: Optimize the shopping list
        optimized_list = self._optimize_shopping_list(all_prices, max_stores, budget)
        
        return {
            "food_item": food_item,
            "ingredients_needed": ingredients,
            "optimized_shopping": optimized_list,
            "all_store_options": all_prices
        }
    
    def format_shopping_list(self, shopping_data: Dict[str, Any]) -> str:
        """Format the shopping list in a readable way."""
        result = f"\n🛒 SHOPPING LIST FOR: {shopping_data['food_item'].upper()}\n"
        result += "=" * 60 + "\n\n"
        
        optimized = shopping_data["optimized_shopping"]
        
        result += f"📍 Stores to visit: {', '.join(optimized['stores_used'])}\n"
        result += f"💰 Total estimated cost: ${optimized['total_cost']}\n"
        result += f"🏪 Number of stores: {len(optimized['stores_used'])}\n\n"
        
        for store, items in optimized["shopping_list"].items():
            result += f"🏪 {store.upper()}:\n"
            result += "-" * 40 + "\n"
            
            store_total = 0
            for item in items:
                result += f"  • {item['name']} ({item['quantity']}) - ${item['price']}\n"
                store_total += item['price']
            
            result += f"  Store Total: ${round(store_total, 2)}\n\n"
        
        result += "📋 COMPLETE INGREDIENTS LIST:\n"
        result += "-" * 40 + "\n"
        for ingredient in shopping_data["ingredients_needed"]:
            result += f"  • {ingredient['name']} ({ingredient['quantity']}) - {ingredient['category']}\n"
        
        return result
    
    def chat(self, user_message: str) -> str:
        """Chat interface for the grocery agent."""
        self.conversation_history.append({"role": "user", "content": user_message})
        
        response = self._call_llm(self.conversation_history)
        
        if not response:
            return "Sorry, I'm having trouble connecting to the AI model right now."
        
        self.conversation_history.append({
            "role": "assistant", 
            "content": response.content
        })
        return response.content

# Example usage
if __name__ == "__main__":
    agent = GroceryAgent()
    
    print("🛒 Grocery Shopping Agent")
    print("I'll help you find the best prices for recipe ingredients!")
    print("Type 'shop' to generate a shopping list, 'chat' to chat, or 'quit' to exit")
    print("-" * 60)
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'shop':
            food_item = input("What would you like to cook? ")
            max_stores = input("Maximum number of stores to visit (default 3): ")
            max_stores = int(max_stores) if max_stores.isdigit() else 3
            
            budget_input = input("Budget limit (press Enter for no limit): $")
            budget = float(budget_input) if budget_input else None
            
            price_range = input("Price range (budget/mid-range/premium, default mid-range): ")
            if not price_range:
                price_range = "mid-range"
            
            print("\n🔄 Generating shopping list...")
            try:
                shopping_data = agent.generate_shopping_list(food_item, max_stores, budget, price_range)
                formatted_list = agent.format_shopping_list(shopping_data)
                print(formatted_list)
            except Exception as e:
                print(f"Error generating shopping list: {e}")
        elif user_input.lower() == 'chat':
            while True:
                chat_input = input("Chat (type 'back' to return to main menu): ")
                if chat_input.lower() == 'back':
                    break
                try:
                    response = agent.chat(chat_input)
                    print(f"\nAgent: {response}")
                except Exception as e:
                    print(f"Error: {e}")
        else:
            print("Commands: 'shop', 'chat', or 'quit'")
    
    print("Thank you for using the Grocery Shopping Agent!") 