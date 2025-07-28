#!/usr/bin/env python3
"""
Flask Web Application for AI Grocery Shopping Agent
Frontend interface for the grocery agent
"""

from flask import Flask, render_template, request, jsonify, session
import os
import json
import asyncio
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv("../variables.env")

# Import the grocery agent
from grocery_agent import GroceryAgent

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Initialize the grocery agent
grocery_agent = GroceryAgent()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/shop', methods=['POST'])
def shop():
    """API endpoint for shopping requests"""
    try:
        data = request.get_json()
        food_item = data.get('food_item', '')
        max_stores = int(data.get('max_stores', 3))
        budget = float(data.get('budget', 25)) if data.get('budget') else None
        price_range = data.get('price_range', 'mid-range')
        
        # Generate shopping list
        shopping_data = grocery_agent.generate_shopping_list(
            food_item=food_item,
            max_stores=max_stores,
            budget=budget,
            price_range=price_range
        )
        
        # Format the response
        formatted_list = grocery_agent.format_shopping_list(shopping_data)
        
        return jsonify({
            'success': True,
            'shopping_list': formatted_list,
            'data': shopping_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint for chat requests"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        # Get chat response
        response = grocery_agent.chat(message)
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/recipes')
def get_recipes():
    """API endpoint to get available recipes"""
    recipes = {
        "Italian": ["pizza", "pasta", "spaghetti carbonara", "chicken alfredo", "chicken parmesan"],
        "Mexican": ["tacos", "guacamole", "fish tacos", "beef tacos", "chicken fajitas"],
        "Asian": ["chicken curry", "stir fry", "beef stir fry", "vegetable stir fry"],
        "American": ["barbecue", "breakfast", "sandwich", "beef chili", "beef stew"],
        "Seafood": ["fish tacos", "shrimp scampi", "salmon dinner"],
        "Vegetarian": ["salad", "vegetarian lasagna", "vegetable stir fry", "vegetable soup"]
    }
    
    return jsonify({
        'success': True,
        'recipes': recipes
    })

@app.route('/api/stores')
def get_stores():
    """API endpoint to get store information"""
    stores = {
        "Aldi": "Budget-friendly, 25-35% cheaper",
        "Walmart": "Good value, 5-25% cheaper", 
        "Target": "Convenience, market prices",
        "Kroger": "Traditional grocery, market prices",
        "Trader Joe's": "Quality focus, 5-15% premium",
        "Whole Foods": "Premium/organic, 40-80% premium"
    }
    
    return jsonify({
        'success': True,
        'stores': stores
    })

if __name__ == '__main__':
    print("🚀 Starting AI Grocery Agent Web Interface...")
    print("🌐 Open your browser to: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001) 