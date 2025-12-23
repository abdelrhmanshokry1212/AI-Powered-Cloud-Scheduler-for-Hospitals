"""
FastAPI REST API for Hospital Scheduler ML Model

This API provides endpoints for:
- Predicting patient wait times
- Getting model information
- Health checks
- Batch predictions
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from models.train_model import HospitalSchedulerModel

# Initialize FastAPI app
app = FastAPI(
    title="Hospital Scheduler API",
    description="AI-Powered Cloud Scheduler for Hospitals - ML Model API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model
model = HospitalSchedulerModel()

try:
    model.load_model('models')
    print("[OK] Model loaded successfully!")
except Exception as e:
    print(f"[WARNING] Could not load model - {e}")
    print("Please train the model first by running: python models/train_model.py")


# Pydantic models for request/response
class PatientInput(BaseModel):
    """Input schema for patient scheduling prediction"""
    arrival_hour: int = Field(..., ge=0, le=23, description="Hour of arrival (0-23)")
    day_of_week: str = Field(..., description="Day of the week")
    department: str = Field(..., description="Hospital department")
    priority: str = Field(..., description="Patient priority level")
    num_available_doctors: int = Field(..., ge=0, description="Number of available doctors")
    num_available_nurses: int = Field(..., ge=0, description="Number of available nurses")
    num_available_rooms: int = Field(..., ge=0, description="Number of available rooms")
    current_queue_length: int = Field(..., ge=0, description="Current queue length")
    patient_age: int = Field(..., ge=0, le=120, description="Patient age")
    is_weekend: int = Field(..., ge=0, le=1, description="Is weekend (0 or 1)")
    season: str = Field(..., description="Season")
    
    class Config:
        schema_extra = {
            "example": {
                "arrival_hour": 14,
                "day_of_week": "Monday",
                "department": "Emergency",
                "priority": "High",
                "num_available_doctors": 5,
                "num_available_nurses": 8,
                "num_available_rooms": 10,
                "current_queue_length": 15,
                "patient_age": 45,
                "is_weekend": 0,
                "season": "Winter"
            }
        }


class PredictionResponse(BaseModel):
    """Response schema for predictions"""
    predicted_wait_time_minutes: float
    input_data: dict
    status: str = "success"


class ModelInfo(BaseModel):
    """Model information response"""
    model_type: str
    features: List[str]
    metrics: dict
    status: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    api_version: str


# API Endpoints

@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Hospital Scheduler API",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/predict",
            "batch_predict": "/predict/batch",
            "model_info": "/model/info",
            "health": "/health"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model.wait_time_model is not None,
        "api_version": "1.0.0"
    }


@app.get("/healthz", response_model=HealthResponse)
async def healthz_check():
    """Healthz check endpoint (rubric requirement)"""
    return {
        "status": "healthy",
        "model_loaded": model.wait_time_model is not None,
        "api_version": "1.0.0"
    }


@app.get("/model/info", response_model=ModelInfo)
async def get_model_info():
    """Get information about the loaded model"""
    
    if model.wait_time_model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_type": "Random Forest Regressor",
        "features": model.feature_columns,
        "metrics": model.metrics,
        "status": "loaded"
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict_wait_time(patient: PatientInput):
    """
    Predict wait time for a single patient
    
    Returns the predicted wait time in minutes based on current hospital conditions
    """
    
    if model.wait_time_model is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please train the model first.")
    
    try:
        # Convert input to dict
        input_dict = patient.dict()
        
        # Make prediction
        prediction = model.predict_wait_time(input_dict)
        
        return {
            "predicted_wait_time_minutes": round(float(prediction), 2),
            "input_data": input_dict,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/predict/batch", response_model=List[PredictionResponse])
async def predict_batch(patients: List[PatientInput]):
    """
    Predict wait times for multiple patients
    
    Accepts a list of patient inputs and returns predictions for each
    """
    
    if model.wait_time_model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        results = []
        
        for patient in patients:
            input_dict = patient.dict()
            prediction = model.predict_wait_time(input_dict)
            
            results.append({
                "predicted_wait_time_minutes": round(float(prediction), 2),
                "input_data": input_dict,
                "status": "success"
            })
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction error: {str(e)}")


@app.get("/departments")
async def get_departments():
    """Get list of available departments"""
    return {
        "departments": ["Emergency", "Cardiology", "Orthopedics", "Pediatrics", "General"]
    }


@app.get("/priorities")
async def get_priorities():
    """Get list of priority levels"""
    return {
        "priorities": ["Critical", "High", "Medium", "Low"]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
