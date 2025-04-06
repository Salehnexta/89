"""LangGraph workflow for the AI Travel Assistant."""
from typing import Annotated, TypedDict

from langgraph.graph import StateGraph

from app.state import AgentState
from app.nodes import (
    user_input_processor,
    intent_classifier,
    draft_manager,
    mock_flight_search_tool,
    mock_hotel_search_tool,
    general_info_handler,
    response_generator,
    get_next_node
)

def create_workflow() -> StateGraph:
    """Create the LangGraph workflow."""
    # Create the workflow
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("user_input_processor", user_input_processor)
    workflow.add_node("intent_classifier", intent_classifier)
    workflow.add_node("draft_manager", draft_manager)
    workflow.add_node("mock_flight_search_tool", mock_flight_search_tool)
    workflow.add_node("mock_hotel_search_tool", mock_hotel_search_tool)
    workflow.add_node("general_info_handler", general_info_handler)
    workflow.add_node("response_generator", response_generator)
    
    # Set the entry point
    workflow.set_entry_point("user_input_processor")
    
    # Define edges
    workflow.add_edge("user_input_processor", "intent_classifier")
    
    # Conditional edges based on intent
    workflow.add_conditional_edges(
        "intent_classifier",
        get_next_node
    )
    
    # Connect tool nodes to response generator
    workflow.add_edge("draft_manager", "response_generator")
    workflow.add_edge("mock_flight_search_tool", "response_generator")
    workflow.add_edge("mock_hotel_search_tool", "response_generator")
    workflow.add_edge("general_info_handler", "response_generator")
    
    # Compile the workflow
    return workflow.compile()

# Create the compiled workflow
compiled_workflow = create_workflow()
