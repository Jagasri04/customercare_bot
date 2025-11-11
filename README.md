# Customer Care Chatbot

This is a **FastAPI-based customer care chatbot** with a web interface.  
It supports:

- Basic greetings
- Policy lookup by policy number
- Payment issue guidance
- Contacting an agent with phone number
- Star rating feedback system

---

## **Features**

1. **Chat Interface**  
   Users can send messages, get replies, and see a chat-like UI in their browser.

2. **Policy Details**  
   Users can enter a 6-digit policy number to get the status, expiration date, and premium due.

3. **Payment Issues**  
   Bot instructs users to retry after some time or contact the agent.

4. **Agent Contact**  
   Displays agent phone number for direct support.

5. **Feedback**  
   After conversation, users can rate the chat experience using stars.

---

## **Tech Stack**

- Python 3.11+
- FastAPI
- SQLModel / SQLite
- HTML, CSS, JavaScript
- Uvicorn (ASGI server)

---

## **Setup Instructions**

1. Clone the repository:

```bash
git clone https://github.com/yourusername/customer-care-chatbot.git
cd customer-care-chatbot
