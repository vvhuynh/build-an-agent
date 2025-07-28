#!/usr/bin/env python3
"""
Test script for the enhanced grocery agent with improved store variety and budget utilization.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv("../variables.env")

# Import the grocery agent
from grocery_agent import GroceryAgent

def test_enhanced_grocery_agent():
    """Test the enhanced grocery agent with various scenarios."""
    
    print("🧪 Testing Enhanced Grocery Agent")
    print("=" * 50)
    
    # Initialize the agent
    agent = GroceryAgent()
    
    # Test scenarios
    test_cases = [
        {
            "food": "guacamole",
            "max_stores": 2,
            "budget": 15,
            "description": "Guacamole with 2 stores, $15 budget"
        },
        {
            "food": "pizza",
            "max_stores": 3,
            "budget": 25,
            "description": "Pizza with 3 stores, $25 budget"
        },
        {
            "food": "chicken curry",
            "max_stores": 2,
            "budget": 20,
            "description": "Chicken curry with 2 stores, $20 budget"
        },
        {
            "food": "breakfast",
            "max_stores": 3,
            "budget": 30,
            "description": "Breakfast with 3 stores, $30 budget"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['description']}")
        print("-" * 40)
        
        try:
            # Generate shopping list
            shopping_data = agent.generate_shopping_list(
                food_item=test_case["food"],
                max_stores=test_case["max_stores"],
                budget=test_case["budget"],
                price_range="mid-range"
            )
            
            # Format and display results
            formatted_list = agent.format_shopping_list(shopping_data)
            print(formatted_list)
            
            # Show budget utilization
            total_cost = shopping_data["optimized_shopping"]["total_cost"]
            budget = test_case["budget"]
            utilization = (total_cost / budget) * 100 if budget else 0
            stores_used = len(shopping_data["optimized_shopping"]["stores_used"])
            
            print(f"📊 Budget Utilization: {utilization:.1f}%")
            print(f"🏪 Stores Used: {stores_used}/{test_case['max_stores']}")
            
            if utilization < 50:
                print("⚠️  Low budget utilization - consider higher budget or more stores")
            elif utilization > 95:
                print("⚠️  Very high budget utilization - cutting it close!")
            else:
                print("✅ Good budget utilization!")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "="*50)

def test_store_variety():
    """Test specifically for store variety improvements."""
    
    print("\n🏪 Testing Store Variety Improvements")
    print("=" * 50)
    
    agent = GroceryAgent()
    
    # Test with different store limits
    food_item = "pizza"
    budget = 30
    
    for max_stores in [1, 2, 3]:
        print(f"\n🔍 Testing with max {max_stores} store(s), budget ${budget}")
        print("-" * 40)
        
        try:
            shopping_data = agent.generate_shopping_list(
                food_item=food_item,
                max_stores=max_stores,
                budget=budget,
                price_range="mid-range"
            )
            
            stores_used = shopping_data["optimized_shopping"]["stores_used"]
            total_cost = shopping_data["optimized_shopping"]["total_cost"]
            
            print(f"📍 Stores used: {', '.join(stores_used)}")
            print(f"💰 Total cost: ${total_cost}")
            print(f"📊 Budget utilization: {(total_cost/budget)*100:.1f}%")
            
            if len(stores_used) > 1:
                print("✅ Multiple stores used - variety achieved!")
            else:
                print("ℹ️  Single store used - cost optimization prioritized")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_enhanced_grocery_agent()
    test_store_variety()
    print("\n🎉 Enhanced grocery agent testing complete!") 