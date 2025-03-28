# Room Booking AI

## Demo

![AI Room booking chatbot - Demo](demo.gif)

## Project Overview

This is an AI-powered room booking chatbot built with Groq LLM, FastAPI, and Streamlit. The chatbot helps users book meeting rooms by understanding natural language requests and providing appropriate responses.

## Features

- Natural language understanding for room booking requests
- Room availability checking
- Room recommendation based on requirements
- Booking confirmation with unique reference numbers
- User-friendly chat interface

## Project Structure

```
├── .env                  # Environment variables (API keys)
├── README.md             # Project documentation
├── demo.gif              # Demo animation
├── requirements.txt      # Project dependencies
└── src/                  # Source code
    ├── api.py            # FastAPI backend
    ├── chatbot.py        # Chatbot core logic
    └── streamlit_app.py  # Streamlit frontend
```

## Setup Instructions

1. Clone this repository
2. Create a `.env` file with your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key
   GROQ_MODEL=mixtral-8x7b-32768
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI backend:
   ```bash
   cd src
   uvicorn api:app --reload
   ```
5. In a new terminal, start the Streamlit frontend:
   ```bash
   cd src
   streamlit run streamlit_app.py
   ```

## Usage

Once both the backend and frontend are running, open your browser to the Streamlit URL (typically http://localhost:8501). You can then interact with the chatbot by typing natural language requests like:

- "I need to book a meeting room for 10 people tomorrow at 2pm"
- "What rooms are available on Friday?"
- "I need a room with video conferencing facilities"

The chatbot will process your request and provide appropriate responses.
#   r o o m _ b o o k i n g _ a i  
 