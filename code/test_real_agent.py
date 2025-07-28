"""
Test script for the Real Agent with NVIDIA API
"""

from real_agent import RealAgent
import time

def test_agent():
    """Test the real agent with various inputs."""
    print("🧪 Testing Real AI Agent with NVIDIA API")
    print("=" * 50)
    
    try:
        agent = RealAgent()
        print("✅ Agent initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return
    
    test_questions = [
        "Hello! How are you today?",
        "What is 15 * 23?",
        "Can you explain what AI agents are?",
        "Generate a simple Python function",
        "What's the weather like? (just asking, no real weather data)"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n🔍 Test {i}: {question}")
        print("-" * 40)
        
        try:
            start_time = time.time()
            response = agent.chat(question)
            end_time = time.time()
            
            print(f"⏱️  Response time: {end_time - start_time:.2f} seconds")
            print(f"🤖 Agent: {response}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
        time.sleep(1)  # Small delay between requests
    
    print(f"📊 {agent.get_conversation_summary()}")

if __name__ == "__main__":
    test_agent() 