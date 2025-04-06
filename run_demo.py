"""
AI Travel Assistant Demo Script

This script runs a demonstration of the AI Travel Assistant for investors.
It follows the conversation flow outlined in demo_script.md and showcases
the assistant's capabilities for trip planning, flight/hotel search, and
travel information.
"""
import os
import sys
import time
import json
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.state import AgentState
from app.workflow import compiled_workflow
from app.database import init_db, save_conversation, get_conversation

# Initialize database
init_db()

# Demo conversation flow based on demo_script.md
DEMO_CONVERSATION = [
    "I'm planning a trip to Paris for a week in June with my partner. We're interested in art and food.",
    "What are the best times to visit museums in Paris?",
    "We'd also like to visit some vineyards. Can you recommend any day trips?",
    "Can you find flights from New York to Paris for June 15-22?",
    "I'd prefer a direct flight in the morning.",
    "Now I need a hotel in central Paris near the Louvre.",
    "I'd like something with a view and breakfast included.",
    "What kind of weather should we expect in Paris in June?",
    "Do we need any special travel documents for France?"
]

def run_demo(session_id, auto_mode=False, delay=2):
    """
    Run the demo conversation.
    
    Args:
        session_id: Unique session identifier
        auto_mode: If True, runs the entire demo automatically
        delay: Delay between messages in auto mode (seconds)
    """
    print("\n" + "=" * 80)
    print("AI TRAVEL ASSISTANT DEMO".center(80))
    print("=" * 80 + "\n")
    
    # Create initial state
    state = AgentState()
    
    # Load existing conversation if available
    history = get_conversation(session_id)
    if history:
        state.conversation_history = history
        print("Loaded existing conversation.\n")
        
        # Display existing conversation
        for message in history:
            role = message["role"]
            content = message["content"]
            
            if role == "user":
                print(f"\033[94mUser:\033[0m {content}")
            else:
                print(f"\033[92mAssistant:\033[0m {content}")
        print("\n")
    
    # Run the conversation
    try:
        if auto_mode:
            # Automatic mode - run through all demo messages
            for user_input in DEMO_CONVERSATION:
                print(f"\033[94mUser:\033[0m {user_input}")
                
                # Process user input
                state.user_input = user_input
                result_state = compiled_workflow.invoke(state)
                
                # Extract the final response from the state
                # LangGraph might return a different state format
                if hasattr(result_state, 'final_response'):
                    response = result_state.final_response
                elif isinstance(result_state, dict) and 'final_response' in result_state:
                    response = result_state['final_response']
                else:
                    response = "I'm processing your request..."
                
                # Update our state object
                state = result_state
                
                # Display assistant response
                time.sleep(delay)  # Add delay to simulate typing
                print(f"\033[92mAssistant:\033[0m {response}\n")
                
                # Save conversation
                # Handle different state formats
                if hasattr(state, 'conversation_history'):
                    history = state.conversation_history
                elif isinstance(state, dict) and 'conversation_history' in state:
                    history = state['conversation_history']
                else:
                    # Create a basic history if not available
                    history = [
                        {"role": "user", "content": user_input},
                        {"role": "assistant", "content": response}
                    ]
                
                save_conversation(session_id, history)
                
                # Pause between exchanges
                time.sleep(delay)
        else:
            # Interactive mode
            print("Demo is in interactive mode. Type 'exit' to quit or 'auto' to switch to automatic mode.\n")
            
            while True:
                # Get user input
                user_input = input("\033[94mUser:\033[0m ")
                
                # Check for exit command
                if user_input.lower() == "exit":
                    break
                
                # Check for auto mode switch
                if user_input.lower() == "auto":
                    print("\nSwitching to automatic mode...\n")
                    remaining_msgs = DEMO_CONVERSATION[len(state.conversation_history) // 2:]
                    
                    for demo_input in remaining_msgs:
                        print(f"\033[94mUser:\033[0m {demo_input}")
                        
                        # Process user input
                        state.user_input = demo_input
                        state = compiled_workflow.invoke(state)
                        
                        # Display assistant response
                        time.sleep(delay)
                        print(f"\033[92mAssistant:\033[0m {state.assistant_response}\n")
                        
                        # Save conversation
                        save_conversation(session_id, state.conversation_history)
                        
                        # Pause between exchanges
                        time.sleep(delay)
                    
                    break
                
                # Process user input
                state.user_input = user_input
                result_state = compiled_workflow.invoke(state)
                
                # Extract the final response from the state
                # LangGraph might return a different state format
                if hasattr(result_state, 'final_response'):
                    response = result_state.final_response
                elif isinstance(result_state, dict) and 'final_response' in result_state:
                    response = result_state['final_response']
                else:
                    response = "I'm processing your request..."
                
                # Update our state object
                state = result_state
                
                # Display assistant response
                print(f"\033[92mAssistant:\033[0m {response}\n")
                
                # Save conversation
                # Handle different state formats
                if hasattr(state, 'conversation_history'):
                    history = state.conversation_history
                elif isinstance(state, dict) and 'conversation_history' in state:
                    history = state['conversation_history']
                else:
                    # Create a basic history if not available
                    history = [
                        {"role": "user", "content": user_input},
                        {"role": "assistant", "content": response}
                    ]
                
                save_conversation(session_id, history)
    
    except KeyboardInterrupt:
        print("\n\nDemo interrupted. Saving conversation...")
        save_conversation(session_id, state.conversation_history)
    
    print("\nDemo completed. Conversation saved.")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run the AI Travel Assistant demo")
    parser.add_argument("--session", default=f"demo_{int(time.time())}", help="Session ID for the conversation")
    parser.add_argument("--auto", action="store_true", help="Run in automatic mode")
    parser.add_argument("--delay", type=int, default=2, help="Delay between messages in auto mode (seconds)")
    
    args = parser.parse_args()
    
    # Run the demo
    run_demo(args.session, args.auto, args.delay)
