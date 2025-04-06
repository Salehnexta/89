"""FastAPI application for the AI Travel Assistant."""
import uuid
from typing import Dict, List, Any, Optional
import traceback # Import traceback module
import logging # Import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.state import AgentState
from app.workflow import compiled_workflow
from app.database import save_conversation, get_conversation
from app.config import validate_config

# Validate configuration
validate_config()

# Create FastAPI app
app = FastAPI(
    title="AI Travel Assistant API",
    description="API for the AI Travel Assistant demo",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request and response models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    chat_history: Optional[List[Dict[str, str]]] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "AI Travel Assistant API is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint."""
    # Generate session ID if not provided
    session_id = request.session_id or str(uuid.uuid4())
    
    # Get conversation history from database or request
    conversation_history = request.chat_history or get_conversation(session_id)
    
    # Create initial state
    initial_state = AgentState(
        user_input=request.message,
        conversation_history=conversation_history
    )
    
    # Invoke workflow
    try:
        result_state = compiled_workflow.invoke(initial_state)
        
        # Save conversation to database
        save_conversation(session_id, result_state.conversation_history)
        
        # Return response
        return ChatResponse(
            response=result_state.final_response,
            session_id=session_id
        )
    except Exception as e:
        # Log the detailed traceback
        tb_str = traceback.format_exc()
        logging.error(f"Error processing request: {e}\nTraceback:\n{tb_str}")
        # Reraise as HTTPException
        raise HTTPException(status_code=500, detail=f"Error processing request: {e}") from e

if __name__ == "__main__":
    import uvicorn
    from app.config import BACKEND_HOST, BACKEND_PORT
    
    uvicorn.run("app.main:app", host=BACKEND_HOST, port=BACKEND_PORT, reload=True)
