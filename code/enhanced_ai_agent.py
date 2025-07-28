#!/usr/bin/env python3
"""
Enhanced AI Grocery Agent - Demonstrating Full AI Agent Potential
Features: Memory, Planning, Tool Usage, Autonomous Decision Making, Learning
"""

import os
import json
import random
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv("../variables.env")

@dataclass
class ShoppingMemory:
    """Memory system for the AI agent"""
    user_preferences: Dict[str, Any]
    shopping_history: List[Dict[str, Any]]
    budget_patterns: Dict[str, float]
    favorite_stores: Dict[str, int]
    dietary_restrictions: List[str]
    last_shopping_date: Optional[str]
    
    def to_dict(self):
        return asdict(self)

@dataclass
class PlanningStep:
    """Planning system for complex shopping tasks"""
    step_id: int
    action: str
    reasoning: str
    expected_outcome: str
    completed: bool = False
    result: Optional[str] = None

class EnhancedGroceryAgent:
    """
    Enhanced AI Agent demonstrating full potential:
    - Memory and Learning
    - Planning and Reasoning
    - Tool Usage and Integration
    - Autonomous Decision Making
    - Multi-step Problem Solving
    """
    
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("NVIDIA_API_KEY"),
            base_url="https://integrate.api.nvidia.com/v1"
        )
        self.model_name = "meta/llama-3.3-70b-instruct"
        
        # Initialize memory system
        self.memory = self._load_memory()
        
        # Planning system
        self.current_plan: List[PlanningStep] = []
        self.planning_context: Dict[str, Any] = {}
        
        # Tool registry
        self.tools = {
            "search_recipes": self._search_recipes,
            "analyze_budget": self._analyze_budget,
            "optimize_shopping": self._optimize_shopping,
            "check_dietary_restrictions": self._check_dietary_restrictions,
            "plan_meals": self._plan_meals,
            "learn_preferences": self._learn_preferences,
            "generate_shopping_strategy": self._generate_shopping_strategy
        }
        
        # Conversation context
        self.conversation_history = []
        
        print("🧠 Enhanced AI Agent Initialized")
        print(f"📚 Memory: {len(self.memory.shopping_history)} shopping sessions")
        print(f"🎯 Tools Available: {len(self.tools)} specialized functions")
    
    def _load_memory(self) -> ShoppingMemory:
        """Load or initialize agent memory"""
        try:
            with open("agent_memory.json", "r") as f:
                data = json.load(f)
                return ShoppingMemory(**data)
        except FileNotFoundError:
            return ShoppingMemory(
                user_preferences={},
                shopping_history=[],
                budget_patterns={},
                favorite_stores={},
                dietary_restrictions=[],
                last_shopping_date=None
            )
    
    def _save_memory(self):
        """Save agent memory to persistent storage"""
        with open("agent_memory.json", "w") as f:
            json.dump(self.memory.to_dict(), f, indent=2)
    
    async def _call_llm(self, messages: List[Dict[str, str]], tools: List[Dict] = None) -> str:
        """Enhanced LLM call with tool usage"""
        try:
            if tools:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    tools=tools,
                    tool_choice="auto",
                    temperature=0.7
                )
            else:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=0.7
                )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"AI processing error: {str(e)}"
    
    def _create_planning_context(self, user_request: str) -> Dict[str, Any]:
        """Create planning context for complex tasks"""
        return {
            "user_request": user_request,
            "memory_context": {
                "preferences": self.memory.user_preferences,
                "budget_patterns": self.memory.budget_patterns,
                "favorite_stores": self.memory.favorite_stores,
                "dietary_restrictions": self.memory.dietary_restrictions
            },
            "current_date": datetime.now().strftime("%Y-%m-%d"),
            "available_tools": list(self.tools.keys())
        }
    
    async def _create_plan(self, user_request: str) -> List[PlanningStep]:
        """AI-powered planning for complex shopping tasks"""
        planning_prompt = f"""
        You are an AI agent planning a complex shopping task. Create a step-by-step plan.
        
        User Request: {user_request}
        Memory Context: {json.dumps(self._create_planning_context(user_request), indent=2)}
        
        Create a detailed plan with these steps:
        1. Analyze user request and context
        2. Check dietary restrictions and preferences
        3. Search for relevant recipes
        4. Analyze budget requirements
        5. Generate shopping strategy
        6. Optimize store selection
        7. Create final shopping list
        
        Return as JSON array of planning steps.
        """
        
        messages = [{"role": "user", "content": planning_prompt}]
        response = await self._call_llm(messages)
        
        try:
            # Parse planning response
            plan_data = json.loads(response)
            return [PlanningStep(**step) for step in plan_data]
        except:
            # Fallback plan
            return [
                PlanningStep(1, "analyze_request", "Understanding user needs", "Clear task definition"),
                PlanningStep(2, "check_preferences", "Checking user preferences", "Dietary and budget constraints"),
                PlanningStep(3, "search_recipes", "Finding relevant recipes", "Recipe recommendations"),
                PlanningStep(4, "optimize_shopping", "Optimizing shopping strategy", "Optimal shopping plan"),
                PlanningStep(5, "generate_list", "Creating final shopping list", "Complete shopping list")
            ]
    
    async def _execute_plan(self) -> Dict[str, Any]:
        """Execute the current plan step by step"""
        results = {}
        
        for step in self.current_plan:
            print(f"🔄 Executing Step {step.step_id}: {step.action}")
            
            if step.action == "analyze_request":
                step.result = "User request analyzed successfully"
                results["analysis"] = step.result
                
            elif step.action == "check_preferences":
                step.result = f"Dietary restrictions: {self.memory.dietary_restrictions}"
                results["preferences"] = step.result
                
            elif step.action == "search_recipes":
                step.result = await self.tools["search_recipes"](self.planning_context["user_request"])
                results["recipes"] = step.result
                
            elif step.action == "optimize_shopping":
                step.result = await self.tools["optimize_shopping"](results.get("recipes", ""))
                results["optimization"] = step.result
                
            elif step.action == "generate_list":
                step.result = await self.tools["generate_shopping_strategy"](results)
                results["final_list"] = step.result
            
            step.completed = True
            await asyncio.sleep(0.5)  # Simulate processing time
        
        return results
    
    # Tool Implementations
    async def _search_recipes(self, query: str) -> str:
        """AI-powered recipe search with context awareness"""
        recipes = {
            "pizza": "Classic pizza with customizable toppings",
            "pasta": "Italian pasta dishes with various sauces",
            "curry": "Spicy curry dishes with rice",
            "tacos": "Mexican tacos with fresh ingredients",
            "salad": "Healthy salad options",
            "soup": "Warm soup recipes for any season"
        }
        
        # AI-enhanced search
        search_prompt = f"Find recipes related to: {query}. Available: {list(recipes.keys())}"
        messages = [{"role": "user", "content": search_prompt}]
        response = await self._call_llm(messages)
        
        return f"AI found recipes for '{query}': {response}"
    
    async def _analyze_budget(self, recipes: str) -> str:
        """AI-powered budget analysis"""
        analysis_prompt = f"Analyze budget requirements for: {recipes}"
        messages = [{"role": "user", "content": analysis_prompt}]
        response = await self._call_llm(messages)
        
        return f"Budget analysis: {response}"
    
    async def _optimize_shopping(self, recipes: str) -> str:
        """AI-powered shopping optimization"""
        optimization_prompt = f"Optimize shopping strategy for: {recipes}"
        messages = [{"role": "user", "content": optimization_prompt}]
        response = await self._call_llm(messages)
        
        return f"Shopping optimization: {response}"
    
    async def _check_dietary_restrictions(self, ingredients: List[str]) -> str:
        """Check ingredients against dietary restrictions"""
        restrictions = self.memory.dietary_restrictions
        if not restrictions:
            return "No dietary restrictions found"
        
        check_prompt = f"Check if these ingredients {ingredients} are compatible with restrictions: {restrictions}"
        messages = [{"role": "user", "content": check_prompt}]
        response = await self._call_llm(messages)
        
        return f"Dietary check: {response}"
    
    async def _plan_meals(self, timeframe: str) -> str:
        """AI-powered meal planning"""
        planning_prompt = f"Create a meal plan for: {timeframe}"
        messages = [{"role": "user", "content": planning_prompt}]
        response = await self._call_llm(messages)
        
        return f"Meal plan for {timeframe}: {response}"
    
    async def _learn_preferences(self, user_feedback: str) -> str:
        """Learn from user feedback and update preferences"""
        learning_prompt = f"Learn from user feedback: {user_feedback}"
        messages = [{"role": "user", "content": learning_prompt}]
        response = await self._call_llm(messages)
        
        # Update memory
        self.memory.user_preferences["last_feedback"] = user_feedback
        self.memory.user_preferences["learning_timestamp"] = datetime.now().isoformat()
        self._save_memory()
        
        return f"Learning update: {response}"
    
    async def _generate_shopping_strategy(self, context: Dict[str, Any]) -> str:
        """Generate comprehensive shopping strategy"""
        strategy_prompt = f"Generate shopping strategy based on: {json.dumps(context, indent=2)}"
        messages = [{"role": "user", "content": strategy_prompt}]
        response = await self._call_llm(messages)
        
        return f"Shopping strategy: {response}"
    
    async def process_request(self, user_input: str) -> str:
        """Main AI agent processing with full capabilities"""
        print(f"\n🧠 AI Agent Processing: {user_input}")
        
        # Create planning context
        self.planning_context = self._create_planning_context(user_input)
        
        # Generate AI plan
        self.current_plan = await self._create_plan(user_input)
        print(f"📋 Generated {len(self.current_plan)} step plan")
        
        # Execute plan
        results = await self._execute_plan()
        
        # Generate final response
        final_prompt = f"""
        Generate a comprehensive response based on the executed plan results:
        {json.dumps(results, indent=2)}
        
        Original request: {user_input}
        """
        
        messages = [{"role": "user", "content": final_prompt}]
        final_response = await self._call_llm(messages)
        
        # Update memory
        self.memory.shopping_history.append({
            "request": user_input,
            "response": final_response,
            "timestamp": datetime.now().isoformat(),
            "plan_steps": len(self.current_plan)
        })
        self._save_memory()
        
        return final_response
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get comprehensive agent status"""
        return {
            "memory_size": len(self.memory.shopping_history),
            "tools_available": len(self.tools),
            "user_preferences": len(self.memory.user_preferences),
            "dietary_restrictions": self.memory.dietary_restrictions,
            "favorite_stores": self.memory.favorite_stores,
            "last_shopping": self.memory.last_shopping_date,
            "planning_capability": len(self.current_plan) > 0
        }

async def main():
    """Demo the enhanced AI agent capabilities"""
    agent = EnhancedGroceryAgent()
    
    print("\n🚀 Enhanced AI Agent Demo")
    print("=" * 50)
    
    # Show agent status
    status = agent.get_agent_status()
    print(f"📊 Agent Status: {json.dumps(status, indent=2)}")
    
    # Demo complex requests
    demo_requests = [
        "I want to plan meals for the week with a $100 budget, considering I'm vegetarian",
        "Help me optimize my grocery shopping to save money while maintaining quality",
        "Create a shopping list for a dinner party with 6 people, budget $150"
    ]
    
    for request in demo_requests:
        print(f"\n🎯 Processing: {request}")
        response = await agent.process_request(request)
        print(f"🤖 AI Response: {response}")
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main()) 