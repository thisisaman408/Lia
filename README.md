# LIA Plus - Backend

This is the brain behind **LIA Plus**. It's a Python-based API built with **FastAPI** that handles the natural language processing, sentiment analysis, and conversation management.

The core idea here isn't just to return text, but to *understand* it. I implemented a hybrid engine that uses both rule-based heuristics (VADER) and dynamic context adjustments. There is also a reinforcement learning loop where the system accepts user feedback to correct its sentiment labels.

## Tech Stack

*   **FastAPI**: For a high-performance, easy-to-document API.
*   **PostgreSQL + SQLAlchemy**: For persistent storage of conversations and message history.
*   **VADER + Custom Heuristics**: A custom-tuned NLP engine for sentiment detection.
*   **Groq API**: Integrated for generating human-like responses when needed.

## Key Components

*   **`engine.py`**: The "Custom Linguistic Engine". It builds on VADER but adds domain-specific rules (like handling slang or crisis terms) to be smarter than a standard library.
*   **`orchestrator.py`**: Manages the flow. It takes user input, analyzes sentiment, decides on a response, and saves everything.
*   **`database.py`**: Handles the connection to PostgreSQL and manages schema migrations.
*   **`storage.py`**: The data layer that saves and retrieves chat history.

## Setup & Running

1.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
2.  Install requirements:
    ```bash
    pip install -r requirements.txt
    ```
3.  Set up your `.env` file with `DATABASE_URL` and `GROQ_API_KEY`.
4.  Run the server:
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

## API Endpoints

*   `POST /chat`: Send a message and get a response.
*   `GET /conversations`: Get a list of past chat sessions.
*   `GET /history/{id}`: Load full history for a specific chat.
*   `POST /feedback`: Correct a sentiment label (this feeds into the learning system).

I wrote this code to be clean and modular, following "Separation of Concerns" so logic isn't mixed together.
