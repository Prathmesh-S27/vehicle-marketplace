from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List

from ..models.vehicle import Vehicle
from ..schemas.vehicle_schema import VehicleCreate, VehicleSearchParams

class VehicleService:
    @staticmethod
    def create_vehicle(db: Session, vehicle: VehicleCreate):
        # Convert images list to comma-separated string
        images_str = ','.join(vehicle.images) if vehicle.images else ''
        
        db_vehicle = Vehicle(
            model=vehicle.model,
            type=vehicle.type,
            description=vehicle.description,
            price=vehicle.price,
            year=vehicle.year,
            seller_id=vehicle.seller_id,
            images=images_str
        )
        
        db.add(db_vehicle)
        db.commit()
        db.refresh(db_vehicle)
        
        return db_vehicle

    @staticmethod
    def search_vehicles(
        db: Session, 
        params: VehicleSearchParams
    ) -> List[Vehicle]:
        query = db.query(Vehicle)
        
        # Apply filters based on search parameters
        if params.vehicle_type:
            query = query.filter(Vehicle.type == params.vehicle_type)
        
        if params.model:
            query = query.filter(
                or_(
                    Vehicle.model.ilike(f"%{params.model}%")
                )
            )
        
        if params.min_price is not None:
            query = query.filter(Vehicle.price >= params.min_price)
        
        if params.max_price is not None:
            query = query.filter(Vehicle.price <= params.max_price)
        
        return query.all()

    @staticmethod
    def get_vehicle_by_id(db: Session, vehicle_id: int):
        return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
