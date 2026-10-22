from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

# --- User Schemas ---
class UserCreate(BaseModel):
    """Validates incoming json payload when a new user registers."""

    email: EmailStr # Ensures valid email format string
    password: str # Plaintext password string provided by user

class UserResponse(BaseModel):
    """Structures outbound user data to clients (excludes passwords for security)"""

    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True # Allows Pydantic to read data from ORM models directly from SQLAlchemy 

# -- Token Schemas --
class Token(BaseModel):
    """Structures the JWT access token response return upon successful login""" 

    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Structures the decoded payload extracted from a JWT token."""

    email: Optional[str] = None

# --- Card Schemas ---
class CardCreate(BaseModel):
    """Validates incoming json payload when a new card is created."""
            
    recipient_email: EmailStr # Ensures valid email format string
    title: str # Title of of the birthday card
    message_body: str # Main text body of the birthday card
    template_style: Optional[int] = "default" # Optional template ID for card design
    scheduled_date: datetime # Date and time when the card is scheduled to be sent

class CardResponse(BaseModel):
    """Structures outboud card data to clients (excludes sensitive information)."""

    uuid: str # Public UUID slug for unqiue sharing links
    #sender_id: Optional[int] # ID of the user who sent the card (nullable for guest senders)
    recipient_email: EmailStr # Email address of the card recipient
    title: str # Greeting title of the card
    message_body: str # Main text body of the card
    template_style: Optional[int] = "default" # Optional template ID for card design
    scheduled_date: datetime # Date and time when the card is scheduled to be sent
    status: str # Delivery status: pending, sent, failed, etc.
    created_at: datetime # Timestamp of when the card was created

    class Config:
        from_attributes = True 
            