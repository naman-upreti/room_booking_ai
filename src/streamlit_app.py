import streamlit as st
import requests
import json
from datetime import datetime

# Set up the page
st.set_page_config(page_title="Room Booking Assistant", layout="wide")

st.markdown("""
    <style>
        .stChatMessageUser { background-color: #D1ECF1; padding: 10px; border-radius: 10px; margin-bottom: 10px; }
        .stChatMessageAssistant { background-color: #F8F9FA; padding: 10px; border-radius: 10px; margin-bottom: 10px; }
        .stSidebar .block-container { padding: 20px; }
        .room-card { background-color: #F8F9FA; padding: 15px; border-radius: 10px; margin-bottom: 15px; }
        h1, h2, h3 { color: #2C3E50; }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

def get_rooms():
    try:
        response = requests.get("http://localhost:8000/rooms")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Error fetching rooms: {e}")
        return {}

# Page Title
st.title("🏢 Room Booking Assistant")
st.write("Effortlessly book meeting rooms with natural language!")

# Sidebar with room information
with st.sidebar:
    st.header("📌 Available Rooms")
    rooms = get_rooms()
    if rooms:
        for room_id, details in rooms.items():
            with st.container():
                st.markdown(f"""<div class='room-card'>
                <h3>{details['name']}</h3>
                <p><strong>Capacity:</strong> {details['capacity']} people</p>
                <p><strong>Location:</strong> {details['location']}</p>
                <p><strong>Facilities:</strong></p>
                <ul>
                {' '.join([f'<li>{facility}</li>' for facility in details['facilities']])}
                </ul>
                </div>""", unsafe_allow_html=True)
    else:
        st.warning("⚠️ No rooms available at the moment.")

# Chat Interface
st.write("### 💬 Chat with the Room Booking Assistant")

for message in st.session_state.messages:
    role_class = "stChatMessageUser" if message["role"] == "user" else "stChatMessageAssistant"
    st.markdown(f'<div class="{role_class}">{message["content"]}</div>', unsafe_allow_html=True)

if prompt := st.chat_input("How can I help you with room booking?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="stChatMessageUser">{prompt}</div>', unsafe_allow_html=True)

    # Get chatbot response
    with st.spinner("Processing your request..."):
        try:
            response = requests.post(
                "http://localhost:8000/chat",
                json={"message": prompt},
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            assistant_message = result.get("response_message", "I couldn't process your request.")
            
            # Display formatted response
            if "booking_details" in result:
                st.success("✅ Booking Confirmed!")
                with st.expander("View Booking Details"):
                    st.json(result["booking_details"])
                st.markdown(f'<div class="stChatMessageAssistant">{assistant_message}</div>', unsafe_allow_html=True)
            elif "available_rooms" in result:
                st.info("🔍 Room Availability")
                st.markdown(f'<div class="stChatMessageAssistant">{assistant_message}</div>', unsafe_allow_html=True)
                if result["available_rooms"]:
                    for room in result["available_rooms"]:
                        st.markdown(f"**{room['name']}** - Capacity: {room['capacity']} - Location: {room['location']}")
                else:
                    st.warning("No rooms match your criteria at the specified time.")
            elif "cancelled_booking" in result:
                st.info("🗑️ Booking Cancelled")
                st.markdown(f'<div class="stChatMessageAssistant">{assistant_message}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="stChatMessageAssistant">{assistant_message}</div>', unsafe_allow_html=True)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        except requests.exceptions.RequestException as e:
            st.error(f"🚨 Network error: {e}")
            st.session_state.messages.append({"role": "assistant", "content": f"Sorry, I encountered a network error: {e}"})
        except Exception as e:
            st.error(f"🚨 Error: {e}")
            st.session_state.messages.append({"role": "assistant", "content": f"Sorry, something went wrong: {e}"})