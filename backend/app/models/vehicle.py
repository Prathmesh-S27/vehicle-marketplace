from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float)
    year = Column(Integer)
    seller_id = Column(Integer, ForeignKey("users.id"))
    
    # Images as a comma-separated string of URLs
    images = Column(Text)

    # Relationships
    seller = relationship("User", back_populates="vehicles")
    contact_requests = relationship("ContactRequest", back_populates="vehicle")
