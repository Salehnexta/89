"""
Test script for the AI Travel Assistant demo flow.

This script tests the conversation flows outlined in the demo script
to ensure they work correctly with the DeepSeek API integration.
"""
import os
import sys
import json
import time
import requests
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

# Load environment variables
load_dotenv()

# Add the current directory to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# API endpoint
API_URL = "http://127.0.0.1:8000/chat"

# Test session ID
TEST_SESSION_ID = f"demo_test_{int(time.time())}"

# Demo conversation flows from the demo script
DEMO_FLOWS = [
    {
        "name": "Trip Planning Flow",
        "messages": [
            "I'm planning a trip to Paris for a week in June with my partner. We're interested in art and food.",
            "What are the best times to visit museums in Paris?",
            "We'd also like to visit some vineyards. Can you recommend any day trips?"
        ]
    },
    {
        "name": "Flight Search Flow",
        "messages": [
            "Can you find flights from New York to Paris for June 15-22?",
            "I'd prefer a direct flight in the morning."
        ]
    },
    {
        "name": "Hotel Search Flow",
        "messages": [
            "Now I need a hotel in central Paris near the Louvre.",
            "I'd like something with a view and breakfast included."
        ]
    },
    {
        "name": "Travel Information Flow",
        "messages": [
            "What kind of weather should we expect in Paris in June?",
            "Do we need any special travel documents for France?"
        ]
    }
]

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"{Fore.CYAN}{Style.BRIGHT}{text}{Style.RESET_ALL}")
    print("=" * 80)

def print_user_message(message):
    """Print a formatted user message."""
    print(f"\n{Fore.GREEN}User: {message}{Style.RESET_ALL}")

def print_assistant_message(message):
    """Print a formatted assistant message."""
    print(f"\n{Fore.BLUE}Assistant: {message[:200]}...{Style.RESET_ALL}")

def send_message(message, chat_history=None):
    """Send a message to the API and get the response."""
    if chat_history is None:
        chat_history = []
    
    # Prepare payload
    payload = {
        "message": message,
        "session_id": TEST_SESSION_ID,
        "chat_history": chat_history
    }
    
    try:
        # Send request to API
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        
        # Parse response
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error sending message: {str(e)}{Style.RESET_ALL}")
        return None

def test_conversation_flow(flow):
    """Test a conversation flow."""
    print_header(f"Testing {flow['name']}")
    
    chat_history = []
    
    for message in flow["messages"]:
        print_user_message(message)
        
        # Send message to API
        data = send_message(message, chat_history)
        
        if data:
            # Print response
            print_assistant_message(data["response"])
            
            # Check if response is not empty
            if data["response"]:
                print(f"{Fore.GREEN}✓ Received non-empty response{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}✗ Received empty response{Style.RESET_ALL}")
            
            # Update chat history
            chat_history.append({"role": "user", "content": message})
            chat_history.append({"role": "assistant", "content": data["response"]})
        else:
            print(f"{Fore.RED}✗ Failed to get response{Style.RESET_ALL}")
            return False
    
    return True

def main():
    """Run all tests."""
    print_header("AI Travel Assistant Demo Flow Test")
    
    # Check if API is accessible
    try:
        response = requests.get("http://127.0.0.1:8000")
        response.raise_for_status()
        print(f"{Fore.GREEN}✓ Backend API is accessible{Style.RESET_ALL}")
    except requests.exceptions.RequestException:
        print(f"{Fore.RED}✗ Backend API is not accessible. Please start the server.{Style.RESET_ALL}")
        return
    
    # Test each conversation flow
    results = []
    for flow in DEMO_FLOWS:
        result = test_conversation_flow(flow)
        results.append((flow["name"], result))
        
        # Add a small delay between flows
        time.sleep(2)
    
    # Print summary
    print_header("Test Summary")
    for name, result in results:
        status = f"{Fore.GREEN}✓ Passed{Style.RESET_ALL}" if result else f"{Fore.RED}✗ Failed{Style.RESET_ALL}"
        print(f"{name}: {status}")
    
    # Overall result
    if all(result for _, result in results):
        print(f"\n{Fore.GREEN}All demo flows passed! The application is ready for the investor demo.{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.YELLOW}Some demo flows failed. Please review the issues before the investor demo.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
