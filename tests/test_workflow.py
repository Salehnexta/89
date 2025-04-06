"""Test the LangGraph workflow."""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.state import AgentState
from app.workflow import compiled_workflow

def test_workflow_basic():
    """Test the workflow with a basic greeting."""
    # Create initial state
    initial_state = AgentState(
        user_input="Hello, I'm planning a trip to Paris"
    )
    
    # Run the workflow
    try:
        result = compiled_workflow.invoke(initial_state)
        
        # Print the result for debugging
        print("\nWorkflow Test Results:")
        print(f"Intent: {result.intent}")
        print(f"Parameters: {result.parameters}")
        print(f"Response: {result.final_response}")
        print(f"History length: {len(result.conversation_history)}")
        
        # Basic assertions
        assert result.intent != ""
        assert len(result.conversation_history) > 0
        assert result.final_response != ""
        
        return True
    except Exception as e:
        print(f"Error testing workflow: {e}")
        return False

if __name__ == "__main__":
    # Check if GOOGLE_API_KEY is set
    if not os.environ.get("GOOGLE_API_KEY"):
        print("\nWARNING: GOOGLE_API_KEY environment variable is not set.")
        print("The test will likely fail without a valid API key.")
        print("Please set the GOOGLE_API_KEY environment variable before running this test.")
    
    # Run the test
    success = test_workflow_basic()
    print(f"\nWorkflow test {'passed' if success else 'failed'}")
