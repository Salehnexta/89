"""LangGraph nodes for the AI Travel Assistant."""
from typing import Dict, Any, Annotated

from langgraph.graph import StateGraph

from app.state import AgentState
from app.language_model import classify_intent, generate_response
from app.mock_tools import search_mock_flights, search_mock_hotels, get_mock_general_info

def user_input_processor(state: AgentState) -> AgentState:
    """Process user input and add it to conversation history."""
    # Add user input to conversation history
    if state.user_input:
        state.add_to_history("user", state.user_input)
    
    # Return updated state
    return state

def intent_classifier(state: AgentState) -> AgentState:
    """Classify user intent and extract parameters."""
    # Skip if no user input
    if not state.user_input:
        return state
    
    # Get intent and parameters
    result = classify_intent(state.user_input, state.get_context_window())
    
    # Update state
    state.intent = result["intent"]
    state.parameters = result["parameters"]
    
    return state

def draft_manager(state: AgentState) -> AgentState:
    """Manage the travel draft package."""
    # Skip if intent is not related to drafting
    if state.intent not in ["start_draft", "update_draft"]:
        return state
    
    # Extract parameters
    params = state.parameters
    
    # Update draft with new information
    updates = {}
    
    if "destination" in params and params["destination"]:
        updates["destination"] = params["destination"]
    
    if "dates" in params and params["dates"]:
        updates["dates"] = params["dates"]
    
    if "travelers" in params and params["travelers"]:
        updates["travelers"] = params["travelers"]
    
    if "budget" in params and params["budget"]:
        updates["budget"] = params["budget"]
    
    if "preferences" in params and params["preferences"]:
        if "preferences" not in state.draft_package:
            state.draft_package["preferences"] = {}
        
        # Handle different formats of preference data
        preferences = params["preferences"]
        if isinstance(preferences, dict):
            state.draft_package["preferences"].update(preferences)
        elif isinstance(preferences, list):
            # Convert list to dictionary if it's a list of interests
            state.draft_package["preferences"]["interests"] = preferences
        else:
            # Handle string or other formats
            state.draft_package["preferences"]["general"] = preferences
            
        updates["preferences"] = state.draft_package["preferences"]
    
    if "activities" in params and params["activities"]:
        if isinstance(params["activities"], list):
            if "activities" not in state.draft_package:
                state.draft_package["activities"] = []
            
            state.draft_package["activities"].extend(params["activities"])
            updates["activities"] = state.draft_package["activities"]
    
    # Update the draft
    if updates:
        state.update_draft(updates)
    
    return state

def mock_flight_search_tool(state: AgentState) -> AgentState:
    """Search for flights using mock data."""
    # Skip if intent is not related to flights
    if state.intent != "search_flights":
        return state
    
    # Extract parameters
    params = state.parameters
    destination = params.get("destination", "")
    departure_date = params.get("departure_date", "")
    return_date = params.get("return_date", "")
    travelers = params.get("travelers", 1)
    
    # Search for flights
    if destination and departure_date:
        flights = search_mock_flights(
            destination=destination,
            date=departure_date,
            return_date=return_date,
            num_passengers=travelers
        )
        
        # Update state
        state.mock_flight_results = flights
    
    return state

def mock_hotel_search_tool(state: AgentState) -> AgentState:
    """Search for hotels using mock data."""
    # Skip if intent is not related to hotels
    if state.intent != "search_hotels":
        return state
    
    # Extract parameters
    params = state.parameters
    destination = params.get("destination", "")
    check_in = params.get("check_in", "")
    check_out = params.get("check_out", "")
    guests = params.get("guests", 1)
    
    # Search for hotels
    if destination and check_in:
        hotels = search_mock_hotels(
            destination=destination,
            check_in=check_in,
            check_out=check_out,
            num_guests=guests
        )
        
        # Update state
        state.mock_hotel_results = hotels
    
    return state

def general_info_handler(state: AgentState) -> AgentState:
    """Handle general information requests."""
    # Skip if intent is not related to information
    if state.intent != "get_info":
        return state
    
    # Extract parameters
    params = state.parameters
    topic = params.get("topic", "")
    destination = params.get("destination", "")
    
    # Get information
    if topic and destination:
        info = get_mock_general_info(topic, destination)
        
        # Add info to state parameters for response generation
        state.parameters["info_result"] = info
    
    return state

def response_generator(state: AgentState) -> AgentState:
    """Generate a response based on the current state."""
    # Prepare context for response generation
    context = {
        "intent": state.intent,
        "parameters": state.parameters,
        "draft_package": state.draft_package if any(state.draft_package.values()) else None,
        "flight_results": state.mock_flight_results if state.mock_flight_results else None,
        "hotel_results": state.mock_hotel_results if state.mock_hotel_results else None,
        "user_input": state.user_input
    }
    
    # Generate response
    response = generate_response(context)
    
    # Update state
    state.final_response = response
    
    # Add response to conversation history
    state.add_to_history("assistant", response)
    
    # Clear temporary data
    state.user_input = ""
    state.clear_search_results()
    
    return state

def get_next_node(state: AgentState) -> str:
    """Determine the next node based on intent."""
    intent = state.intent
    
    if intent == "start_draft" or intent == "update_draft":
        return "draft_manager"
    elif intent == "search_flights":
        return "mock_flight_search_tool"
    elif intent == "search_hotels":
        return "mock_hotel_search_tool"
    elif intent == "get_info":
        return "general_info_handler"
    else:
        return "response_generator"
