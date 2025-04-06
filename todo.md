# TODO List: AI Travel Assistant Investor Demo (Vibe Coding with Windsurf)

## Phase 1: Setup & Environment Configuration

-   [ ] **Initialize Project:** Create the main project directory.
-   [ ] **Setup Virtual Environment:**
    -   Create a Python virtual environment (e.g., `python -m venv venv`).
    * Activate the virtual environment.
-   [ ] **Install Core Dependencies:**
    -   Install necessary Python libraries: `pip install langgraph langchain langchain_google_genai fastapi uvicorn gradio requests python-dotenv` (add others as needed).
-   [ ] **Setup Windsurf:**
    * Ensure your Windsurf tool/environment is installed and configured according to its documentation.
-   [ ] **Configure API Keys:**
    * Obtain your Gemini API Key.
    * Create a `.env` file in the project root.
    * Use Vibe Coding/Windsurf to generate Python code (`config.py` or similar) to load the API key securely from the `.env` file using `python-dotenv`.
-   [ ] **Project Structure:**
    * Create basic folder structure (e.g., `/app` for backend, `/frontend` potentially, `/data` for SQLite DB, `/tests`).
-   [ ] **Version Control:**
    * Initialize Git repository (`git init`).
    * Create a `.gitignore` file (use Vibe Coding/Windsurf to generate a standard Python .gitignore).
    * Make the initial commit.

## Phase 2: Backend Development (FastAPI + LangGraph via Vibe Coding)

-   [ ] **Database Setup (SQLite - Demo):**
    -   Use Vibe Coding/Windsurf: "Generate Python code using sqlite3 module to create/connect to `demo_travel_app.db`. Define and create a simple table `conversations` (e.g., session_id TEXT, history TEXT)." (Keep schema minimal for demo).
-   [ ] **Define LangGraph State:**
    -   Use Vibe Coding/Windsurf: "Generate a Python dataclass or TypedDict `AgentState` suitable for LangGraph. Include fields for: `user_input` (str), `conversation_history` (list), `intent` (str), `parameters` (dict), `draft_package` (dict), `mock_flight_results` (list), `mock_hotel_results` (list), `final_response` (str)."
-   [ ] **Implement Mock Tools:**
    -   Use Vibe Coding/Windsurf: "Generate Python function `search_mock_flights(destination, date)` returning a hardcoded list of 2-3 mock flight dictionaries." (Specify example dict structure).
    -   Use Vibe Coding/Windsurf: "Generate Python function `search_mock_hotels(destination, date, num_guests)` returning a hardcoded list of 2-3 mock hotel dictionaries." (Specify example dict structure).
    -   (Optional) Use Vibe Coding/Windsurf: "Generate Python function `get_mock_general_info(topic, destination)` returning hardcoded answers for demo topics like weather or visa."
-   [ ] **Implement LangGraph Nodes:**
    -   Use Vibe Coding/Windsurf for each node (provide clear prompts):
        -   `UserInputProcessor`: Generate function: gets input, adds to `conversation_history` in state.
        -   `IntentClassifier`: Generate function: formats prompt for Gemini 1.5 Pro (using state's history/input), calls Gemini API via `langchain_google_genai`, parses response for intent/params, updates state.
        -   `DraftManager`: Generate function: reads intent/params from state, initializes or updates `draft_package` dict in state.
        -   `MockFlightSearchToolNode`: Generate function: gets params from state, calls `search_mock_flights`, updates `mock_flight_results` in state.
        -   `MockHotelSearchToolNode`: Generate function: gets params from state, calls `search_mock_hotels`, updates `mock_hotel_results` in state.
        -   `GeneralInfoHandlerNode`: Generate function: gets params/topic from state, calls `get_mock_general_info` or formats prompt for Gemini, updates state with answer (or add to `final_response` directly).
        -   `ResponseGeneratorNode`: Generate function: reads relevant fields from state (draft, results, history), formats final prompt for Gemini 1.5 Pro, calls Gemini API, updates `final_response` in state.
-   [ ] **Assemble LangGraph Graph:**
    -   Use Vibe Coding/Windsurf: "Generate Python code to import LangGraph and defined nodes/state."
    * Use Vibe Coding/Windsurf: "Generate code to instantiate the LangGraph `Workflow`."
    * Use Vibe Coding/Windsurf: "Generate code to add all defined nodes to the graph."
    * Use Vibe Coding/Windsurf: "Generate code to set the entry point node."
    * Use Vibe Coding/Windsurf: "Generate code to define conditional edges based on `intent` and state (e.g., `if intent == 'start_draft': go to DraftManager`)."
    * Use Vibe Coding/Windsurf: "Generate code to compile the LangGraph app (`app = workflow.compile()`)."
-   [ ] **Develop FastAPI Endpoint:**
    * Use Vibe Coding/Windsurf: "Generate basic FastAPI app setup in `main.py`."
    * Use Vibe Coding/Windsurf: "Generate a POST endpoint `/chat` that accepts JSON with `message` and `chat_history`."
    * Inside endpoint (Use Vibe Coding/Windsurf):
        * Generate code to prepare the initial state for LangGraph using request data.
        * Generate code to invoke the compiled LangGraph app: `result_state = compiled_graph.invoke(initial_state)`.
        * Generate code to extract the `final_response` from the `result_state`.
        * Generate code to return the response as JSON: `return {"response": final_response}`.

## Phase 3: Frontend Development (Gradio via Vibe Coding)

-   [ ] **Create Gradio App File:** Create `gradio_app.py`.
-   [ ] **Basic Gradio UI:**
    * Use Vibe Coding/Windsurf: "Generate Python code for a Gradio app using `gr.ChatInterface`." (Reference previous example).
    * Use Vibe Coding/Windsurf: "Customize the `title`, `description`, and `examples` for the investor demo."
-   [ ] **Implement Gradio `respond` Function:**
    * Use Vibe Coding/Windsurf: "Generate the `respond(message, chat_history)` function for Gradio."
    * Inside `respond` (Use Vibe Coding/Windsurf):
        * Generate code to prepare the JSON payload for FastAPI (message, history).
        * Generate code using `requests` to POST the payload to the FastAPI `/chat` endpoint (`http://127.0.0.1:8000/chat` typically).
        * Generate code to handle the JSON response from FastAPI.
        * Generate code to handle potential HTTP errors.
        * Generate code to append the user message and bot response to Gradio's `chat_history`.
        * Generate code to return the updated history for the UI.

## Phase 4: Integration & Testing

-   [ ] **Run Backend:** Start FastAPI: `uvicorn app.main:app --reload --port 8000` (adjust module path if needed).
-   [ ] **Run Frontend:** Start Gradio: `python gradio_app.py`.
-   [ ] **End-to-End Testing:**
    * Open Gradio URL in browser.
    * Test the main conversational flows outlined in the demo script.
    * Verify intent classification works for different inputs.
    * Verify mock flight/hotel data appears correctly in responses.
    * Check that conversation state (like the draft package) seems to be maintained across turns.
-   [ ] **Basic Unit Testing (Optional but Recommended):**
    * Use Vibe Coding/Windsurf: "Generate basic pytest unit tests for the mock tool functions (`search_mock_flights`, etc.)."
    * Use Vibe Coding/Windsurf: "Generate basic unit tests for any simple utility functions created."
-   [ ] **Debugging:** Address any errors or unexpected behavior found during testing. Refine Vibe Coding prompts or manually adjust code as needed.

## Phase 5: Demo Preparation

-   [ ] **Refine Mock Data:** Ensure mock data is realistic and relevant for the planned demo narrative.
-   [ ] **Finalize Gradio UI:** Polish titles, descriptions, examples.
-   [ ] **Prepare Demo Script:** Outline the exact conversation flow and features to showcase to investors.
-   [ ] **Practice Run:** Do a full run-through of the demo script using the application.
-   [ ] **Documentation (Basic):**
    * Use Vibe Coding/Windsurf: "Generate a simple README.md explaining the project purpose (Investor Demo), tech stack, and how to run the backend and frontend."
