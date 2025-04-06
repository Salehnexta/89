# AI Travel Assistant Demo

An intelligent travel assistant demo that helps users plan trips, book flights, and find accommodations using AI-powered conversations.

## Tech Stack

- Backend: FastAPI + LangGraph
- Frontend: Gradio
- AI: Google Gemini Pro via LangChain
- Database: SQLite

## Setup

1. Create virtual environment:
```bash
python -m venv venv
```

2. Activate virtual environment:
- Windows: `venv\Scripts\activate`
- Unix/MacOS: `source venv/bin/activate`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file in project root and add:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

## Running the Application

1. Start the backend server:
```bash
uvicorn app.main:app --reload --port 8000
```

2. In a new terminal, start the frontend:
```bash
python frontend/gradio_app.py
```

3. Open the Gradio interface URL shown in the terminal (typically http://127.0.0.1:7860)
