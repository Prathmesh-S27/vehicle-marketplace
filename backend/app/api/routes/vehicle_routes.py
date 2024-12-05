from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ...database import get_db
from ...models.vehicle import Vehicle
from ...schemas.vehicle_schema import (
    VehicleCreate, 
    VehicleResponse, 
    VehicleSearchParams
)
from ...services.vehicle_service import VehicleService

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.post("/", response_model=VehicleResponse)
def create_vehicle(
    vehicle: VehicleCreate, 
    db: Session = Depends(get_db)
):
    return VehicleService.create_vehicle(db, vehicle)

@router.get("/search", response_model=List[VehicleResponse])
def search_vehicles(
    db: Session = Depends(get_db),
    vehicle_type: Optional[str] = None,
    model: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    search_params = VehicleSearchParams(
        vehicle_type=vehicle_type,
        model=model,
        min_price=min_price,
        max_price=max_price
    )
    return VehicleService.search_vehicles(db, search_params)

@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db)
):
    vehicle = VehicleService.get_vehicle_by_id(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle
