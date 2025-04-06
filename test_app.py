"""
Test script for the AI Travel Assistant application.

This script tests all the main features of the application to ensure
they work correctly with the DeepSeek API integration.
"""
import os
import sys
import time
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.config import BACKEND_HOST, BACKEND_PORT, DEEPSEEK_API_KEY
from app.database import init_db, save_conversation, get_conversation

# Initialize database
init_db()

# API endpoint
API_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}/chat"

# Test session ID
TEST_SESSION_ID = f"test_session_{int(time.time())}"

# Test cases
TEST_CASES = [
    {
        "name": "Trip Planning",
        "message": "I want to plan a trip to Paris in June with my partner. We're interested in art and food.",
        "expected_intent": "start_draft"
    },
    {
        "name": "Flight Search",
        "message": "Can you find flights from New York to Paris for June 15-22?",
        "expected_intent": "flight_search"
    },
    {
        "name": "Hotel Search",
        "message": "I need a hotel in central Paris near the Louvre.",
        "expected_intent": "hotel_search"
    },
    {
        "name": "General Information",
        "message": "What's the weather like in Paris in June?",
        "expected_intent": "general_info"
    }
]

def test_backend_connection():
    """Test connection to the backend server."""
    print("\n=== Testing Backend Connection ===")
    try:
        # Send a simple request to check if the server is running
        response = requests.get(f"http://{BACKEND_HOST}:{BACKEND_PORT}/health")
        response.raise_for_status()
        
        print(f"✅ Backend server is running at http://{BACKEND_HOST}:{BACKEND_PORT}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to backend server: {str(e)}")
        return False

def test_api_key():
    """Test if the DeepSeek API key is configured."""
    print("\n=== Testing API Key Configuration ===")
    if DEEPSEEK_API_KEY:
        print("✅ DeepSeek API key is configured")
        return True
    else:
        print("⚠️ DeepSeek API key is not configured. Tests will run in mock mode.")
        return False

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
        print(f"❌ Error sending message: {str(e)}")
        return None

def test_conversation_flow():
    """Test the conversation flow with multiple messages."""
    print("\n=== Testing Conversation Flow ===")
    
    chat_history = []
    
    for i, test_case in enumerate(TEST_CASES):
        print(f"\nTest Case {i+1}: {test_case['name']}")
        print(f"User: {test_case['message']}")
        
        # Send message to API
        data = send_message(test_case['message'], chat_history)
        
        if data:
            # Print response
            print(f"Assistant: {data['response'][:100]}...")
            
            # Check if response is not empty
            if data['response']:
                print(f"✅ Received non-empty response")
            else:
                print(f"❌ Received empty response")
            
            # Update chat history
            chat_history.append({"role": "user", "content": test_case['message']})
            chat_history.append({"role": "assistant", "content": data['response']})
            
            # Check if conversation was saved to database
            saved_history = get_conversation(TEST_SESSION_ID)
            if saved_history:
                print(f"✅ Conversation saved to database")
            else:
                print(f"❌ Conversation not saved to database")
        else:
            print(f"❌ Failed to get response")
    
    return len(chat_history) > 0

def test_error_handling():
    """Test error handling with an invalid request."""
    print("\n=== Testing Error Handling ===")
    
    try:
        # Send an invalid request (missing required fields)
        response = requests.post(API_URL, json={})
        
        # Check if we got a proper error response
        if response.status_code >= 400:
            print(f"✅ Received expected error response (status code: {response.status_code})")
            return True
        else:
            print(f"❌ Expected error response, got status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending request: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("Starting AI Travel Assistant Tests")
    print("==================================")
    
    # Test backend connection
    if not test_backend_connection():
        print("\n❌ Backend server is not running. Please start the server and try again.")
        return
    
    # Test API key configuration
    has_api_key = test_api_key()
    
    # Test conversation flow
    conversation_ok = test_conversation_flow()
    
    # Test error handling
    error_handling_ok = test_error_handling()
    
    # Print summary
    print("\n=== Test Summary ===")
    print(f"Backend Connection: {'✅ OK' if True else '❌ Failed'}")
    print(f"API Key Configuration: {'✅ OK' if has_api_key else '⚠️ Running in mock mode'}")
    print(f"Conversation Flow: {'✅ OK' if conversation_ok else '❌ Failed'}")
    print(f"Error Handling: {'✅ OK' if error_handling_ok else '❌ Failed'}")
    
    if conversation_ok and error_handling_ok:
        print("\n✅ All tests passed! The AI Travel Assistant is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the logs for details.")

if __name__ == "__main__":
    main()
