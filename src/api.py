from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# Fix the import statement
from .chatbot import RoomBookingChatbot
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("room-booking-api")

app = FastAPI(title="Room Booking API", description="API for room booking assistant")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chatbot
chatbot = RoomBookingChatbot(
    api_key=os.getenv('GROQ_API_KEY'),
    model=os.getenv('GROQ_MODEL', 'mixtral-8x7b-32768')
)

# Middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

class ChatRequest(BaseModel):
    message: str

@app.post("/chat", response_description="Chatbot response")
async def chat(request: ChatRequest):
    try:
        logger.info(f"Received chat request: {request.message[:50]}...")
        response = await chatbot.process_booking_request(request.message)
        logger.info(f"Chat response generated successfully")
        return response
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process request: {str(e)}")

@app.get("/rooms", response_description="List of available rooms")
async def get_rooms():
    try:
        logger.info("Fetching room information")
        return chatbot.rooms
    except Exception as e:
        logger.error(f"Error fetching rooms: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch rooms: {str(e)}")

@app.get("/bookings", response_description="List of current bookings")
async def get_bookings():
    try:
        logger.info("Fetching booking information")
        return chatbot.bookings
    except Exception as e:
        logger.error(f"Error fetching bookings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch bookings: {str(e)}")

@app.get("/health", response_description="API health check")
async def health_check():
    return {"status": "healthy", "message": "Room Booking API is running"}