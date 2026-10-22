from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Card, User
from app.schemas import CardCreate, CardResponse
from app.auth import get_current_user

# Initialize an APIRouter for card-related routes
router = APIRouter(prefix="/cards", tags=["Cards"])

@router.post(
    "/", response_model=CardResponse, status_code=status.HTTP_201_CREATED
)

def create_card(
    card: CardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Allows an authenticated user to create and schedule a birthday card."""
    # Create a new card instance with the provided data and associate it with the current user
    new_card = Card(
        sender_id=current_user.id,
        recipient_email=card.recipient_email,
        title=card.title,
        message_body=card.message_body,
        template_style=card.template_style,
        scheduled_date=card.scheduled_date
    )
    # Add the new card to the database session and commit the transaction
    db.add(new_card)
    db.commit()
    db.refresh(new_card) # Refresh the instance to get the updated data from the database
    return new_card # Return the newly created card data as a response

@router.get("/vault", response_model=List[CardResponse])
def get_user_vault(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves all cards sent TO the logged-in user's email address."""
    # Query the database for all cards associated with the currents user's ID and retrun"""
    cards = (
        db.query(Card)
        .filter(Card.recipient_email == current_user.email)
        .all() 
    )
    return cards # Return the list of cards as a response

@router.get("/{card_uuid}", response_model=CardResponse)
def view_public_card(card_uuid:str , db: Session = Depends(get_db)):
    """Public endpoint allowing anyone with the unique UUID slug to view the card."""
    card = db.query(Card).filter(Card.uuid == card_uuid).first()
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found",
        )
    return card # Return the card data as a response