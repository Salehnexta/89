"""Initial tests for the AI Travel Assistant."""
import pytest
from pathlib import Path
import sys

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.database import get_db_connection, save_conversation, get_conversation
from app.state import AgentState
from app.mock_tools import search_mock_flights, search_mock_hotels, get_mock_general_info

def test_database_connection():
    """Test database connection and basic operations."""
    conn = get_db_connection()
    assert conn is not None
    conn.close()

def test_conversation_storage():
    """Test saving and retrieving conversations."""
    session_id = "test_session_1"
    test_history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ]
    
    # Save conversation
    save_conversation(session_id, test_history)
    
    # Retrieve conversation
    retrieved = get_conversation(session_id)
    assert len(retrieved) == 2
    assert retrieved[0]["content"] == "Hello"
    assert retrieved[1]["content"] == "Hi there!"

def test_agent_state():
    """Test AgentState functionality."""
    state = AgentState()
    
    # Test adding to history
    state.add_to_history("user", "Test message")
    assert len(state.conversation_history) == 1
    assert state.conversation_history[0]["content"] == "Test message"
    
    # Test updating draft
    state.update_draft({"destination": "Paris"})
    assert state.draft_package["destination"] == "Paris"
    assert state.draft_package["created_at"] != ""

def test_mock_tools():
    """Test mock tool functions."""
    # Test flight search
    flights = search_mock_flights("Paris", "2024-05-01")
    assert len(flights) == 3
    assert all(isinstance(f["price"], (int, float)) for f in flights)
    
    # Test hotel search
    hotels = search_mock_hotels("Paris", "2024-05-01")
    assert len(hotels) == 3
    assert all(isinstance(h["rating"], (int, float)) for h in hotels)
    
    # Test general info
    weather_info = get_mock_general_info("weather", "Paris")
    assert "temperature" in weather_info
