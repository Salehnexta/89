# AI Travel Assistant

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/Salehnexta/89/releases/tag/v1.0.0)

An intelligent travel assistant that helps users plan trips, book flights, and find accommodations using AI-powered conversations. This project is designed to demonstrate advanced natural language understanding and contextual awareness for travel planning scenarios.

## Features

- **Intelligent Conversation** - Context-aware dialog for natural travel planning
- **Intent Classification** - Accurately identifies user needs (flight search, hotel booking, etc.)
- **Travel Draft Management** - Creates and updates travel package drafts based on user preferences
- **Flight & Hotel Search** - Simulated search functionality for travel options
- **General Travel Information** - Provides destination information, travel tips, and recommendations

## Architecture

This project implements a state-of-the-art workflow using LangGraph for managing conversational state and complex decision trees:

```
User Input → Intent Classification → Task-Specific Nodes → Response Generation
```

## Tech Stack

- **Backend**: FastAPI + LangGraph
- **Frontend**: Gradio for clean, interactive UI
- **AI Models**: DeepSeek API (primary), with Google Gemini Pro fallback
- **State Management**: LangGraph for complex conversation flow
- **Database**: SQLite for conversation storage

## Setup

### Prerequisites

- Python 3.8+
- DeepSeek API key (or Google API key as fallback)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Salehnexta/89.git
   cd 89
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Unix/MacOS
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create environment variables:
   ```bash
   cp .env.template .env
   ```

5. Add your API keys to the `.env` file:
   ```
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here  # Optional fallback
   ```

## Running the Application

### Backend API Server

```bash
python -m app.main
# or alternatively
uvicorn app.main:app --reload --port 8000
```

### Frontend Interface

In a new terminal window:

```bash
python -m frontend.gradio_app
```

Open the provided URL in your browser (typically http://127.0.0.1:7860).

### Test Mode

For testing or demonstration purposes:

```bash
python test_demo_flow.py
```

## Project Structure

```
├── app/                  # Core application code
│   ├── config.py         # Configuration handling
│   ├── database.py       # Database operations
│   ├── language_model.py # LLM integration
│   ├── main.py           # FastAPI application
│   ├── mock_tools.py     # Mock flight/hotel search
│   ├── nodes.py          # LangGraph workflow nodes
│   ├── state.py          # State management
│   └── workflow.py       # LangGraph workflow definition
├── frontend/            # User interface
│   └── gradio_app.py     # Gradio interface
├── tests/               # Test suite
├── .env.template        # Environment template
├── requirements.txt     # Dependencies
└── README.md            # Documentation
```

## Testing

Run tests with:

```bash
python -m pytest
```

## Development Notes

- The application uses mock data for flights and hotels during demonstration
- For best results, ensure your DeepSeek API key has sufficient quota
- Conversation history is stored in a local SQLite database

## Future Improvements

- Integration with real travel API providers
- Authentication system for user accounts
- Expanded language support
- Mobile application interface

---

*This project was created as a demonstration of AI-powered travel planning capabilities.*