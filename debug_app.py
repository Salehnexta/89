"""
Debug script for the AI Travel Assistant application.

This script uses Python's built-in debugger (pdb) to step through the application
and identify any issues with the DeepSeek API integration.
"""
import os
import sys
import pdb
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.state import AgentState
from app.workflow import compiled_workflow
from app.language_model import get_language_model
from app.config import validate_config, DEEPSEEK_API_KEY, GOOGLE_API_KEY
from app.nodes import intent_classifier, draft_manager, response_generator

def debug_config():
    """Debug configuration settings."""
    print("\n=== Debugging Configuration ===")
    # Check if API keys are loaded
    print(f"DeepSeek API Key present: {bool(DEEPSEEK_API_KEY)}")
    print(f"Google API Key present: {bool(GOOGLE_API_KEY)}")
    
    # Validate configuration
    validation_result = validate_config()
    print(f"Configuration validation: {validation_result}")
    
    return validation_result

def debug_language_model():
    """Debug language model initialization."""
    print("\n=== Debugging Language Model ===")
    try:
        # Get language model
        model = get_language_model()
        model_type = type(model).__name__
        print(f"Language model type: {model_type}")
        
        # Test simple completion
        test_prompt = "Hello, how are you?"
        print(f"Testing simple prompt: '{test_prompt}'")
        
        from langchain.schema.messages import HumanMessage
        messages = [HumanMessage(content=test_prompt)]
        
        response = model.invoke(messages)
        print(f"Response type: {type(response)}")
        print(f"Response content: {response.content[:100]}...")
        
        return True
    except Exception as e:
        print(f"Error in language model: {str(e)}")
        return False

def debug_intent_classification():
    """Debug intent classification."""
    print("\n=== Debugging Intent Classification ===")
    try:
        # Create a test state
        state = AgentState()
        state.user_input = "I want to plan a trip to Paris in June"
        
        # Run intent classification
        print(f"Input: '{state.user_input}'")
        result_state = intent_classifier(state)
        
        print(f"Detected intent: {result_state.intent}")
        print(f"Extracted parameters: {json.dumps(result_state.parameters, indent=2)}")
        
        return True
    except Exception as e:
        print(f"Error in intent classification: {str(e)}")
        return False

def debug_draft_manager():
    """Debug draft manager."""
    print("\n=== Debugging Draft Manager ===")
    try:
        # Create a test state with parameters
        state = AgentState()
        state.intent = "start_draft"
        state.parameters = {
            "destination": "Paris",
            "dates": {"start": "2025-06-15", "end": "2025-06-22"},
            "travelers": 2,
            "preferences": ["art", "food"]
        }
        
        # Run draft manager
        print(f"Input parameters: {json.dumps(state.parameters, indent=2)}")
        result_state = draft_manager(state)
        
        print(f"Updated draft package: {json.dumps(result_state.draft_package, indent=2)}")
        
        return True
    except Exception as e:
        print(f"Error in draft manager: {str(e)}")
        return False

def debug_response_generator():
    """Debug response generator."""
    print("\n=== Debugging Response Generator ===")
    try:
        # Create a test state
        state = AgentState()
        state.intent = "general_info"
        state.user_input = "What are the best times to visit museums in Paris?"
        state.parameters = {
            "topic": "museums",
            "destination": "Paris",
            "info_result": "Most museums in Paris are less crowded on weekdays, especially in the morning."
        }
        
        # Run response generator
        print(f"Input: '{state.user_input}'")
        result_state = response_generator(state)
        
        print(f"Generated response: {result_state.final_response[:100]}...")
        
        return True
    except Exception as e:
        print(f"Error in response generator: {str(e)}")
        return False

def debug_workflow():
    """Debug the entire workflow."""
    print("\n=== Debugging Complete Workflow ===")
    try:
        # Create a test state
        state = AgentState()
        state.user_input = "I want to plan a trip to Paris in June"
        
        # Run the workflow
        print(f"Input: '{state.user_input}'")
        result_state = compiled_workflow.invoke(state)
        
        # Check the result type
        print(f"Result state type: {type(result_state)}")
        
        # Extract and print the response
        if hasattr(result_state, 'final_response'):
            response = result_state.final_response
        elif isinstance(result_state, dict) and 'final_response' in result_state:
            response = result_state['final_response']
        else:
            response = "Could not extract response"
        
        print(f"Generated response: {response[:100]}...")
        
        return True
    except Exception as e:
        print(f"Error in workflow: {str(e)}")
        return False

def main():
    """Main debug function."""
    print("Starting AI Travel Assistant Debugging")
    
    # Debug each component
    config_ok = debug_config()
    if not config_ok:
        print("Configuration validation failed. Please check your .env file.")
        return
    
    model_ok = debug_language_model()
    if not model_ok:
        print("Language model initialization failed. Please check your API keys.")
        return
    
    intent_ok = debug_intent_classification()
    if not intent_ok:
        print("Intent classification failed. Please check the intent_classifier function.")
        return
    
    draft_ok = debug_draft_manager()
    if not draft_ok:
        print("Draft manager failed. Please check the draft_manager function.")
        return
    
    response_ok = debug_response_generator()
    if not response_ok:
        print("Response generator failed. Please check the response_generator function.")
        return
    
    workflow_ok = debug_workflow()
    if not workflow_ok:
        print("Workflow execution failed. Please check the workflow configuration.")
        return
    
    print("\n=== Debugging Complete ===")
    print("All components are functioning correctly!")

if __name__ == "__main__":
    # Set up the debugger
    pdb.set_trace()
    main()
