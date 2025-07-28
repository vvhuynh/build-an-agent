"""
Simple Document Generation Agent using NVIDIA API

This agent uses the same approach as real_agent.py to avoid LangChain authentication issues.
"""

import json
import os
import asyncio
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv("../variables.env")

class SimpleDocGenAgent:
    def __init__(self):
        """Initialize the document generation agent."""
        self.client = OpenAI(
            api_key=os.environ.get("NVIDIA_API_KEY"),
            base_url="https://integrate.api.nvidia.com/v1"
        )
        self.model_name = "meta/llama-3.3-70b-instruct"
        self.conversation_history = []
        
        print(f"✅ Connected to {self.model_name}")
        print(f"🔑 API Key: {os.environ.get('NVIDIA_API_KEY')[:20]}...")
    
    def _call_llm(self, messages: List[Dict[str, str]], tools: List[Dict] = None):
        """Call the Llama 3.3 70B model."""
        kwargs = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        if tools:
            kwargs["tools"] = tools
        
        try:
            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message
        except Exception as e:
            print(f"❌ Error calling LLM: {e}")
            return None
    
    def _create_simulated_search_results(self, query: str) -> str:
        """Create simulated search results for demonstration."""
        simulated_results = {
            "ai": "Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines. Recent developments include machine learning, neural networks, and deep learning applications across various industries.",
            "machine learning": "Machine learning enables computers to learn from data without explicit programming. Key areas include supervised learning, unsupervised learning, and reinforcement learning.",
            "technology": "Technology continues to evolve rapidly with innovations in quantum computing, blockchain, renewable energy, and artificial intelligence shaping the future.",
            "science": "Scientific research advances in medicine, physics, and environmental science lead to breakthroughs that improve human life and understanding of the universe."
        }
        
        query_lower = query.lower()
        for topic, content in simulated_results.items():
            if topic in query_lower:
                return f"Search results for '{query}': {content}"
        
        return f"Search results for '{query}': This is simulated information about {query}. In a real implementation, this would contain actual search results from the web."
    
    def _define_tools(self) -> List[Dict[str, Any]]:
        """Define the tools this agent can use."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_web",
                    "description": "Search for information on a topic",
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
                    "name": "analyze_topic",
                    "description": "Analyze and summarize information about a topic",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "The topic to analyze"
                            }
                        },
                        "required": ["topic"]
                    }
                }
            }
        ]
    
    def _execute_tool(self, tool_call):
        """Execute a tool call."""
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        if function_name == "search_web":
            query = arguments.get("query", "")
            return self._create_simulated_search_results(query)
        
        elif function_name == "analyze_topic":
            topic = arguments.get("topic", "")
            return f"Analysis of {topic}: This topic involves various aspects and applications. Key points include its importance in modern technology and its potential for future development."
        
        return f"Unknown tool: {function_name}"
    
    async def generate_report(self, topic: str, report_structure: str) -> str:
        """Generate a comprehensive report on the given topic."""
        print(f"📝 Generating report on: {topic}")
        
        # Step 1: Research the topic
        research_prompt = f"""You are a research assistant. Research the topic: {topic}
        
        Provide comprehensive information about this topic including:
        - Key concepts and definitions
        - Current state of the field
        - Important developments and trends
        - Applications and use cases
        - Future prospects
        
        Be thorough and provide detailed information."""
        
        research_messages = [
            {"role": "system", "content": research_prompt},
            {"role": "user", "content": f"Please research {topic} thoroughly."}
        ]
        
        print("🔍 Researching topic...")
        research_response = self._call_llm(research_messages, self._define_tools())
        
        if not research_response:
            return "Error: Could not research the topic."
        
        # Step 2: Create report outline
        outline_prompt = f"""Based on the research about {topic}, create a detailed report outline following this structure:

{report_structure}

The outline should be comprehensive and well-organized."""
        
        outline_messages = [
            {"role": "system", "content": outline_prompt},
            {"role": "user", "content": research_response.content or "Research completed"},
            {"role": "user", "content": f"Create a detailed outline for the {topic} report."}
        ]
        
        print("📋 Creating report outline...")
        outline_response = self._call_llm(outline_messages)
        
        if not outline_response:
            return "Error: Could not create report outline."
        
        # Step 3: Generate the full report
        report_prompt = f"""Write a comprehensive report on {topic} following this outline:

{outline_response.content}

The report should be:
- Well-structured and professional
- Comprehensive and detailed
- Include relevant examples and explanations
- Be suitable for a professional audience

Write the complete report now."""
        
        report_messages = [
            {"role": "system", "content": report_prompt},
            {"role": "user", "content": research_response.content or "Research data available"},
            {"role": "user", "content": "Write the complete report based on the outline and research."}
        ]
        
        print("✍️ Writing full report...")
        report_response = self._call_llm(report_messages)
        
        if not report_response:
            return "Error: Could not generate the report."
        
        return report_response.content
    
    def chat(self, user_message: str) -> str:
        """Simple chat interface for the agent."""
        self.conversation_history.append({"role": "user", "content": user_message})
        
        response = self._call_llm(self.conversation_history, self._define_tools())
        
        if not response:
            return "Sorry, I'm having trouble connecting to the AI model right now."
        
        # Handle tool calls if any
        if hasattr(response, 'tool_calls') and response.tool_calls:
            self.conversation_history.append({
                "role": "assistant",
                "content": None,
                "tool_calls": response.tool_calls
            })
            
            tool_results = []
            for tool_call in response.tool_calls:
                result = self._execute_tool(tool_call)
                tool_results.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "content": result
                })
            
            self.conversation_history.extend(tool_results)
            
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
            self.conversation_history.append({
                "role": "assistant", 
                "content": response.content
            })
            return response.content

# Example usage
if __name__ == "__main__":
    agent = SimpleDocGenAgent()
    
    print("📄 Simple Document Generation Agent")
    print("This agent can generate comprehensive reports on any topic!")
    print("Type 'report' to generate a report, 'chat' to chat, or 'quit' to exit")
    print("-" * 60)
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'report':
            topic = input("Enter topic for report: ")
            structure = input("Enter report structure (or press Enter for default): ")
            if not structure:
                structure = """1. Introduction
2. Background and Context
3. Main Content
4. Analysis and Discussion
5. Conclusion"""
            
            print("\n🔄 Generating report... This may take a few minutes...")
            try:
                report = asyncio.run(agent.generate_report(topic, structure))
                print(f"\n📄 Generated Report:\n{'-'*50}\n{report}\n{'-'*50}")
            except Exception as e:
                print(f"Error generating report: {e}")
        elif user_input.lower() == 'chat':
            while True:
                chat_input = input("Chat (type 'back' to return to main menu): ")
                if chat_input.lower() == 'back':
                    break
                try:
                    response = agent.chat(chat_input)
                    print(f"\nAgent: {response}")
                except Exception as e:
                    print(f"Error: {e}")
        else:
            print("Commands: 'report', 'chat', or 'quit'")
    
    print("Thank you for using the Document Generation Agent!") 