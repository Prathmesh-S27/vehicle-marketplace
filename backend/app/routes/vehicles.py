from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..models.vehicle import Vehicle
from ..schemas.vehicle_schema import (
    VehicleCreate, 
    VehicleUpdate, 
    VehicleResponse, 
    VehicleSearchParams
)
from ..services.vehicle_service import VehicleService
from ..utils.image_upload import ImageUploadService

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.post("/", response_model=VehicleResponse)
def create_vehicle(
    vehicle: VehicleCreate, 
    db: Session = Depends(get_db)
):
    """
    Create a new vehicle listing
    """
    try:
        created_vehicle = VehicleService.create_vehicle(db, vehicle)
        return created_vehicle
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{vehicle_id}/upload-images")
def upload_vehicle_images(
    vehicle_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload images for a specific vehicle
    """
    try:
        # Validate vehicle exists
        vehicle = VehicleService.get_vehicle_by_id(db, vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        
        # Upload images
        uploaded_images = ImageUploadService.upload_multiple_images(
            files, 
            upload_dir="/path/to/vehicle/images"
        )
        
        # Update vehicle with new images
        updated_vehicle = VehicleService.add_vehicle_images(
            db, 
            vehicle_id, 
            uploaded_images
        )
        
        return {"images": uploaded_images}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/search", response_model=List[VehicleResponse])
def search_vehicles(
    db: Session = Depends(get_db),
    vehicle_type: Optional[str] = None,
    model: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    """
    Search vehicles with optional filters
    """
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
    """
    Get vehicle details by ID
    """
    vehicle = VehicleService.get_vehicle_by_id(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@router.put("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(
    vehicle_id: int,
    vehicle_update: VehicleUpdate,
    db: Session = Depends(get_db)
):
    """
    Update vehicle listing
    """
    try:
        updated_vehicle = VehicleService.update_vehicle(
            db, 
            vehicle_id, 
            vehicle_update
        )
        return updated_vehicle
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{vehicle_id}")
def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete vehicle listing
    """
    try:
        VehicleService.delete_vehicle(db, vehicle_id)
        return {"message": "Vehicle deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
