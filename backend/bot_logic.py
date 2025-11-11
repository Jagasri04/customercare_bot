# bot_logic.py
from database import engine
from models import Policy
from sqlmodel import Session
import re

# Store user context (policy number, awaiting input, etc.)
user_context = {}

def get_bot_reply(user_message, user_id="default"):
    msg = user_message.lower().strip()

    # Initialize context for user
    if user_id not in user_context:
        user_context[user_id] = {"awaiting_policy_number": False}

    context = user_context[user_id]

    # Step 1: If awaiting policy number
    if context.get("awaiting_policy_number"):
        # Policy number assumed numeric (digits)
        if re.fullmatch(r"\d+", msg):
            policy_number = int(msg)
            with Session(engine) as session:
                policy = session.get(Policy, policy_number)
                context["awaiting_policy_number"] = False
                if policy:
                    return (f"Policy {policy.policy_number} for {policy.customer_name}:\n"
                            f"Due date: {policy.due_date}\nAmount: {policy.amount}\n"
                            "Do you want any other details?")
                else:
                    return "Policy not found. Please check your policy number."
        else:
            return "That doesn't look like a valid policy number. Please enter the numeric policy number."

    # Step 2: Greeting
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
    if any(greet in msg for greet in greetings):
        return "Hello! Welcome to our customer care. How can I help you today?"

    # Step 3: Policy related queries
    if "policy" in msg or "policy details" in msg or "policy due" in msg:
        context["awaiting_policy_number"] = True
        return "Please provide your policy number so I can fetch the details."

    # Step 4: Bill or payment queries
    if "bill" in msg or "payment" in msg:
        return ("Your bill is usually due on the 15th of every month. "
                "You can also check your account for the exact date or pay online.")

    # Step 5: Issue / complaint queries
    if any(keyword in msg for keyword in ["issue", "problem", "error", "payment issue", "website issue"]):
        return "I'm sorry to hear that. Can you please describe the issue in detail so we can help?"

    # Step 6: Agent request
    if "agent" in msg or "contact" in msg:
        return ("You can contact our agent directly:\n"
                "Phone: +1-555-123-4567\n"
                "Email: support@company.com")

    # Step 7: Thank you / end of conversation
    if any(keyword in msg for keyword in ["thank", "thanks"]):
        return "Thank you for using our service! Please rate your chat experience from 1 to 5 ⭐⭐⭐⭐⭐"

    # Step 8: Fallback response
    return ("Sorry, I did not understand that. "
            "You can ask to contact an agent for further assistance by typing 'agent'.")
