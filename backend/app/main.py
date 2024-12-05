from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth_routes, vehicle_routes
from app.database import engine
from app.models import user, vehicle, contact_request

# Create database tables
user.Base.metadata.create_all(bind=engine)
vehicle.Base.metadata.create_all(bind=engine)
contact_request.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vehicle Marketplace API")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include API routes
app.include_router(auth_routes.router, prefix="/api")
app.include_router(vehicle_routes.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to Vehicle Marketplace API"}
