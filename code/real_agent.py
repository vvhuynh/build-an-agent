"""
Real AI Agent using NVIDIA API

This agent uses the actual Llama 3.3 70B model via NVIDIA's API to provide real AI responses.
"""

import json
import os
import re
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv("../variables.env")

class RealAgent:
    def __init__(self):
        """Initialize the agent with NVIDIA API connection."""
        self.client = OpenAI(
            api_key=os.environ.get("NVIDIA_API_KEY"),
            base_url="https://integrate.api.nvidia.com/v1"
        )
        self.model_name = "meta/llama-3.3-70b-instruct"
        self.conversation_history = []
        self.tools = self._define_tools()
        
        print(f"✅ Connected to {self.model_name}")
        print(f"🔑 API Key: {os.environ.get('NVIDIA_API_KEY')[:20]}...")
    
    def _define_tools(self) -> List[Dict[str, Any]]:
        """Define the tools this agent can use."""
        return [
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
                                "description": "Mathematical expression to evaluate (e.g., '2 + 2', '15 * 23')"
                            }
                        },
                        "required": ["expression"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_text",
                    "description": "Analyze and summarize text content",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "The text to analyze"
                            },
                            "analysis_type": {
                                "type": "string",
                                "description": "Type of analysis: 'summarize', 'sentiment', 'keywords'",
                                "enum": ["summarize", "sentiment", "keywords"]
                            }
                        },
                        "required": ["text", "analysis_type"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "generate_code",
                    "description": "Generate code examples or solutions",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "language": {
                                "type": "string",
                                "description": "Programming language (e.g., 'python', 'javascript', 'html')"
                            },
                            "task": {
                                "type": "string",
                                "description": "What the code should do"
                            }
                        },
                        "required": ["language", "task"]
                    }
                }
            }
        ]
    
    def _call_llm(self, messages: List[Dict[str, str]], tools: List[Dict] = None):
        """Call the Llama 3.3 70B model."""
        kwargs = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        if tools:
            kwargs["tools"] = tools
        
        try:
            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message
        except Exception as e:
            print(f"❌ Error calling LLM: {e}")
            return None
    
    def _execute_tool(self, tool_call):
        """Execute a tool call."""
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        if function_name == "calculate":
            expression = arguments.get("expression", "")
            try:
                # Safe evaluation - only allow basic math operations
                allowed_chars = set('0123456789+-*/.() ')
                if all(c in allowed_chars for c in expression):
                    result = eval(expression)
                    return f"Calculation result: {expression} = {result}"
                else:
                    return f"Error: Invalid characters in expression '{expression}'"
            except Exception as e:
                return f"Error calculating {expression}: {str(e)}"
        
        elif function_name == "analyze_text":
            text = arguments.get("text", "")
            analysis_type = arguments.get("analysis_type", "summarize")
            
            if analysis_type == "summarize":
                return f"Text Analysis (Summary): The provided text contains {len(text)} characters and appears to be about {text[:100]}..."
            elif analysis_type == "sentiment":
                return f"Text Analysis (Sentiment): The text appears to have a neutral sentiment based on the content provided."
            elif analysis_type == "keywords":
                words = text.split()
                keywords = [word for word in words if len(word) > 4][:5]
                return f"Text Analysis (Keywords): Key terms found: {', '.join(keywords)}"
            else:
                return f"Unknown analysis type: {analysis_type}"
        
        elif function_name == "generate_code":
            language = arguments.get("language", "python")
            task = arguments.get("task", "")
            
            if language.lower() == "python":
                if "hello" in task.lower():
                    return '''```python
print("Hello, World!")
```'''
                elif "function" in task.lower():
                    return '''```python
def example_function():
    """Example function."""
    return "Hello from function!"

# Usage
result = example_function()
print(result)
```'''
                else:
                    return f"```{language}\n# {task}\n# Code would be generated here\n```"
            else:
                return f"```{language}\n// {task}\n// Code would be generated here\n```"
        
        return f"Unknown tool: {function_name}"
    
    def chat(self, user_message: str) -> str:
        """Main chat interface for the agent."""
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Get response from LLM
        response = self._call_llm(self.conversation_history, self.tools)
        
        if not response:
            return "Sorry, I'm having trouble connecting to the AI model right now."
        
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
            if final_response:
                self.conversation_history.append({
                    "role": "assistant",
                    "content": final_response.content
                })
                return final_response.content
            else:
                return "I processed your request with tools, but couldn't generate a final response."
        else:
            # Simple response without tools
            self.conversation_history.append({
                "role": "assistant", 
                "content": response.content
            })
            return response.content
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation."""
        return f"Conversation has {len(self.conversation_history)} messages"

# Example usage
if __name__ == "__main__":
    agent = RealAgent()
    
    print("🤖 Real AI Agent with Llama 3.3 70B")
    print("This agent uses the actual NVIDIA API for real AI responses!")
    print("Try asking complex questions, requesting calculations, or asking for code examples.")
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