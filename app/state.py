"""State management for the AI Travel Assistant."""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class AgentState:
    """State container for the AI Travel Assistant."""
    
    # Input and conversation state
    user_input: str = ""
    conversation_history: List[Dict[str, str]] = field(default_factory=list)
    
    # Intent and parameters from the last user message
    intent: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    # Travel package draft state
    draft_package: Dict[str, Any] = field(default_factory=lambda: {
        "destination": "",
        "dates": {},
        "travelers": 0,
        "preferences": {},
        "activities": [],
        "budget": {},
        "created_at": "",
        "last_modified": ""
    })
    
    # Search results
    mock_flight_results: List[Dict[str, Any]] = field(default_factory=list)
    mock_hotel_results: List[Dict[str, Any]] = field(default_factory=list)
    
    # Response generation
    final_response: str = ""
    
    def update_draft(self, updates: Dict[str, Any]):
        """Update the draft package with new information."""
        self.draft_package.update(updates)
        self.draft_package["last_modified"] = datetime.now().isoformat()
        if not self.draft_package["created_at"]:
            self.draft_package["created_at"] = self.draft_package["last_modified"]
    
    def add_to_history(self, role: str, content: str):
        """Add a message to the conversation history."""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def clear_search_results(self):
        """Clear temporary search results."""
        self.mock_flight_results.clear()
        self.mock_hotel_results.clear()
    
    def get_context_window(self, max_messages: int = 5) -> List[Dict[str, str]]:
        """Get the recent conversation context."""
        return self.conversation_history[-max_messages:] if self.conversation_history else []
