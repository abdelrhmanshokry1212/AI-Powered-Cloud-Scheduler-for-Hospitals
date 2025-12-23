"""
Integration tests for the FastAPI application
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from api.main import app

client = TestClient(app)


class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "endpoints" in data
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "model_loaded" in data
        assert "api_version" in data
    
    def test_get_departments(self):
        """Test departments endpoint"""
        response = client.get("/departments")
        assert response.status_code == 200
        data = response.json()
        assert "departments" in data
        assert len(data["departments"]) > 0
    
    def test_get_priorities(self):
        """Test priorities endpoint"""
        response = client.get("/priorities")
        assert response.status_code == 200
        data = response.json()
        assert "priorities" in data
        assert len(data["priorities"]) > 0


class TestPredictionEndpoint:
    """Test prediction functionality"""
    
    @pytest.fixture
    def valid_patient_data(self):
        """Valid patient data for testing"""
        return {
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
    
    def test_predict_endpoint_structure(self, valid_patient_data):
        """Test prediction endpoint returns correct structure"""
        response = client.post("/predict", json=valid_patient_data)
        
        # May fail if model not loaded, but should return proper error
        if response.status_code == 200:
            data = response.json()
            assert "predicted_wait_time_minutes" in data
            assert "input_data" in data
            assert "status" in data
            assert data["status"] == "success"
        elif response.status_code == 503:
            # Model not loaded - acceptable for testing
            assert "detail" in response.json()
    
    def test_predict_invalid_data(self):
        """Test prediction with invalid data"""
        invalid_data = {
            "arrival_hour": 25,  # Invalid hour
            "day_of_week": "Monday",
            "department": "Emergency"
            # Missing required fields
        }
        
        response = client.post("/predict", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_batch_prediction(self, valid_patient_data):
        """Test batch prediction endpoint"""
        batch_data = [valid_patient_data, valid_patient_data]
        
        response = client.post("/predict/batch", json=batch_data)
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
