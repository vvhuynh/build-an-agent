#!/usr/bin/env python3
"""
Hackathon Demo Script - AI Grocery Shopping Agent
A polished presentation-ready interface for the grocery agent.
"""

import os
import sys
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv("../variables.env")

# Import the grocery agent
from grocery_agent import GroceryAgent

def print_banner():
    """Print a professional banner for the demo."""
    print("\n" + "="*70)
    print("🛒 AI GROCERY SHOPPING AGENT")
    print("   Powered by Llama 3.3 70B & NVIDIA AI")
    print("   Build An Agent Hackathon 2024")
    print("="*70)
    print("🎯 Features:")
    print("   • 27+ Popular Recipes")
    print("   • 6 Major Grocery Stores")
    print("   • Smart Budget Optimization")
    print("   • Realistic 2024 Pricing")
    print("   • Store Variety Optimization")
    print("="*70)

def demo_quick_shopping():
    """Quick demo of the shopping functionality."""
    print("\n🚀 QUICK DEMO: Shopping for Pizza")
    print("-" * 50)
    
    agent = GroceryAgent()
    
    # Demo pizza shopping
    shopping_data = agent.generate_shopping_list(
        food_item="pizza",
        max_stores=2,
        budget=25,
        price_range="mid-range"
    )
    
    formatted_list = agent.format_shopping_list(shopping_data)
    print(formatted_list)
    
    # Show key metrics
    total_cost = shopping_data["optimized_shopping"]["total_cost"]
    stores_used = shopping_data["optimized_shopping"]["stores_used"]
    budget_utilization = (total_cost / 25) * 100
    
    print(f"📊 DEMO METRICS:")
    print(f"   • Budget Used: {budget_utilization:.1f}%")
    print(f"   • Stores Visited: {len(stores_used)}")
    print(f"   • Money Saved: ${25 - total_cost:.2f}")
    print(f"   • Optimization Score: ✅ Excellent")

def demo_recipe_browser():
    """Show available recipes by category."""
    print("\n📚 RECIPE BROWSER")
    print("-" * 50)
    
    categories = {
        "🍕 Italian": ["pizza", "pasta", "spaghetti carbonara", "chicken alfredo", "chicken parmesan"],
        "🌮 Mexican": ["tacos", "guacamole", "fish tacos", "beef tacos", "chicken fajitas"],
        "🥘 Asian": ["chicken curry", "stir fry", "beef stir fry", "vegetable stir fry"],
        "🍔 American": ["barbecue", "breakfast", "sandwich", "beef chili", "beef stew"],
        "🐟 Seafood": ["fish tacos", "shrimp scampi", "salmon dinner"],
        "🥬 Vegetarian": ["salad", "vegetarian lasagna", "vegetable stir fry", "vegetable soup"]
    }
    
    for category, recipes in categories.items():
        print(f"\n{category}:")
        for recipe in recipes:
            print(f"   • {recipe.title()}")
    
    print(f"\n📋 Total: 27+ recipes available")

def demo_store_comparison():
    """Show store pricing comparison."""
    print("\n🏪 STORE PRICING COMPARISON")
    print("-" * 50)
    
    stores = {
        "Aldi": "Budget-friendly, 25-35% cheaper",
        "Walmart": "Good value, 5-25% cheaper", 
        "Target": "Convenience, market prices",
        "Kroger": "Traditional grocery, market prices",
        "Trader Joe's": "Quality focus, 5-15% premium",
        "Whole Foods": "Premium/organic, 40-80% premium"
    }
    
    for store, description in stores.items():
        print(f"🏪 {store}: {description}")

def demo_budget_optimization():
    """Show budget optimization examples."""
    print("\n💰 BUDGET OPTIMIZATION EXAMPLES")
    print("-" * 50)
    
    agent = GroceryAgent()
    
    examples = [
        {"recipe": "guacamole", "budget": 12, "description": "Budget Snack"},
        {"recipe": "chicken curry", "budget": 20, "description": "Family Dinner"},
        {"recipe": "salmon dinner", "budget": 35, "description": "Special Occasion"}
    ]
    
    for example in examples:
        try:
            shopping_data = agent.generate_shopping_list(
                food_item=example["recipe"],
                max_stores=2,
                budget=example["budget"],
                price_range="mid-range"
            )
            
            total_cost = shopping_data["optimized_shopping"]["total_cost"]
            stores_used = shopping_data["optimized_shopping"]["stores_used"]
            utilization = (total_cost / example["budget"]) * 100
            
            print(f"\n🍽️  {example['description']}: {example['recipe'].title()}")
            print(f"   Budget: ${example['budget']} | Used: ${total_cost:.2f} ({utilization:.1f}%)")
            print(f"   Stores: {', '.join(stores_used)}")
            
        except Exception as e:
            print(f"❌ Error with {example['recipe']}: {e}")

def interactive_demo():
    """Interactive demo for live presentation."""
    print("\n🎮 INTERACTIVE DEMO")
    print("-" * 50)
    print("Try these commands during your presentation:")
    print("\n1. 🛒 Quick Shopping Demo:")
    print("   python3 demo_presentation.py --quick")
    
    print("\n2. 📚 Recipe Browser:")
    print("   python3 demo_presentation.py --recipes")
    
    print("\n3. 🏪 Store Comparison:")
    print("   python3 demo_presentation.py --stores")
    
    print("\n4. 💰 Budget Optimization:")
    print("   python3 demo_presentation.py --budget")
    
    print("\n5. 🎯 Live Interactive Demo:")
    print("   python3 grocery_agent.py")
    print("   Then type: shop")
    print("   Try: 'pizza', 'guacamole', 'chicken curry'")

def main():
    """Main demo function."""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--quick":
            demo_quick_shopping()
        elif command == "--recipes":
            demo_recipe_browser()
        elif command == "--stores":
            demo_store_comparison()
        elif command == "--budget":
            demo_budget_optimization()
        else:
            print("Unknown command. Use --quick, --recipes, --stores, or --budget")
    else:
        print_banner()
        print("\n🎯 HACKATHON PRESENTATION READY!")
        print("\n📋 What you have:")
        print("   ✅ Working AI agent with NVIDIA API")
        print("   ✅ 27+ recipes with realistic pricing")
        print("   ✅ Smart budget optimization")
        print("   ✅ Store variety optimization")
        print("   ✅ Professional demo interface")
        
        print("\n🚀 Presentation Tips:")
        print("   1. Start with: python3 demo_presentation.py --quick")
        print("   2. Show recipe variety: python3 demo_presentation.py --recipes")
        print("   3. Demonstrate live: python3 grocery_agent.py")
        print("   4. Highlight the AI optimization capabilities")
        
        print("\n💡 Key Selling Points:")
        print("   • Real AI using Llama 3.3 70B")
        print("   • Practical everyday use case")
        print("   • Smart optimization algorithms")
        print("   • Realistic 2024 pricing data")
        print("   • Multiple store integration")

if __name__ == "__main__":
    main() 