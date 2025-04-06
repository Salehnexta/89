"""Language model interface for the AI Travel Assistant."""
import json
import random
from typing import Dict, Any, List, Optional

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage, BaseMessage
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.llms.base import LLM

from app.config import DEEPSEEK_API_KEY, GOOGLE_API_KEY

class MockResponse:
    """Mock response object that mimics the structure of ChatOpenAI responses."""
    def __init__(self, content: str):
        self.content = content

class MockLanguageModel:
    """Mock language model for testing without API keys."""
    temperature: float = 0.7
    
    def __init__(self, temperature: float = 0.7):
        self.temperature = temperature
    
    def _generate_mock_response(self, prompt: str) -> str:
        """Generate a mock response based on the prompt."""
        # Simple intent classification based on keywords
        if 'intent' in prompt.lower():
            return json.dumps({
                "intent": "start_draft",
                "parameters": {
                    "destination": "Paris",
                    "dates": "June",
                    "travelers": 2,
                    "interests": ["art", "food"]
                }
            })
        
        # Generate context-aware responses based on keywords in the prompt
        if 'flight' in prompt.lower():
            return "I've found several flight options from New York to Paris for June 15-22. The best option is a direct flight with Air France departing at 7:30 PM, arriving at 9:00 AM the next day. The price is approximately $950 round trip per person."
        
        if 'hotel' in prompt.lower():
            return "For hotels near the Louvre, I recommend the Hotel du Louvre, a 4-star hotel with excellent reviews. It's just a 5-minute walk from the museum and offers rooms with views starting at $220 per night. They do include breakfast!"
        
        if 'weather' in prompt.lower():
            return "In June, Paris typically enjoys pleasant weather with average temperatures between 60°F and 75°F (15°C to 24°C). It's generally sunny with occasional light rain showers. It's a great time to visit as the days are long and the city's gardens are in full bloom."
        
        # Default responses for trip planning
        responses = [
            "I'd be happy to help you plan your trip to Paris! Paris is known for its art museums like the Louvre and Musée d'Orsay, as well as its incredible food scene. For art lovers, I recommend visiting museums in the morning when they're less crowded, typically right when they open around 9 AM.",
            "Paris is a wonderful destination for art and food lovers. The best times to visit museums are weekday mornings, especially Tuesday through Thursday. For food, you should definitely try the local bistros in neighborhoods like Le Marais and Saint-Germain-des-Prés.",
            "For your trip to Paris, I suggest creating an itinerary that balances major attractions with time to wander and discover hidden gems. The Louvre is less crowded on Wednesday and Friday evenings when it's open late."
        ]
        return random.choice(responses)
    
    def invoke(self, input_messages: List[BaseMessage], **kwargs) -> MockResponse:
        """Process a list of messages and return a response object with content attribute."""
        # Extract the prompt from the messages
        prompt = " ".join([msg.content for msg in input_messages])
        
        # Generate the response content
        response_content = self._generate_mock_response(prompt)
        
        # Return a mock response object with a content attribute
        return MockResponse(content=response_content)

def get_language_model(temperature: float = 0.7, use_mock: bool = True):
    """Get a language model instance.
    
    Args:
        temperature: The temperature parameter for the language model.
        use_mock: Whether to use mock data for the demo. Default is True for reliable demo experience.
    """
    # For demos and tests, we prioritize the mock model for reliability
    if use_mock:
        print("Using mock language model for demo/test purposes.")
        return MockLanguageModel(temperature=temperature)
    
    # For production, try to use DeepSeek API first, fall back to Google API if needed
    elif DEEPSEEK_API_KEY:
        try:
            return ChatOpenAI(
                model="deepseek-chat",  # This is the model name for DeepSeek
                api_key=DEEPSEEK_API_KEY,
                temperature=temperature,
                base_url="https://api.deepseek.com/v1",  # Updated base URL with version
                max_retries=3,  # Add retries for better reliability
                timeout=60  # Increase timeout for longer responses
            )
        except Exception as e:
            print(f"Error initializing DeepSeek API: {str(e)}. Falling back to alternative.")
            # If DeepSeek fails, we'll try the next option
    elif GOOGLE_API_KEY:
        # Import here to avoid circular imports
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=GOOGLE_API_KEY,
            temperature=temperature,
            convert_system_message_to_human=True
        )
    else:
        # Use mock mode for testing without API keys
        print("WARNING: No API keys found. Using mock mode for language model.")
        return MockLanguageModel(temperature=temperature)

def format_chat_history(history: List[Dict[str, str]]) -> List[Any]:
    """Format chat history for the language model."""
    formatted_messages = []
    
    for message in history:
        if message["role"] == "user":
            formatted_messages.append(HumanMessage(content=message["content"]))
        elif message["role"] == "assistant":
            formatted_messages.append(AIMessage(content=message["content"]))
        elif message["role"] == "system":
            formatted_messages.append(SystemMessage(content=message["content"]))
    
    return formatted_messages

def classify_intent(
    user_input: str,
    history: List[Dict[str, str]]
) -> Dict[str, Any]:
    """Classify the user's intent and extract parameters."""
    try:
        model = get_language_model(temperature=0.2)  # Lower temperature for more deterministic output
        
        # Define the output schema
        intent_schema = ResponseSchema(
            name="intent",
            description="The user's intent category (start_draft, update_draft, search_flights, search_hotels, get_info, etc.)"
        )
        
        parameters_schema = ResponseSchema(
            name="parameters",
            description="Parameters extracted from the user's message (destination, dates, travelers, preferences, etc.)"
        )
        
        # Create a parser with the schemas
        parser = StructuredOutputParser.from_response_schemas([intent_schema, parameters_schema])
        format_instructions = parser.get_format_instructions()
        
        # Create system and user messages
        system_message = SystemMessage(
            content=(
                "You are an AI assistant that classifies user intents for a travel planning application. "
                "Extract the user's intent and any relevant parameters from their message."
            )
        )
        
        # Format history for context
        formatted_history = format_chat_history(history)
        
        # Add the current user input
        user_message = HumanMessage(
            content=(
                f"Based on this message: '{user_input}', classify the intent and extract parameters. "
                f"\n{format_instructions}"
            )
        )
        
        # Generate classification
        messages = [system_message] + formatted_history + [user_message]
        response = model.invoke(messages)
        
        # Parse the response
        try:
            parsed_response = parser.parse(response.content)
            return parsed_response
        except Exception as e:
            # Fallback to a simple classification if parsing fails
            print(f"Error parsing intent classification: {str(e)}")
            
            # Simple keyword-based fallback
            intent = "general_info"
            parameters = {}
            
            if any(keyword in user_input.lower() for keyword in ["plan", "trip", "visit", "vacation"]):
                intent = "start_draft"
                # Extract potential destination
                parameters = {"destination": "Unknown"}
            elif any(keyword in user_input.lower() for keyword in ["flight", "fly", "plane"]):
                intent = "flight_search"
            elif any(keyword in user_input.lower() for keyword in ["hotel", "stay", "accommodation"]):
                intent = "hotel_search"
            
            return {"intent": intent, "parameters": parameters}
    
    except Exception as e:
        # Main error handling for the entire function
        print(f"Error in intent classification: {str(e)}")
        # Return a safe default intent
        return {
            "intent": "general_info",
            "parameters": {}
        }

def generate_response(
    state_context: Dict[str, Any],
    system_prompt: Optional[str] = None
) -> str:
    """Generate a response based on the current state."""
    try:
        model = get_language_model(temperature=0.7)
        
        # Default system prompt
        if system_prompt is None:
            system_prompt = (
                "You are an AI Travel Assistant helping users plan trips, find flights and hotels, "
                "and provide travel information. Be helpful, concise, and friendly. "
                "If you don't know something, be honest about it."
            )
        
        # Format conversation history
        conversation_history = state_context.get("conversation_history", [])
        formatted_history = format_chat_history(conversation_history)
        
        # Create messages
        messages = [
            SystemMessage(content=system_prompt),
            *formatted_history
        ]
        
        # Generate response
        response = model.invoke(messages)
        
        return response.content
    except Exception as e:
        # Log the error
        print(f"Error generating response: {str(e)}")
        
        # Provide a fallback response
        fallback_responses = [
            "I'm sorry, I'm having trouble processing your request right now. Could you please try again?",
            "It seems there's a technical issue on my end. Let me try to help you with a simpler response.",
            "I apologize for the inconvenience, but I'm experiencing some difficulties. Please try rephrasing your question."
        ]
        
        # Use the user input to generate a more contextual fallback if possible
        user_input = ""
        for message in reversed(conversation_history):
            if message.get("role") == "user":
                user_input = message.get("content", "")
                break
        
        if "flight" in user_input.lower():
            return "I'm sorry, I'm having trouble accessing flight information right now. Please try again in a moment."
        elif "hotel" in user_input.lower():
            return "I apologize, but I can't retrieve hotel information at the moment. Please try again shortly."
        elif any(word in user_input.lower() for word in ["weather", "temperature", "forecast"]):
            return "I'm sorry, I can't access weather information right now. Please try again later."
        
        import random
        return random.choice(fallback_responses)
