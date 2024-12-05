from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.contact_request import ContactRequest
from ..schemas.contact_request_schema import ContactRequestCreate, ContactRequestResponse
from ..services.contact_request_service import ContactRequestService

router = APIRouter(prefix="/contact-requests", tags=["Contact Requests"])

@router.post("/", response_model=ContactRequestResponse)
def create_contact_request(
    contact_request: ContactRequestCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new contact request for a vehicle
    """
    try:
        created_request = ContactRequestService.create_contact_request(
            db, 
            contact_request
        )
        return created_request
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/vehicle/{vehicle_id}", response_model=List[ContactRequestResponse])
def get_vehicle_contact_requests(
    vehicle_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all contact requests for a specific vehicle
    """
    contact_requests = ContactRequestService.get_vehicle_contact_requests(
        db, 
        vehicle_id
    )
    return contact_requests

@router.get("/user/{user_id}", response_model=List[ContactRequestResponse])
def get_user_contact_requests(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all contact requests made by a specific user
    """
    contact_requests = ContactRequestService.get_user_contact_requests(
        db, 
        user_id
    )
    return contact_requests
