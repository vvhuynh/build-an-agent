#!/usr/bin/env python3
"""
Comprehensive test script for the enhanced grocery agent with expanded recipe database.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv("../variables.env")

# Import the grocery agent
from grocery_agent import GroceryAgent

def test_all_recipes():
    """Test all available recipes in the grocery agent."""
    
    print("🍽️  Testing All Available Recipes")
    print("=" * 60)
    
    # Initialize the agent
    agent = GroceryAgent()
    
    # All available recipes
    recipes = [
        {"name": "pizza", "budget": 25, "max_stores": 2},
        {"name": "pasta", "budget": 20, "max_stores": 2},
        {"name": "chicken curry", "budget": 20, "max_stores": 2},
        {"name": "salad", "budget": 15, "max_stores": 2},
        {"name": "tacos", "budget": 18, "max_stores": 2},
        {"name": "stir fry", "budget": 22, "max_stores": 2},
        {"name": "soup", "budget": 18, "max_stores": 2},
        {"name": "sandwich", "budget": 15, "max_stores": 2},
        {"name": "breakfast", "budget": 25, "max_stores": 2},
        {"name": "barbecue", "budget": 30, "max_stores": 2},
        {"name": "guacamole", "budget": 12, "max_stores": 2},
        {"name": "spaghetti carbonara", "budget": 20, "max_stores": 2},
        {"name": "chicken alfredo", "budget": 25, "max_stores": 2},
        {"name": "beef stir fry", "budget": 25, "max_stores": 2},
        {"name": "fish tacos", "budget": 22, "max_stores": 2},
        {"name": "vegetarian lasagna", "budget": 28, "max_stores": 2},
        {"name": "chicken soup", "budget": 18, "max_stores": 2},
        {"name": "beef chili", "budget": 20, "max_stores": 2},
        {"name": "shrimp scampi", "budget": 30, "max_stores": 2},
        {"name": "vegetable stir fry", "budget": 18, "max_stores": 2},
        {"name": "chicken parmesan", "budget": 25, "max_stores": 2},
        {"name": "beef tacos", "budget": 20, "max_stores": 2},
        {"name": "salmon dinner", "budget": 35, "max_stores": 2},
        {"name": "pasta primavera", "budget": 22, "max_stores": 2},
        {"name": "chicken fajitas", "budget": 22, "max_stores": 2},
        {"name": "beef stew", "budget": 30, "max_stores": 2},
        {"name": "vegetable soup", "budget": 15, "max_stores": 2}
    ]
    
    print(f"📋 Total recipes available: {len(recipes)}")
    print("\n" + "="*60)
    
    # Test each recipe
    for i, recipe in enumerate(recipes, 1):
        print(f"\n🍳 Recipe {i:2d}: {recipe['name'].upper()}")
        print("-" * 40)
        
        try:
            # Generate shopping list
            shopping_data = agent.generate_shopping_list(
                food_item=recipe["name"],
                max_stores=recipe["max_stores"],
                budget=recipe["budget"],
                price_range="mid-range"
            )
            
            # Get key metrics
            total_cost = shopping_data["optimized_shopping"]["total_cost"]
            stores_used = shopping_data["optimized_shopping"]["stores_used"]
            num_ingredients = len(shopping_data["ingredients_needed"])
            budget_utilization = (total_cost / recipe["budget"]) * 100
            
            # Display summary
            print(f"💰 Cost: ${total_cost:.2f} / ${recipe['budget']} ({budget_utilization:.1f}%)")
            print(f"🏪 Stores: {', '.join(stores_used)} ({len(stores_used)} stores)")
            print(f"📦 Ingredients: {num_ingredients} items")
            
            # Show store breakdown
            for store, items in shopping_data["optimized_shopping"]["shopping_list"].items():
                store_total = sum(item["price"] for item in items)
                print(f"  • {store}: ${store_total:.2f} ({len(items)} items)")
            
            # Budget utilization indicator
            if budget_utilization < 60:
                print("⚠️  Low budget utilization")
            elif budget_utilization > 95:
                print("⚠️  High budget utilization")
            else:
                print("✅ Good budget utilization")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()

def test_recipe_categories():
    """Test recipes by category to show variety."""
    
    print("\n📊 Recipe Categories Analysis")
    print("=" * 60)
    
    agent = GroceryAgent()
    
    categories = {
        "Italian": ["pizza", "pasta", "spaghetti carbonara", "chicken alfredo", "chicken parmesan", "pasta primavera"],
        "Mexican": ["tacos", "guacamole", "fish tacos", "beef tacos", "chicken fajitas"],
        "Asian": ["chicken curry", "stir fry", "beef stir fry", "vegetable stir fry"],
        "American": ["barbecue", "breakfast", "sandwich", "beef chili", "beef stew"],
        "Seafood": ["fish tacos", "shrimp scampi", "salmon dinner"],
        "Vegetarian": ["salad", "vegetarian lasagna", "vegetable stir fry", "vegetable soup"],
        "Soups": ["soup", "chicken soup", "beef chili", "vegetable soup", "beef stew"]
    }
    
    for category, recipes in categories.items():
        print(f"\n🍽️  {category.upper()} RECIPES ({len(recipes)} recipes):")
        print("-" * 40)
        
        total_cost = 0
        total_budget = 0
        
        for recipe in recipes:
            try:
                shopping_data = agent.generate_shopping_list(
                    food_item=recipe,
                    max_stores=2,
                    budget=25,  # Standard budget for comparison
                    price_range="mid-range"
                )
                
                cost = shopping_data["optimized_shopping"]["total_cost"]
                total_cost += cost
                total_budget += 25
                
                print(f"  • {recipe}: ${cost:.2f}")
                
            except Exception as e:
                print(f"  • {recipe}: Error")
        
        if total_budget > 0:
            avg_cost = total_cost / len(recipes)
            print(f"  📊 Average cost: ${avg_cost:.2f}")

def test_ingredient_variety():
    """Test to show the variety of ingredients available."""
    
    print("\n🥬 Ingredient Variety Analysis")
    print("=" * 60)
    
    agent = GroceryAgent()
    
    # Test a few complex recipes to show ingredient variety
    complex_recipes = ["vegetarian lasagna", "beef stew", "shrimp scampi", "salmon dinner"]
    
    all_ingredients = set()
    category_counts = {}
    
    for recipe in complex_recipes:
        try:
            shopping_data = agent.generate_shopping_list(
                food_item=recipe,
                max_stores=2,
                budget=30,
                price_range="mid-range"
            )
            
            print(f"\n🍳 {recipe.upper()}:")
            print("-" * 30)
            
            for ingredient in shopping_data["ingredients_needed"]:
                name = ingredient["name"]
                category = ingredient["category"]
                all_ingredients.add(name)
                
                if category not in category_counts:
                    category_counts[category] = 0
                category_counts[category] += 1
                
                print(f"  • {name} ({category})")
                
        except Exception as e:
            print(f"❌ Error with {recipe}: {e}")
    
    print(f"\n📊 Total unique ingredients: {len(all_ingredients)}")
    print("📊 Ingredients by category:")
    for category, count in sorted(category_counts.items()):
        print(f"  • {category}: {count} items")

if __name__ == "__main__":
    test_all_recipes()
    test_recipe_categories()
    test_ingredient_variety()
    print("\n🎉 Comprehensive recipe testing complete!")
    print(f"\n💡 You can now ask the grocery agent for any of these {len(recipes)} recipes!") 