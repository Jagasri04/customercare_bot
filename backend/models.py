# models.py
from sqlmodel import SQLModel, Field

class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_message: str
    bot_reply: str

class Policy(SQLModel, table=True):
    policy_number: str = Field(primary_key=True)
    customer_name: str
    due_date: str
    amount: float
