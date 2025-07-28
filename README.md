# AI Grocery Shopping Agent

Welcome to the **AI Grocery Shopping Agent** - an intelligent web application that optimizes your grocery shopping experience using NVIDIA's Llama 3.3 70B model and advanced AI agents! 🛒🤖

## 🚀 Project Overview

This application demonstrates how **AI agents** can solve real-world problems by combining:
- **Large Language Models** (NVIDIA Llama 3.3 70B)
- **Multi-agent architecture** for complex decision making
- **Web interface** with modern UI/UX
- **Intelligent optimization algorithms** for shopping efficiency

## 🎯 What It Does

The AI Grocery Shopping Agent helps you:
- **Generate optimized shopping lists** for any recipe
- **Find the best prices** across multiple grocery stores
- **Stay within budget** with intelligent cost optimization
- **Minimize store visits** while maximizing savings
- **Get cooking advice** through conversational AI
- **Browse recipes** across multiple cuisines

## 🏪 Supported Stores

- **Walmart** - Budget-friendly, 25-35% cheaper
- **Target** - Convenience, market prices
- **Whole Foods** - Premium/organic, 40-80% premium
- **Kroger** - Traditional grocery, market prices
- **Trader Joe's** - Quality focus, 5-15% premium
- **Aldi** - Budget-friendly, 25-35% cheaper

## 🍽️ Recipe Categories

- **Italian** - Pizza, pasta, carbonara, alfredo, parmesan
- **Mexican** - Tacos, guacamole, fajitas
- **Asian** - Curry, stir fry, sushi
- **American** - BBQ, breakfast, sandwiches
- **Seafood** - Fish tacos, shrimp scampi, salmon
- **Vegetarian** - Salads, lasagna, stir fry

## 🤖 AI Agent Architecture

### Multi-Agent System
1. **Main Orchestrator Agent** - Coordinates all other agents
2. **Recipe Analysis Agent** - Converts food items to ingredient lists
3. **Pricing Intelligence Agent** - Simulates realistic store pricing
4. **Optimization Agent** - Balances cost, convenience, and budget
5. **Budget Validation Agent** - Ensures constraints are met
6. **Conversational Agent** - Provides cooking and shopping advice

### Complex Decision Making
The agents work together to solve optimization problems:
- **Multi-objective optimization** (cost, convenience, quality)
- **Contextual decision making** (seasonal pricing, store specialties)
- **Adaptive reasoning** (handles unknown recipes intelligently)
- **Budget-aware planning** (70-95% optimal utilization)

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **AI Model**: NVIDIA Llama 3.3 70B Instruct
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **AI Framework**: OpenAI API with NVIDIA endpoints
- **Optimization**: Custom algorithms for shopping optimization

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- NVIDIA API key (for AI model access)

### Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd build-an-agent

# Install dependencies
pip3 install -r requirements.txt

# Set up environment variables
# Copy variables.env.example to variables.env and add your NVIDIA_API_KEY
```

### Running the Application
```bash
# Navigate to the code directory
cd code

# Start the Flask application
python3 app.py
```

### Access the Web Interface
Open your browser and go to: **http://localhost:5002**

## 🎮 How to Use

### 1. Generate Shopping Lists
- Enter a recipe (e.g., "pizza", "chicken curry", "guacamole")
- Set your budget and preferences
- Get an optimized shopping list with store recommendations

### 2. Chat with AI
- Ask cooking questions
- Get shopping tips
- Request recipe suggestions

### 3. Browse Recipes
- Explore 27+ pre-defined recipes
- Quick-select popular dishes
- Discover new cuisines

### 4. Compare Stores
- View store pricing strategies
- Learn about store specialties
- Understand price ranges

## 📊 Features

### Intelligent Optimization
- **Multi-store optimization** - Finds best prices across stores
- **Budget management** - Ensures shopping stays within budget
- **Travel efficiency** - Minimizes number of store visits
- **Quality vs cost** - Balances premium vs budget options

### Realistic Pricing
- **2024 market rates** - Based on current grocery prices
- **Store-specific multipliers** - Reflects real pricing strategies
- **Seasonal variations** - Accounts for produce price fluctuations
- **Location-based pricing** - Considers store locations

### User Experience
- **Responsive design** - Works on desktop, tablet, and mobile
- **Real-time processing** - Instant shopping list generation
- **Interactive chat** - Natural language AI assistant
- **Visual feedback** - Loading states and progress indicators

## 🔧 API Endpoints

- `GET /` - Main web interface
- `POST /api/shop` - Generate shopping list
- `POST /api/chat` - AI chat interface
- `GET /api/recipes` - Get available recipes
- `GET /api/stores` - Get store information

## 🧠 AI Agent Capabilities

### Recipe Intelligence
- Converts any food item into detailed ingredient lists
- Handles 27+ predefined recipes + generates for unknown dishes
- Provides realistic quantities and measurements
- Categorizes ingredients (Meat, Produce, Dairy, Pantry, etc.)

### Shopping Optimization
- Balances competing objectives (cost, convenience, quality)
- Uses advanced algorithms for multi-constraint optimization
- Considers store specialties and seasonal pricing
- Adapts to budget constraints and preferences

### Conversational AI
- Natural language understanding for cooking questions
- Contextual responses based on shopping history
- Provides personalized recommendations
- Offers cooking tips and techniques

## 🏆 Project Highlights

- **Real-world application** - Solves actual grocery shopping problems
- **Advanced AI architecture** - Multi-agent system with complex decision making
- **Production-ready** - Web interface with modern UI/UX
- **Scalable design** - Easy to add new stores, recipes, and features
- **Cost-effective** - Uses NVIDIA's competitive API pricing

## 🤝 Contributing

This project was built for the **Build An Agent Hackathon 2024**. Feel free to:
- Add new recipes and ingredients
- Implement additional stores
- Enhance the optimization algorithms
- Improve the user interface
- Add new AI agent capabilities

## 📝 License

Built for educational and demonstration purposes. Feel free to use and modify for your own projects!

---

**Built with ❤️ for the Build An Agent Hackathon 2024**


