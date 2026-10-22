# Import built-in uuid to generate unique secure public card slugs
import uuid

#Import datetime for timestamp generatiion
from datetime import datetime

# Import database Base class from our local database.py file to map our models to the database
from app.database import Base

# Import SQLAlchemy's column types and constraints
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

class User(Base):
    """SQLAlchemy model representing a registered user account."""

    __tablename__ = "users" # Name of the table in SQL database

    id = Column( 
        Integer, primary_key=True, index=True 
    ) # Unique auto-incrementing integer ID
    email = Column(
        String, unique=True, index=True, nullable=False
    ) # Unique email login, indexed for fast lookups, cannot be null
    hashed_password = Column(
        String, nullable=False
    ) # Stores securely hashed password, cannot be null
    created_at = Column(
        DateTime, default=datetime.utcnow
    ) # Timestamp of account creation

    # Establishes an ORM relationship linking user to cards they created
    sent_cards = relationship(
        "Card", back_populates="sender", foreign_keys="Card.sender_id"
    )

class Card(Base):
    """SQLAchemy model representing a scheduled birthday card."""

    __tablename__= "cards"  # Name of the table in the SQL database

    id = Column(
        Integer, primary_key=True, index=True
    ) # Internal integer primary key

    uuid= Column(
        String,
        unique=True,
        index=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    ) # Public secure UUID slug for unique sharing links

    sender_id= Column(
        Integer, ForeignKey("users.id"), nullable=True
    ) # Foreign key linking to user (nullable for guest senders)
    recipient_email = Column(
        String, index=True, nullable=False
    ) # Email address of the card recipient
    title = Column(String, nullable=False) # Greeting title of the card
    message_body = Column(Text, nullable=False) # Main text body
    template_style = Column(
        String, default="default"
    ) # Visual template theme identifier
    scheduled_date = Column(
        DateTime, nullable=False
    ) # Date/time when card scheduled to deliver
    status = Column(
        String, default="pending"
    ) # Delivery status: pending, sent, failed, etc.
    created_at = Column(
        DateTime, default=datetime.utcnow
    ) # Timestamp when card was created

    # Inverse relationship linking back to the sender user object
    sender = relationship(
        "User", back_populates="sent_cards", foreign_keys=[sender_id]
    )

