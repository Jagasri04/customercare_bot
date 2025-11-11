# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bot_logic import get_bot_reply
from database import create_db_and_tables, get_session, engine
from models import Message, Policy
from sqlmodel import Session

# Initialize app
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables
create_db_and_tables()

# Pydantic models
class UserMessage(BaseModel):
    message: str

class Rating(BaseModel):
    rating: int

# Chat endpoint
@app.post("/chat")
def chat(msg: UserMessage):
    user_id = "default"  # single user for now
    reply = get_bot_reply(msg.message, user_id=user_id)

    # Save to DB
    with Session(engine) as session:
        message_obj = Message(user_message=msg.message, bot_reply=reply)
        session.add(message_obj)
        session.commit()

    return {"reply": reply}

# Rating endpoint
@app.post("/rating")
def submit_rating(r: Rating):
    # Save rating to DB if you want
    print(f"User rated: {r.rating}")
    return {"message": "Thanks for your feedback!"}

# Policy lookup endpoint
@app.get("/policy/{policy_number}")
def get_policy(policy_number: str):
    with Session(engine) as session:
        policy = session.get(Policy, policy_number)
        if policy:
            return {
                "policy_number": policy.policy_number,
                "customer_name": policy.customer_name,
                "due_date": policy.due_date,
                "amount": policy.amount,
            }
        else:
            return {"message": "Policy not found."}

# Agent contact endpoint
@app.get("/agent")
def agent_contact():
    return {
        "name": "John Doe",
        "phone": "+1-555-123-4567",
        "email": "support@company.com"
    }
