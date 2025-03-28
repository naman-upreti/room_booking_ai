
# **🏢 Room Booking AI Chatbot**  

AI-powered chatbot for **seamless meeting room booking**, built with **Groq LLM, FastAPI, and Streamlit**.  

## **🚀 Features**  

✔️ **Natural Language Understanding** – Users can type requests in simple language (e.g., “Book a room for 5 people tomorrow at 10 AM”).  
✔️ **Room Availability Checking** – The chatbot checks which rooms are available based on the requested date and time.  
✔️ **Room Recommendations** – Suggests rooms based on the number of people, required facilities, and location.  
✔️ **Instant Booking Confirmation** – Generates unique booking reference numbers.  
✔️ **User-Friendly Chat Interface** – Interactive **Streamlit-powered UI** for easy interaction.  

## **📂 Project Structure**  

```
room-booking-ai/
│── .env                  # Environment variables (API keys)
│── README.md             # Project documentation
│── demo.gif              # Demo animation (example interaction)
│── requirements.txt      # Project dependencies
│
└── src/                  # Source code
    ├── api.py            # FastAPI backend for chatbot API
    ├── chatbot.py        # Chatbot logic (room booking processing)
    ├── streamlit_app.py  # Streamlit frontend (user chat interface)
```

---

## **🔧 Setup & Installation**  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/your-username/room-booking-ai.git
cd room-booking-ai
```

### **2️⃣ Set Up Environment Variables**  
Create a **`.env`** file in the root folder and add your **Groq API Key**:  
```ini
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=mixtral-8x7b-32768
```
> ⚠️ **Make sure to replace `your_groq_api_key` with your actual API key.**  

### **3️⃣ Install Dependencies**  
Run the following command:  
```bash
pip install -r requirements.txt
```
> If you face issues due to spaces in file paths, try running the command inside the project directory.

---

## **🖥️ Running the Project**  

### **1️⃣ Start the FastAPI Backend**  
```bash
cd src
uvicorn api:app --reload
```
📌 **By default, the API runs on** `http://127.0.0.1:8000`  

🔹 **Check API documentation** at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  

🔹 **Test API response** for available rooms:  
[http://127.0.0.1:8000/rooms](http://127.0.0.1:8000/rooms)  

---

### **2️⃣ Start the Streamlit Frontend**  
In a **new terminal**, run:  
```bash
cd src
streamlit run streamlit_app.py
```
📌 **The frontend will be available at**: [http://localhost:8501](http://localhost:8501)  

---

## **💬 Usage Examples**  

Once the chatbot is running, open the UI and type natural language queries:  

🗣️ **Example User Queries:**  
- **"I need to book a meeting room for 10 people tomorrow at 2 PM."**  
- **"What rooms are available on Friday?"**  
- **"I need a room with a projector and whiteboard."**  

---

## **🛠️ Troubleshooting & Fixes**  

### **✅ Issue: "ModuleNotFoundError: No module named 'groq'"**  
🔹 **Fix**: Install the missing package  
```bash
pip install groq
```

### **✅ Issue: FastAPI Server Port Conflict (8000 Already in Use)**  
🔹 **Fix**: Change the port when starting FastAPI  
```bash
uvicorn api:app --reload --port 8080
```

### **✅ Issue: Streamlit App Not Opening in Browser**  
🔹 **Fix**: Manually open [http://localhost:8501](http://localhost:8501)  

---

## **🤝 Contributing**  

💡 Found a bug? Have an improvement idea? Feel free to **fork** this repo and submit a **pull request**!  

---

## **📜 License**  
This project is licensed under the **MIT License**.  

---

### **🌟 If you found this useful, give it a ⭐ on GitHub!** 🚀  

---

This README ensures **clarity, easy installation, and smooth usage** of your **Room Booking AI** chatbot. Let me know if you want any modifications! 😊
