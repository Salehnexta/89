"""
Tests for DeepSeek API integration in the AI Travel Assistant.

This test suite focuses on testing the language model functionality
with the DeepSeek API integration.
"""
import unittest
import os
import sys
import json
from unittest.mock import patch, MagicMock
import datetime

# Add the parent directory to sys.path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.state import AgentState
from app.workflow import compiled_workflow
from app.language_model import get_language_model, generate_response, classify_intent
from app.config import DEEPSEEK_API_KEY, GOOGLE_API_KEY
from app.nodes import intent_classifier, response_generator


class TestDeepSeekIntegration(unittest.TestCase):
    """Tests for DeepSeek API integration in the AI Travel Assistant."""

    def setUp(self):
        """Set up test environment before each test."""
        # Create a test state
        self.state = AgentState()
        
        # Check if we're using the real API or mock mode
        self.using_real_api = bool(DEEPSEEK_API_KEY)
        if not self.using_real_api:
            print("\nWARNING: No DeepSeek API key found. Tests will run in mock mode.")
    
    def test_language_model_initialization(self):
        """Test that the language model can be initialized."""
        model = get_language_model()
        self.assertIsNotNone(model)
        
        # Check the model type based on available API keys
        if self.using_real_api:
            from langchain_openai import ChatOpenAI
            self.assertIsInstance(model, ChatOpenAI)
        else:
            from app.language_model import MockLanguageModel
            self.assertIsInstance(model, MockLanguageModel)
    
    def test_intent_classification(self):
        """Test intent classification with various inputs."""
        test_inputs = [
            {
                "input": "I want to plan a trip to Paris in June",
                "expected_intent": "start_draft",
                "expected_params": {"destination": "Paris"}
            },
            {
                "input": "Find me flights to New York for July 15-22",
                "expected_intent": "flight_search",
                "expected_params": {"destination": "New York"}
            },
            {
                "input": "What hotels are available in Barcelona?",
                "expected_intent": "hotel_search",
                "expected_params": {"destination": "Barcelona"}
            },
            {
                "input": "What's the weather like in Tokyo in spring?",
                "expected_intent": "general_info",
                "expected_params": {"destination": "Tokyo", "topic": "weather"}
            }
        ]
        
        for test_case in test_inputs:
            # Set up the state with the test input
            self.state.user_input = test_case["input"]
            
            # Run intent classification
            result_state = intent_classifier(self.state)
            
            # Check that an intent was classified
            self.assertIsNotNone(result_state.intent)
            self.assertNotEqual(result_state.intent, "")
            
            # If using the real API, check that parameters were extracted
            if self.using_real_api:
                self.assertIsNotNone(result_state.parameters)
                # Check for the expected destination in parameters
                if "destination" in test_case["expected_params"]:
                    self.assertIn("destination", result_state.parameters)
            
            # Print the actual results for debugging
            print(f"\nInput: {test_case['input']}")
            print(f"Detected intent: {result_state.intent}")
            print(f"Extracted parameters: {json.dumps(result_state.parameters, indent=2)}")
    
    def test_response_generation(self):
        """Test response generation with various contexts."""
        test_contexts = [
            {
                "intent": "start_draft",
                "user_input": "I want to plan a trip to Paris in June",
                "parameters": {"destination": "Paris", "dates": {"month": "June"}}
            },
            {
                "intent": "flight_search",
                "user_input": "Find me flights to New York",
                "parameters": {"destination": "New York"},
                "mock_flight_results": [
                    {
                        "airline": "Test Airlines",
                        "flight_number": "TA123",
                        "price": 500,
                        "departure_time": "10:00 AM",
                        "arrival_time": "2:00 PM",
                        "stops": 0
                    }
                ]
            },
            {
                "intent": "general_info",
                "user_input": "What's the weather like in Tokyo?",
                "parameters": {
                    "destination": "Tokyo", 
                    "topic": "weather",
                    "info_result": {"weather": "Tokyo has four distinct seasons."}
                }
            }
        ]
        
        for context in test_contexts:
            # Set up the state with the test context
            self.state.intent = context["intent"]
            self.state.user_input = context["user_input"]
            self.state.parameters = context["parameters"]
            
            if "mock_flight_results" in context:
                self.state.mock_flight_results = context["mock_flight_results"]
            
            # Run response generation
            result_state = response_generator(self.state)
            
            # Check that a response was generated
            self.assertIsNotNone(result_state.final_response)
            self.assertNotEqual(result_state.final_response, "")
            
            # Print the actual response for debugging
            print(f"\nContext: {context['intent']} - {context['user_input']}")
            print(f"Generated response: {result_state.final_response[:100]}...")
    
    @patch('app.language_model.get_language_model')
    def test_error_handling(self, mock_get_model):
        """Test error handling when the API fails."""
        # Mock the language model to raise an exception
        mock_model = MagicMock()
        mock_model.invoke.side_effect = Exception("API Error")
        mock_get_model.return_value = mock_model
        
        # Set up the state
        self.state.intent = "general_info"
        self.state.user_input = "What's the weather like in Tokyo?"
        self.state.parameters = {"destination": "Tokyo", "topic": "weather"}
        
        # Run response generation
        result_state = response_generator(self.state)
        
        # Check that a fallback response was generated
        self.assertIsNotNone(result_state.final_response)
        self.assertNotEqual(result_state.final_response, "")
        
        # Print the actual response for debugging
        print(f"\nError handling test:")
        print(f"Generated response: {result_state.final_response[:100]}...")
    
    def test_full_workflow(self):
        """Test the full workflow with a sample user input."""
        # Skip this test if we're not using the real API
        if not self.using_real_api:
            self.skipTest("Skipping full workflow test in mock mode")
        
        # Set up the state with a sample user input
        self.state.user_input = "I want to plan a trip to Paris in June with my family"
        
        # Run the workflow
        try:
            result_state = compiled_workflow.invoke(self.state)
            
            # Check the result type
            self.assertIsNotNone(result_state)
            
            # Extract and check the response
            if hasattr(result_state, 'final_response'):
                response = result_state.final_response
            elif isinstance(result_state, dict) and 'final_response' in result_state:
                response = result_state['final_response']
            else:
                response = None
            
            self.assertIsNotNone(response)
            self.assertNotEqual(response, "")
            
            # Print the actual response for debugging
            print(f"\nFull workflow test:")
            print(f"Input: {self.state.user_input}")
            print(f"Generated response: {response[:100]}...")
            
        except Exception as e:
            self.fail(f"Workflow execution failed with error: {str(e)}")


if __name__ == '__main__':
    unittest.main()
