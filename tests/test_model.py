"""
Unit tests for the Hospital Scheduler ML Model
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from models.train_model import HospitalSchedulerModel
from data.generate_data import HospitalDataGenerator


class TestDataGenerator:
    """Test the data generator"""
    
    def test_generate_dataset(self):
        """Test dataset generation"""
        generator = HospitalDataGenerator(num_samples=100)
        df = generator.generate_dataset()
        
        assert len(df) == 100
        assert 'wait_time_minutes' in df.columns
        assert 'department' in df.columns
        assert df['wait_time_minutes'].min() >= 5
        
    def test_wait_time_calculation(self):
        """Test wait time calculation logic"""
        generator = HospitalDataGenerator(num_samples=100)
        df = generator.generate_dataset()
        
        # Critical patients should generally have lower wait times
        critical = df[df['priority'] == 'Critical']['wait_time_minutes'].mean()
        low = df[df['priority'] == 'Low']['wait_time_minutes'].mean()
        
        assert critical < low


class TestMLModel:
    """Test the ML model"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing"""
        generator = HospitalDataGenerator(num_samples=1000)
        return generator.generate_dataset()
    
    @pytest.fixture
    def trained_model(self, sample_data, tmp_path):
        """Train a model for testing"""
        # Save sample data
        data_path = tmp_path / "test_data.csv"
        sample_data.to_csv(data_path, index=False)
        
        # Train model
        model = HospitalSchedulerModel()
        model.train(str(data_path), test_size=0.2)
        
        return model
    
    def test_model_training(self, trained_model):
        """Test that model trains successfully"""
        assert trained_model.wait_time_model is not None
        assert 'wait_time' in trained_model.metrics
        assert trained_model.metrics['wait_time']['test_r2'] > 0
    
    def test_prediction(self, trained_model):
        """Test model prediction"""
        test_input = {
            'arrival_hour': 14,
            'day_of_week': 'Monday',
            'department': 'Emergency',
            'priority': 'High',
            'num_available_doctors': 5,
            'num_available_nurses': 8,
            'num_available_rooms': 10,
            'current_queue_length': 15,
            'patient_age': 45,
            'is_weekend': 0,
            'season': 'Winter'
        }
        
        prediction = trained_model.predict_wait_time(test_input)
        
        assert isinstance(prediction, (int, float, np.number))
        assert prediction > 0
        assert prediction < 500  # Reasonable upper bound
    
    def test_save_load_model(self, trained_model, tmp_path):
        """Test model saving and loading"""
        model_dir = tmp_path / "models"
        model_dir.mkdir()
        
        # Save model
        trained_model.save_model(str(model_dir))
        
        # Load model
        new_model = HospitalSchedulerModel()
        new_model.load_model(str(model_dir))
        
        assert new_model.wait_time_model is not None
        assert new_model.feature_columns == trained_model.feature_columns
    
    def test_feature_importance(self, trained_model):
        """Test feature importance extraction"""
        importance = trained_model.get_feature_importance(trained_model.feature_columns)
        
        assert importance is not None
        assert len(importance) > 0
        assert 'feature' in importance.columns
        assert 'importance' in importance.columns


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
