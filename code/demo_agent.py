"""
Demo AI Agent - No API Key Required

This demonstrates the core components of an AI agent without requiring external API calls.
Perfect for learning and understanding agent concepts.
"""

import json
import random
from typing import List, Dict, Any

class DemoAgent:
    def __init__(self):
        """Initialize the demo agent with simulated tools."""
        self.conversation_history = []
        self.tools = self._define_tools()
        self.knowledge_base = {
            "weather": {
                "sunny": "It's a beautiful sunny day! Perfect for outdoor activities.",
                "rainy": "It's raining today. Don't forget your umbrella!",
                "cloudy": "It's cloudy but pleasant. Good day for a walk."
            },
            "math": {
                "addition": "I can help with addition! Just give me two numbers.",
                "multiplication": "I can help with multiplication! Just give me two numbers.",
                "division": "I can help with division! Just give me two numbers."
            },
            "greetings": [
                "Hello! How can I help you today?",
                "Hi there! What would you like to know?",
                "Greetings! I'm here to assist you."
            ]
        }
    
    def _define_tools(self) -> List[Dict[str, Any]]:
        """Define the tools this agent can use."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get current weather information for a location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The location to get weather for"
                            }
                        },
                        "required": ["location"]
                    }
                }
            },
            {
                "type": "function", 
                "function": {
                    "name": "calculate",
                    "description": "Perform mathematical calculations",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "Mathematical expression to evaluate"
                            }
                        },
                        "required": ["expression"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_knowledge",
                    "description": "Search for information in the knowledge base",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query"
                            }
                        },
                        "required": ["query"]
                    }
                }
            }
        ]
    
    def _simulate_llm_response(self, user_message: str) -> Dict[str, Any]:
        """Simulate an LLM response that might include tool calls."""
        message_lower = user_message.lower()
        
        # Simulate tool usage based on keywords
        if any(word in message_lower for word in ["weather", "temperature", "forecast"]):
            return {
                "content": None,
                "tool_calls": [{
                    "id": "call_1",
                    "function": {
                        "name": "get_weather",
                        "arguments": json.dumps({"location": "current location"})
                    }
                }]
            }
        elif any(word in message_lower for word in ["calculate", "math", "add", "multiply", "divide"]):
            return {
                "content": None,
                "tool_calls": [{
                    "id": "call_2",
                    "function": {
                        "name": "calculate",
                        "arguments": json.dumps({"expression": "2 + 2"})
                    }
                }]
            }
        elif any(word in message_lower for word in ["search", "find", "information", "about"]):
            return {
                "content": None,
                "tool_calls": [{
                    "id": "call_3",
                    "function": {
                        "name": "search_knowledge",
                        "arguments": json.dumps({"query": user_message})
                    }
                }]
            }
        else:
            # Simple response without tools
            responses = [
                "I understand you're asking about that. Let me help you with that.",
                "That's an interesting question! Here's what I know about that topic.",
                "I'd be happy to help you with that. Let me provide some information.",
                "Great question! Let me share some insights about that.",
                "I can help you with that. Here's what I found."
            ]
            return {
                "content": random.choice(responses),
                "tool_calls": None
            }
    
    def _execute_tool(self, tool_call):
        """Execute a tool call."""
        function_name = tool_call["function"]["name"]
        arguments = json.loads(tool_call["function"]["arguments"])
        
        if function_name == "get_weather":
            location = arguments.get("location", "unknown")
            weather_types = ["sunny", "rainy", "cloudy"]
            weather = random.choice(weather_types)
            return f"Weather in {location}: {weather}. {self.knowledge_base['weather'][weather]}"
        
        elif function_name == "calculate":
            expression = arguments.get("expression", "2 + 2")
            try:
                result = eval(expression)
                return f"Calculation result: {expression} = {result}"
            except Exception as e:
                return f"Error calculating {expression}: {str(e)}"
        
        elif function_name == "search_knowledge":
            query = arguments.get("query", "")
            if "weather" in query.lower():
                return "I found weather information in my knowledge base. Would you like me to get current weather for you?"
            elif "math" in query.lower():
                return "I found mathematical tools in my knowledge base. I can help with calculations!"
            else:
                return f"I searched for '{query}' in my knowledge base. Here's what I found: This is simulated search results for your query."
        
        return f"Unknown tool: {function_name}"
    
    def chat(self, user_message: str) -> str:
        """Main chat interface for the agent."""
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Get simulated response from LLM
        response = self._simulate_llm_response(user_message)
        
        # Handle tool calls if any
        if response.get("tool_calls"):
            # Add assistant message with tool calls
            self.conversation_history.append({
                "role": "assistant",
                "content": None,
                "tool_calls": response["tool_calls"]
            })
            
            # Execute tools
            tool_results = []
            for tool_call in response["tool_calls"]:
                result = self._execute_tool(tool_call)
                tool_results.append({
                    "tool_call_id": tool_call["id"],
                    "role": "tool",
                    "content": result
                })
            
            # Add tool results to conversation
            self.conversation_history.extend(tool_results)
            
            # Get final response
            final_response = self._simulate_llm_response(f"Based on the tool results: {tool_results[0]['content']}")
            self.conversation_history.append({
                "role": "assistant",
                "content": final_response["content"]
            })
            
            return final_response["content"]
        else:
            # Simple response without tools
            self.conversation_history.append({
                "role": "assistant", 
                "content": response["content"]
            })
            return response["content"]
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation."""
        return f"Conversation has {len(self.conversation_history)} messages"

# Example usage
if __name__ == "__main__":
    agent = DemoAgent()
    
    print("🤖 Demo AI Agent (No API Key Required)")
    print("This agent simulates AI responses to demonstrate how agents work!")
    print("Try asking about weather, math, or general questions.")
    print("Type 'quit' to exit")
    print("-" * 60)
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            break
            
        try:
            response = agent.chat(user_input)
            print(f"\nAgent: {response}")
        except Exception as e:
            print(f"\nError: {e}")
    
    print(f"\n{agent.get_conversation_summary()}") 