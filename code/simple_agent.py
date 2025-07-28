"""
Simple AI Agent Example

This demonstrates the core components of an AI agent:
1. Model (LLM) - The brain
2. Tools - Actions the agent can take
3. Memory - Context and conversation history
4. Planning - Decision making logic
"""

import json
import os
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv("../variables.env")

class SimpleAgent:
    def __init__(self):
        """Initialize the agent with model and tools."""
        self.client = OpenAI(
            api_key=os.environ.get("NVIDIA_API_KEY"),
            base_url="https://integrate.api.nvidia.com/v1"
        )
        self.model_name = "meta/llama-3.3-70b-instruct"
        self.conversation_history = []
        self.tools = self._define_tools()
    
    def _define_tools(self) -> List[Dict[str, Any]]:
        """Define the tools this agent can use."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_web",
                    "description": "Search the web for current information on a topic",
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
            }
        ]
    
    def _call_llm(self, messages: List[Dict[str, str]], tools: List[Dict] = None):
        """Call the language model."""
        kwargs = {
            "model": self.model_name,
            "messages": messages,
        }
        
        if tools:
            kwargs["tools"] = tools
        
        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message
    
    def _execute_tool(self, tool_call):
        """Execute a tool call."""
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        if function_name == "search_web":
            # Simulate web search
            query = arguments.get("query", "")
            return f"Search results for '{query}': [Simulated search results would appear here]"
        
        elif function_name == "calculate":
            # Simulate calculation
            expression = arguments.get("expression", "")
            try:
                result = eval(expression)  # Note: In production, use safer evaluation
                return f"Calculation result: {expression} = {result}"
            except Exception as e:
                return f"Error calculating {expression}: {str(e)}"
        
        return f"Unknown tool: {function_name}"
    
    def chat(self, user_message: str) -> str:
        """Main chat interface for the agent."""
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Get response from LLM
        response = self._call_llm(self.conversation_history, self.tools)
        
        # Handle tool calls if any
        if hasattr(response, 'tool_calls') and response.tool_calls:
            # Add assistant message with tool calls
            self.conversation_history.append({
                "role": "assistant",
                "content": None,
                "tool_calls": response.tool_calls
            })
            
            # Execute tools
            tool_results = []
            for tool_call in response.tool_calls:
                result = self._execute_tool(tool_call)
                tool_results.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "content": result
                })
            
            # Add tool results to conversation
            self.conversation_history.extend(tool_results)
            
            # Get final response
            final_response = self._call_llm(self.conversation_history)
            self.conversation_history.append({
                "role": "assistant",
                "content": final_response.content
            })
            
            return final_response.content
        else:
            # Simple response without tools
            self.conversation_history.append({
                "role": "assistant", 
                "content": response.content
            })
            return response.content

# Example usage
if __name__ == "__main__":
    agent = SimpleAgent()
    
    print("🤖 Simple AI Agent")
    print("Type 'quit' to exit")
    print("-" * 50)
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            break
            
        try:
            response = agent.chat(user_input)
            print(f"\nAgent: {response}")
        except Exception as e:
            print(f"\nError: {e}") 