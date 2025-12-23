"""
Quick setup script for Hospital Scheduler AI
Runs all necessary setup steps in sequence
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"Output: {e.output}")
        return False

def main():
    """Main setup process"""
    
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║   AI-Powered Hospital Scheduler - Automated Setup       ║
    ║   This will set up your project in 3 simple steps       ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Generate dataset
    print("\n📊 Step 1/3: Generating hospital scheduling dataset...")
    if not run_command(
        f"{sys.executable} data/generate_data.py",
        "Generating synthetic hospital data"
    ):
        print("⚠️  Dataset generation failed, but continuing...")
    
    # Step 2: Train model
    print("\n🤖 Step 2/3: Training machine learning model...")
    if not run_command(
        f"{sys.executable} models/train_model.py",
        "Training Random Forest model"
    ):
        print("❌ Model training failed. Please check the errors above.")
        return False
    
    # Step 3: Verify setup
    print("\n✅ Step 3/3: Verifying setup...")
    
    # Check if model files exist
    model_files = [
        'models/wait_time_model.pkl',
        'models/label_encoders.pkl',
        'models/feature_columns.pkl',
        'models/metrics.json'
    ]
    
    all_exist = True
    for file in model_files:
        if Path(file).exists():
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} missing")
            all_exist = False
    
    if all_exist:
        print("""
        ╔══════════════════════════════════════════════════════════╗
        ║              🎉 SETUP COMPLETE! 🎉                       ║
        ╚══════════════════════════════════════════════════════════╝
        
        Next steps:
        
        1. Start the API server:
           python -m uvicorn api.main:app --reload
        
        2. Open the frontend:
           Open frontend/index.html in your browser
           OR
           cd frontend && python -m http.server 3000
        
        3. Access the application:
           Frontend: http://localhost:3000
           API Docs: http://localhost:8000/docs
        
        Happy scheduling! 🏥
        """)
        return True
    else:
        print("\n❌ Setup incomplete. Some files are missing.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
