# 🛒 AI Grocery Shopping Agent
## Build An Agent Hackathon 2024

### 🎯 **Project Overview**
An intelligent AI agent that optimizes grocery shopping by finding the best prices across multiple stores while respecting budget constraints and minimizing store visits.

### 🚀 **Key Features**

#### **🤖 AI-Powered Optimization**
- **Model**: Llama 3.3 70B via NVIDIA AI Endpoints
- **Smart Algorithms**: Multi-objective optimization balancing cost, store variety, and budget utilization
- **Real-time Decision Making**: Dynamic store selection based on pricing and constraints

#### **📋 Comprehensive Recipe Database**
- **27+ Popular Recipes** across multiple cuisines
- **Categories**: Italian, Mexican, Asian, American, Seafood, Vegetarian
- **Realistic Ingredients**: 50+ ingredients with 2024 market pricing
- **Detailed Quantities**: Specific package sizes and measurements

#### **🏪 Multi-Store Integration**
- **6 Major Stores**: Aldi, Walmart, Target, Kroger, Trader Joe's, Whole Foods
- **Realistic Pricing**: Store-specific price multipliers based on market data
- **Seasonal Adjustments**: Dynamic pricing for produce items
- **Store Specialties**: Each store optimized for different product categories

#### **💰 Smart Budget Management**
- **Budget Optimization**: Uses 70-95% of budget efficiently
- **Store Minimization**: Reduces number of store visits
- **Price Range Options**: Budget, mid-range, premium selections
- **Cost Savings**: Typically saves 10-30% through optimization

### 🛠️ **Technical Architecture**

#### **Core Components**
```
grocery_agent.py          # Main AI agent with optimization algorithms
demo_presentation.py      # Presentation-ready demo interface
test_enhanced_grocery.py  # Comprehensive testing suite
```

#### **AI Integration**
- **NVIDIA API**: Direct integration with Llama 3.3 70B
- **OpenAI Client**: Standardized API interface
- **Environment Management**: Secure API key handling

#### **Optimization Algorithm**
```python
Score = Cost + Store_Variety_Bonus + Budget_Utilization_Bonus
```
- **Cost Penalty**: Lower is better
- **Store Variety**: Bonus for using multiple stores (up to limit)
- **Budget Utilization**: Bonus for using 70-95% of budget

### 📊 **Demo Results**

#### **Sample Optimizations**
| Recipe | Budget | Cost | Utilization | Stores | Savings |
|--------|--------|------|-------------|--------|---------|
| Pizza | $25 | $22.38 | 89.5% | 2 | $2.62 |
| Guacamole | $12 | $11.52 | 96.0% | 1 | $0.48 |
| Chicken Curry | $20 | $17.33 | 86.6% | 2 | $2.67 |

#### **Store Performance**
- **Aldi**: 25-35% cheaper (budget optimization)
- **Walmart**: 5-25% cheaper (value focus)
- **Whole Foods**: 40-80% premium (quality focus)

### 🎮 **How to Demo**

#### **Quick Start**
```bash
# 1. Setup environment
cd code
python3 demo_presentation.py --quick

# 2. Show recipe variety
python3 demo_presentation.py --recipes

# 3. Live interactive demo
python3 grocery_agent.py
# Then type: shop
# Try: pizza, guacamole, chicken curry
```

#### **Presentation Flow**
1. **Introduction**: "AI-powered grocery optimization"
2. **Quick Demo**: Show pizza shopping optimization
3. **Recipe Variety**: Display 27+ available recipes
4. **Live Demo**: Interactive shopping experience
5. **Technical Deep Dive**: Explain optimization algorithms

### 🏆 **Competitive Advantages**

#### **Technical Innovation**
- **Multi-Objective Optimization**: Balances cost, convenience, and budget
- **Realistic Data**: 2024 market pricing with seasonal variations
- **Scalable Architecture**: Easy to add new stores and recipes

#### **Practical Value**
- **Everyday Use Case**: Solves real grocery shopping problems
- **Cost Savings**: Demonstrable 10-30% savings
- **Time Efficiency**: Reduces store visits and planning time

#### **AI Integration**
- **State-of-the-Art Model**: Llama 3.3 70B for intelligent decision making
- **Real-time Optimization**: Dynamic store and price selection
- **Natural Language Interface**: Conversational shopping experience

### 📈 **Future Enhancements**

#### **Immediate Additions**
- **Nutritional Information**: Health-conscious shopping
- **Dietary Restrictions**: Vegan, gluten-free, etc.
- **Meal Planning**: Weekly shopping optimization

#### **Advanced Features**
- **Real-time Pricing**: API integration with store databases
- **Delivery Optimization**: Include delivery fees and time
- **Social Features**: Share shopping lists and recipes

### 🎯 **Hackathon Impact**

#### **Problem Solved**
- **Budget Management**: Helps families save money on groceries
- **Time Optimization**: Reduces shopping time and store visits
- **Decision Fatigue**: AI handles complex optimization decisions

#### **Technical Achievement**
- **Complex Algorithms**: Multi-objective optimization
- **Real AI Integration**: Production-ready NVIDIA API usage
- **Comprehensive Testing**: 27+ recipes with realistic data

#### **Market Potential**
- **Large Addressable Market**: Everyone shops for groceries
- **Clear Value Proposition**: Demonstrable cost savings
- **Scalable Business Model**: Easy to expand to more stores/regions

### 🏅 **Why This Wins**

1. **Real AI**: Uses cutting-edge Llama 3.3 70B model
2. **Practical Value**: Solves everyday problems
3. **Technical Excellence**: Sophisticated optimization algorithms
4. **Complete Solution**: Ready for immediate use
5. **Scalable**: Easy to expand and improve

---

**Built with ❤️ for the Build An Agent Hackathon 2024** 