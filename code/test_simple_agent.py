"""
Test script for the Simple Agent
"""

from simple_agent import SimpleAgent

def test_agent():
    """Test the simple agent with various inputs."""
    agent = SimpleAgent()
    
    test_questions = [
        "What is 15 * 23?",
        "Can you search for information about AI agents?",
        "What is the capital of France?",
        "Calculate 2^10",
        "Tell me a joke"
    ]
    
    print("🤖 Testing Simple AI Agent")
    print("=" * 50)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\nTest {i}: {question}")
        print("-" * 30)
        
        try:
            response = agent.chat(question)
            print(f"Agent: {response}")
        except Exception as e:
            print(f"Error: {e}")
        
        print()

if __name__ == "__main__":
    test_agent() 