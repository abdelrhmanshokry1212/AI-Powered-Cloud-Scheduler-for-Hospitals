"""
Hospital Scheduling Dataset Generator

This module generates synthetic but realistic hospital scheduling data
for training the ML model. The dataset includes:
- Patient arrival times
- Department types
- Patient priority levels
- Resource availability
- Wait times (target variable)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

class HospitalDataGenerator:
    """Generate realistic hospital scheduling data"""
    
    def __init__(self, num_samples=10000):
        self.num_samples = num_samples
        self.departments = ['Emergency', 'Cardiology', 'Orthopedics', 'Pediatrics', 'General']
        self.priority_levels = ['Critical', 'High', 'Medium', 'Low']
        self.days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
    def generate_dataset(self):
        """Generate the complete dataset"""
        
        data = {
            'patient_id': range(1, self.num_samples + 1),
            'arrival_hour': np.random.randint(0, 24, self.num_samples),
            'day_of_week': np.random.choice(self.days_of_week, self.num_samples),
            'department': np.random.choice(self.departments, self.num_samples, 
                                          p=[0.35, 0.20, 0.15, 0.15, 0.15]),
            'priority': np.random.choice(self.priority_levels, self.num_samples,
                                        p=[0.10, 0.25, 0.40, 0.25]),
            'num_available_doctors': np.random.randint(1, 10, self.num_samples),
            'num_available_nurses': np.random.randint(2, 15, self.num_samples),
            'num_available_rooms': np.random.randint(1, 20, self.num_samples),
            'current_queue_length': np.random.randint(0, 50, self.num_samples),
            'patient_age': np.random.randint(1, 95, self.num_samples),
            'is_weekend': [1 if day in ['Saturday', 'Sunday'] else 0 
                          for day in np.random.choice(self.days_of_week, self.num_samples)],
            'season': np.random.choice(['Winter', 'Spring', 'Summer', 'Fall'], self.num_samples),
        }
        
        df = pd.DataFrame(data)
        
        # Generate realistic wait times based on features
        df['wait_time_minutes'] = self._calculate_wait_times(df)
        
        # Add some noise to make it more realistic
        noise = np.random.normal(0, 5, self.num_samples)
        df['wait_time_minutes'] = np.maximum(5, df['wait_time_minutes'] + noise)
        
        return df
    
    def _calculate_wait_times(self, df):
        """Calculate realistic wait times based on hospital conditions"""
        
        base_wait = 30  # Base wait time in minutes
        
        # Priority impact (critical patients wait less)
        priority_impact = df['priority'].map({
            'Critical': -20,
            'High': -10,
            'Medium': 0,
            'Low': 15
        })
        
        # Department impact
        dept_impact = df['department'].map({
            'Emergency': 10,
            'Cardiology': 25,
            'Orthopedics': 20,
            'Pediatrics': 15,
            'General': 30
        })
        
        # Resource availability impact
        resource_impact = (
            -2 * df['num_available_doctors'] +
            -1 * df['num_available_nurses'] +
            -0.5 * df['num_available_rooms']
        )
        
        # Queue length impact
        queue_impact = 2 * df['current_queue_length']
        
        # Time of day impact (peak hours have longer waits)
        time_impact = df['arrival_hour'].apply(lambda x: 
            20 if 9 <= x <= 17 else 10 if 18 <= x <= 22 else 0
        )
        
        # Weekend impact
        weekend_impact = df['is_weekend'] * 15
        
        # Calculate total wait time
        wait_time = (base_wait + priority_impact + dept_impact + 
                    resource_impact + queue_impact + time_impact + weekend_impact)
        
        return np.maximum(5, wait_time)  # Minimum 5 minutes wait


def generate_and_save_data(output_path='data/hospital_scheduling_data.csv', num_samples=10000):
    """Generate and save the dataset"""
    
    print(f"Generating {num_samples} hospital scheduling records...")
    generator = HospitalDataGenerator(num_samples)
    df = generator.generate_dataset()
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"Dataset saved to {output_path}")
    
    # Print statistics
    print("\n=== Dataset Statistics ===")
    print(f"Total records: {len(df)}")
    print(f"\nWait Time Statistics:")
    print(df['wait_time_minutes'].describe())
    print(f"\nDepartment Distribution:")
    print(df['department'].value_counts())
    print(f"\nPriority Distribution:")
    print(df['priority'].value_counts())
    
    return df


if __name__ == "__main__":
    # Generate dataset
    df = generate_and_save_data(num_samples=10000)
    print("\n[OK] Dataset generation complete!")
