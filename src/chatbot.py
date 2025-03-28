from groq import Groq
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Optional, Tuple, Any

class RoomBookingChatbot:
    def __init__(self, api_key: str, model: str):
        self.client = Groq(api_key=api_key)
        self.model = model
        self.rooms = self._load_rooms()
        self.bookings = {}
        
        # Configure logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger("RoomBookingChatbot")

    def _load_rooms(self) -> Dict:
        return {
            'conference_a': {
                'name': 'Conference Room A',
                'capacity': 20,
                'facilities': ['projector', 'whiteboard', 'video_conferencing'],
                'location': 'First Floor'
            },
            'meeting_b': {
                'name': 'Meeting Room B',
                'capacity': 10,
                'facilities': ['whiteboard', 'video_conferencing'],
                'location': 'Second Floor'
            },
            'board_room': {
                'name': 'Board Room',
                'capacity': 15,
                'facilities': ['projector', 'video_conferencing', 'catering'],
                'location': 'Third Floor'
            }
        }

    async def process_booking_request(self, user_request: str) -> Dict:
        """Process a booking request and return appropriate response"""
        response = await self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": self._get_system_prompt()
                },
                {
                    "role": "user",
                    "content": user_request
                }
            ],
            model=self.model,
            temperature=0.7,
        )
        
        return self._parse_response(response.choices[0].message.content)

    def _get_system_prompt(self) -> str:
        rooms_info = json.dumps(self.rooms, indent=2)
        bookings_info = json.dumps(self.bookings, indent=2) if self.bookings else "No current bookings"
        
        return f"""You are a professional room booking assistant. Help users book meeting rooms.
Available rooms and their details are:
{rooms_info}

Current bookings:
{bookings_info}

Extract the following information from user requests:
- Required date and time (use YYYY-MM-DD format for dates)
- Number of participants
- Required facilities
- Duration of meeting (in minutes)
- Any special requirements

When suggesting rooms:
1. Check if the room has enough capacity for the participants
2. Ensure the room has the requested facilities
3. Verify the room is available at the requested time

Respond in JSON format with the following structure:
{{
    "intent": "book_room/check_availability/room_info/cancel_booking",
    "extracted_info": {{
        "date": "YYYY-MM-DD",
        "time": "HH:MM",
        "participants": number,
        "duration": number_in_minutes,
        "facilities": ["facility1", "facility2"],
        "special_requirements": "any special notes"
    }},
    "suggested_room": "room_id",
    "response_message": "your response to user"
}}
"""

    def _parse_response(self, response: str) -> Dict:
        try:
            self.logger.info(f"Parsing response: {response[:100]}...")
            parsed = json.loads(response)
            
            # Handle different intents
            if parsed['intent'] == 'book_room':
                return self._handle_booking(parsed)
            elif parsed['intent'] == 'check_availability':
                return self._check_availability(parsed)
            elif parsed['intent'] == 'cancel_booking':
                return self._handle_cancellation(parsed)
            
            # Default case for other intents like room_info
            return parsed
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON parsing error: {str(e)}")
            return {
                "status": "error",
                "message": "Failed to process request. The response couldn't be parsed correctly."
            }
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            return {
                "status": "error",
                "message": f"An unexpected error occurred: {str(e)}"
            }

    def _handle_booking(self, parsed_response: Dict) -> Dict:
        """Handle room booking requests"""
        self.logger.info(f"Handling booking request: {parsed_response}")
        
        # Extract booking information
        extracted_info = parsed_response.get('extracted_info', {})
        suggested_room = parsed_response.get('suggested_room')
        
        # Validate room availability
        if not suggested_room or suggested_room not in self.rooms:
            return {
                "status": "error",
                "message": "No suitable room found or invalid room suggested",
                "response_message": "I couldn't find a suitable room for your requirements. Could you please adjust your criteria?"
            }
            
        # Check if the room is available at the requested time
        is_available, conflict_reason = self._is_room_available(suggested_room, extracted_info)
        if not is_available:
            return {
                "status": "unavailable",
                "message": conflict_reason,
                "response_message": f"I'm sorry, but {self.rooms[suggested_room]['name']} is not available at that time. {conflict_reason}"
            }
        
        # Generate confirmation number
        confirmation_number = "BOK" + datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Store booking in the system
        booking_record = {
            "confirmation_number": confirmation_number,
            "room_id": suggested_room,
            "room_name": self.rooms[suggested_room]['name'],
            "date": extracted_info.get('date'),
            "time": extracted_info.get('time'),
            "duration": extracted_info.get('duration', 60),
            "participants": extracted_info.get('participants'),
            "facilities_requested": extracted_info.get('facilities', []),
            "special_requirements": extracted_info.get('special_requirements', ''),
            "booking_time": datetime.now().isoformat()
        }
        
        # Add to bookings dictionary
        self.bookings[confirmation_number] = booking_record
        
        return {
            "status": "success",
            "booking_details": booking_record,
            "confirmation_number": confirmation_number,
            "response_message": f"Great! I've booked {self.rooms[suggested_room]['name']} for you on {extracted_info.get('date')} at {extracted_info.get('time')}. Your confirmation number is {confirmation_number}."
        }
        
    def _check_availability(self, parsed_response: Dict) -> Dict:
        """Check room availability"""
        self.logger.info(f"Checking availability: {parsed_response}")
        
        extracted_info = parsed_response.get('extracted_info', {})
        suggested_room = parsed_response.get('suggested_room')
        
        available_rooms = []
        for room_id, room_details in self.rooms.items():
            if suggested_room and room_id != suggested_room:
                continue
                
            is_available, reason = self._is_room_available(room_id, extracted_info)
            if is_available:
                available_rooms.append({
                    "room_id": room_id,
                    "name": room_details['name'],
                    "capacity": room_details['capacity'],
                    "facilities": room_details['facilities'],
                    "location": room_details['location']
                })
        
        return {
            "status": "success",
            "available_rooms": available_rooms,
            "response_message": parsed_response.get('response_message', "Here are the available rooms for your criteria.")
        }
    
    def _handle_cancellation(self, parsed_response: Dict) -> Dict:
        """Handle booking cancellation"""
        self.logger.info(f"Handling cancellation request: {parsed_response}")
        
        # Extract confirmation number from the response
        extracted_info = parsed_response.get('extracted_info', {})
        confirmation_number = extracted_info.get('confirmation_number')
        
        if not confirmation_number or confirmation_number not in self.bookings:
            return {
                "status": "error",
                "message": "Invalid or missing confirmation number",
                "response_message": "I couldn't find a booking with that confirmation number. Please check and try again."
            }
        
        # Get booking details before removing
        booking_details = self.bookings[confirmation_number]
        
        # Remove the booking
        del self.bookings[confirmation_number]
        
        return {
            "status": "success",
            "cancelled_booking": booking_details,
            "response_message": f"I've cancelled your booking for {booking_details['room_name']} on {booking_details['date']} at {booking_details['time']}. Your confirmation number was {confirmation_number}."
        }
    
    def _is_room_available(self, room_id: str, booking_info: Dict) -> Tuple[bool, str]:
        """Check if a room is available for the requested time"""
        # For now, we'll implement a simple availability check
        # In a real system, this would check against a database of bookings
        
        # Check if the room exists
        if room_id not in self.rooms:
            return False, "Room does not exist"
            
        # Check if the room has enough capacity
        participants = booking_info.get('participants', 0)
        if participants > self.rooms[room_id]['capacity']:
            return False, f"Room capacity ({self.rooms[room_id]['capacity']}) is less than required ({participants})"
            
        # Check if the room has the required facilities
        required_facilities = booking_info.get('facilities', [])
        for facility in required_facilities:
            if facility not in self.rooms[room_id]['facilities']:
                return False, f"Room does not have the required facility: {facility}"
                
        # Check for time conflicts with existing bookings
        requested_date = booking_info.get('date')
        requested_time = booking_info.get('time')
        requested_duration = booking_info.get('duration', 60)  # Default to 60 minutes
        
        if not requested_date or not requested_time:
            return True, ""  # If no specific time requested, assume it's available
            
        # Convert requested time to datetime object
        try:
            requested_datetime = datetime.strptime(f"{requested_date} {requested_time}", "%Y-%m-%d %H:%M")
            requested_end_time = requested_datetime + timedelta(minutes=requested_duration)
            
            # Check against existing bookings
            for booking_id, booking in self.bookings.items():
                if booking['room_id'] != room_id:
                    continue
                    
                if booking['date'] == requested_date:
                    booking_time = datetime.strptime(f"{booking['date']} {booking['time']}", "%Y-%m-%d %H:%M")
                    booking_end_time = booking_time + timedelta(minutes=booking['duration'])
                    
                    # Check for overlap
                    if (requested_datetime < booking_end_time and requested_end_time > booking_time):
                        return False, f"Time conflict with existing booking (Confirmation: {booking_id})"
        except ValueError:
            self.logger.error(f"Date/time parsing error for {requested_date} {requested_time}")
            return False, "Invalid date or time format"
            
        return True, ""