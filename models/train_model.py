"""
Machine Learning Model for Hospital Scheduling

This module implements the ML model for predicting patient wait times
and classifying patient priority. It includes:
- Data preprocessing
- Model training (Random Forest Regressor)
- Model evaluation
- Model saving/loading
- Feature importance analysis
"""

import pandas as pd
import numpy as np
import joblib
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.metrics import classification_report, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


class HospitalSchedulerModel:
    """ML Model for hospital scheduling predictions"""
    
    def __init__(self):
        self.wait_time_model = None
        self.priority_classifier = None
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_columns = None
        self.metrics = {}
        
    def preprocess_data(self, df):
        """Preprocess the dataset for training"""
        
        print("Preprocessing data...")
        
        # Create a copy
        df_processed = df.copy()
        
        # Encode categorical variables
        categorical_cols = ['day_of_week', 'department', 'priority', 'season']
        
        for col in categorical_cols:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
                df_processed[col] = self.label_encoders[col].fit_transform(df_processed[col])
            else:
                df_processed[col] = self.label_encoders[col].transform(df_processed[col])
        
        return df_processed
    
    def train_wait_time_model(self, X_train, y_train, X_test, y_test):
        """Train the wait time prediction model (Regression)"""
        
        print("\n=== Training Wait Time Prediction Model ===")
        
        # Initialize Random Forest Regressor
        self.wait_time_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        
        # Train the model
        print("Training Random Forest Regressor...")
        self.wait_time_model.fit(X_train, y_train)
        
        # Make predictions
        y_pred_train = self.wait_time_model.predict(X_train)
        y_pred_test = self.wait_time_model.predict(X_test)
        
        # Calculate metrics
        train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
        test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
        train_mae = mean_absolute_error(y_train, y_pred_train)
        test_mae = mean_absolute_error(y_test, y_pred_test)
        train_r2 = r2_score(y_train, y_pred_train)
        test_r2 = r2_score(y_test, y_pred_test)
        
        self.metrics['wait_time'] = {
            'train_rmse': float(train_rmse),
            'test_rmse': float(test_rmse),
            'train_mae': float(train_mae),
            'test_mae': float(test_mae),
            'train_r2': float(train_r2),
            'test_r2': float(test_r2)
        }
        
        print(f"Training RMSE: {train_rmse:.2f} minutes")
        print(f"Testing RMSE: {test_rmse:.2f} minutes")
        print(f"Training MAE: {train_mae:.2f} minutes")
        print(f"Testing MAE: {test_mae:.2f} minutes")
        print(f"Training R²: {train_r2:.4f}")
        print(f"Testing R²: {test_r2:.4f}")
        
        return self.wait_time_model
    
    def get_feature_importance(self, feature_names):
        """Get feature importance from the trained model"""
        
        if self.wait_time_model is None:
            return None
        
        importance = self.wait_time_model.feature_importances_
        feature_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        return feature_importance
    
    def train(self, data_path, test_size=0.2):
        """Complete training pipeline"""
        
        print("Loading data...")
        df = pd.read_csv(data_path)
        
        print(f"Dataset shape: {df.shape}")
        
        # Preprocess data
        df_processed = self.preprocess_data(df)
        
        # Define features and target
        target_col = 'wait_time_minutes'
        exclude_cols = ['patient_id', target_col]
        
        self.feature_columns = [col for col in df_processed.columns if col not in exclude_cols]
        
        X = df_processed[self.feature_columns]
        y = df_processed[target_col]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        print(f"Training set size: {len(X_train)}")
        print(f"Testing set size: {len(X_test)}")
        
        # Train wait time model
        self.train_wait_time_model(X_train, y_train, X_test, y_test)
        
        # Get feature importance
        feature_importance = self.get_feature_importance(self.feature_columns)
        print("\n=== Feature Importance ===")
        print(feature_importance.head(10))
        
        return self.metrics
    
    def predict_wait_time(self, input_data):
        """Predict wait time for new data"""
        
        if self.wait_time_model is None:
            raise ValueError("Model not trained yet!")
        
        # Ensure input is DataFrame
        if isinstance(input_data, dict):
            input_data = pd.DataFrame([input_data])
        
        # Preprocess
        input_processed = self.preprocess_data(input_data)
        
        # Select features
        X = input_processed[self.feature_columns]
        
        # Predict
        prediction = self.wait_time_model.predict(X)
        
        return prediction[0] if len(prediction) == 1 else prediction
    
    def save_model(self, model_dir='models'):
        """Save the trained model and encoders"""
        
        model_dir = Path(model_dir)
        model_dir.mkdir(exist_ok=True)
        
        print(f"\nSaving model to {model_dir}...")
        
        # Save the model
        joblib.dump(self.wait_time_model, model_dir / 'wait_time_model.pkl')
        
        # Save encoders
        joblib.dump(self.label_encoders, model_dir / 'label_encoders.pkl')
        
        # Save feature columns
        joblib.dump(self.feature_columns, model_dir / 'feature_columns.pkl')
        
        # Save metrics
        with open(model_dir / 'metrics.json', 'w') as f:
            json.dump(self.metrics, f, indent=2)
        
        print("[OK] Model saved successfully!")
    
    def load_model(self, model_dir='models'):
        """Load a trained model"""
        
        model_dir = Path(model_dir)
        
        print(f"Loading model from {model_dir}...")
        
        # Load the model
        self.wait_time_model = joblib.load(model_dir / 'wait_time_model.pkl')
        
        # Load encoders
        self.label_encoders = joblib.load(model_dir / 'label_encoders.pkl')
        
        # Load feature columns
        self.feature_columns = joblib.load(model_dir / 'feature_columns.pkl')
        
        # Load metrics
        with open(model_dir / 'metrics.json', 'r') as f:
            self.metrics = json.load(f)
        
        print("[OK] Model loaded successfully!")
        
        return self


def main():
    """Main training script"""
    
    # Initialize model
    model = HospitalSchedulerModel()
    
    # Train model
    metrics = model.train('data/hospital_scheduling_data.csv')
    
    # Save model
    model.save_model('models')
    
    print("\n" + "="*50)
    print("MODEL TRAINING COMPLETE!")
    print("="*50)
    print(f"\nTest R² Score: {metrics['wait_time']['test_r2']:.4f}")
    print(f"Test RMSE: {metrics['wait_time']['test_rmse']:.2f} minutes")
    print(f"Test MAE: {metrics['wait_time']['test_mae']:.2f} minutes")
    
    # Test prediction
    print("\n=== Testing Prediction ===")
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
    
    prediction = model.predict_wait_time(test_input)
    print(f"Predicted wait time: {prediction:.2f} minutes")
    print(f"Input: {test_input}")


if __name__ == "__main__":
    main()
