"""Gradio frontend for the AI Travel Assistant.

This module provides a user-friendly web interface for the AI Travel Assistant,
allowing users to interact with the assistant through a chat interface.
"""
import os
import sys
import json
import uuid
import requests
import time
from typing import List, Tuple, Any
from pathlib import Path

import gradio as gr

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import BACKEND_HOST, BACKEND_PORT

# API endpoint
API_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}/chat"

# Session management
session_id = str(uuid.uuid4())

def respond(message: str, chat_history: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """Send message to API and get response."""
    global session_id
    
    # Convert Gradio chat history to API format
    api_history = []
    for user_msg, bot_msg in chat_history:
        if user_msg:
            api_history.append({"role": "user", "content": user_msg})
        if bot_msg:
            api_history.append({"role": "assistant", "content": bot_msg})
    
    # Add current message
    api_history.append({"role": "user", "content": message})
    
    # Prepare payload - only include necessary fields
    payload = {
        "message": message,
        "session_id": session_id
    }
    
    # Only include chat history if it's not empty
    if api_history:
        payload["chat_history"] = api_history
    
    try:
        # Send request to API
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        
        # Parse response
        data = response.json()
        bot_message = data["response"]
        
        # Update session ID if provided
        if "session_id" in data:
            session_id = data["session_id"]
        
        # Return updated chat history
        chat_history.append((message, bot_message))
        return chat_history
    
    except requests.exceptions.RequestException as e:
        error_msg = f"Error communicating with the backend server: {str(e)}"
        chat_history.append((message, error_msg))
        return chat_history

# Example conversations with detailed descriptions
examples = [
    ["I want to plan a trip to Paris for next month", "Start planning a trip to Paris"],
    ["What's the best time to visit Tokyo?", "Get travel information about Tokyo"],
    ["Find me flights to New York for July 15-22", "Search for flights to New York"],
    ["Show me hotels in Barcelona for 2 people", "Find accommodation in Barcelona"],
    ["What kind of visa do I need for Thailand?", "Get visa information for Thailand"],
    ["Recommend some activities in Rome for a family with kids", "Get activity recommendations"],
    ["What are the COVID-19 restrictions for traveling to Canada?", "Check travel restrictions"]
]

# Load custom HTML components
def load_html_file(file_path):
    """Load HTML content from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error loading HTML file {file_path}: {e}")
        return ""

# Set up static file serving
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

# Load custom HTML components
header_html = load_html_file(os.path.join(static_dir, "header.html"))
footer_html = load_html_file(os.path.join(static_dir, "footer.html"))

# Create a more professional Gradio interface
with gr.Blocks(css=os.path.join(static_dir, "custom.css"), theme=gr.themes.Soft()) as demo:
    # Custom header
    gr.HTML(header_html)
    
    # Title and description
    gr.Markdown(
        """
        # AI Travel Assistant
        
        Welcome to the AI Travel Assistant! I can help you plan trips, find flights and hotels, 
        and provide travel information. Powered by advanced AI technology, I'm here to make your 
        travel planning experience seamless and enjoyable.
        
        ### How can I help you today?
        """
    )
    
    # Error message container
    error_container = gr.HTML(
        """<div id="error-message" class="error-message">An error occurred. Please try again.</div>""",
        visible=True
    )
    
    # Chat interface
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        height=500,
        label="Conversation"
    )
    
    # Input components
    with gr.Row():
        with gr.Column(scale=4):
            msg = gr.Textbox(
                show_label=False,
                placeholder="Ask me anything about travel planning...",
                container=False,
                scale=4,
                autofocus=True
            )
        with gr.Column(scale=1):
            submit_btn = gr.Button("Send", variant="primary", scale=1)
    
    # Clear button
    clear_btn = gr.Button("Clear Conversation", variant="secondary")
    
    # Examples section with improved styling
    gr.Markdown("### Try some examples:")
    example_container = gr.Examples(
        examples=examples,
        inputs=msg,
        label="Example queries",
        examples_per_page=5
    )
    
    # Status indicator
    status = gr.Markdown("")
    
    # Set up event handlers
    def user_input(message, history):
        """Process user input and update status."""
        status.update("Thinking...")
        return "", history + [[message, None]]
    
    def bot_response(history):
        """Generate bot response and update status."""
        user_message = history[-1][0]
        history[-1][1] = ""
        
        try:
            # Process through our API
            response_history = respond(user_message, history[:-1])
            bot_message = response_history[-1][1]
            
            # Simulate typing effect
            for i in range(min(len(bot_message), 10)):
                time.sleep(0.05)
                history[-1][1] = bot_message[:i*len(bot_message)//10]
                yield history
                
            history[-1][1] = bot_message
            status.update("Ready")
            yield history
            
        except Exception as e:
            history[-1][1] = f"I'm sorry, I encountered an error: {str(e)}"
            status.update("Error occurred. Ready for new input.")
            yield history
    
    # Clear conversation function
    def clear_conversation():
        """Clear the conversation history."""
        global session_id
        session_id = str(uuid.uuid4())  # Generate new session ID
        return [], "Conversation cleared. Ready for new input."
    
    # Connect UI components to functions
    msg.submit(user_input, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot_response, chatbot, chatbot
    )
    
    submit_btn.click(user_input, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot_response, chatbot, chatbot
    )
    
    clear_btn.click(clear_conversation, None, [chatbot, status], queue=False)
    
    # Footer
    gr.HTML(footer_html)

if __name__ == "__main__":
    # Get the frontend port from environment or use default
    from app.config import FRONTEND_PORT
    port = int(FRONTEND_PORT) if FRONTEND_PORT else 7862
    
    # Ensure all required static files exist
    Path(static_dir).mkdir(exist_ok=True)
    
    # Create a placeholder avatar if it doesn't exist
    avatar_path = os.path.join(static_dir, "assistant-avatar.png")
    if not os.path.exists(avatar_path):
        print(f"Note: Assistant avatar not found at {avatar_path}. Using default.")
    
    # Launch the app with enhanced settings
    demo.launch(
        server_name="127.0.0.1",
        server_port=port,
        share=False,
        favicon_path=os.path.join(static_dir, "favicon.ico") if os.path.exists(os.path.join(static_dir, "favicon.ico")) else None,
        allowed_paths=[static_dir],
        show_api=False,  # Hide API docs for the demo
        show_error=True  # Show detailed errors during development
    )
    
    print(f"\n✨ AI Travel Assistant is running at http://127.0.0.1:{port}")
    print("Ready for the investor demo!")
