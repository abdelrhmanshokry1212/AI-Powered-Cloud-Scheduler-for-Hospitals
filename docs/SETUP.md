# AI-Powered Cloud Scheduler for Hospitals - Setup Guide

## Quick Start

Follow these steps to get the project running:

### Step 1: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 2: Generate Dataset

```powershell
python data/generate_data.py
```

This will create a synthetic hospital scheduling dataset with 10,000 records.

### Step 3: Train the ML Model

```powershell
python models/train_model.py
```

This will:
- Load and preprocess the data
- Train a Random Forest Regressor
- Save the trained model to `models/`
- Display model performance metrics

### Step 4: Start the API Server

```powershell
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### Step 5: Open the Frontend

Open `frontend/index.html` in your web browser, or serve it with a simple HTTP server:

```powershell
# Using Python's built-in server
cd frontend
python -m http.server 3000
```

Then navigate to: `http://localhost:3000`

## Docker Deployment

### Build and Run with Docker Compose

```powershell
docker-compose up --build
```

This will:
- Build the API container
- Start the Nginx frontend server
- Make the application available at `http://localhost`

### Individual Docker Commands

Build the image:
```powershell
docker build -t hospital-scheduler .
```

Run the container:
```powershell
docker run -p 8000:8000 -v ${PWD}/models:/app/models hospital-scheduler
```

## API Endpoints

Once the API is running, you can access:

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Model Info**: http://localhost:8000/model/info
- **Predict**: POST http://localhost:8000/predict

## Testing the API

### Using cURL

```powershell
curl -X POST "http://localhost:8000/predict" `
  -H "Content-Type: application/json" `
  -d '{
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
  }'
```

### Using Python

```python
import requests

url = "http://localhost:8000/predict"
data = {
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

response = requests.post(url, json=data)
print(response.json())
```

## Cloud Deployment

### AWS Deployment

1. **Create EC2 Instance**
   - Launch Ubuntu 20.04 instance
   - Open ports 80, 8000, 443

2. **Install Docker**
   ```bash
   sudo apt update
   sudo apt install docker.io docker-compose -y
   ```

3. **Deploy Application**
   ```bash
   git clone <your-repo>
   cd Cloud\ Project
   sudo docker-compose up -d
   ```

### Azure Deployment

1. **Create Container Instance**
   ```bash
   az container create \
     --resource-group hospital-scheduler \
     --name hospital-api \
     --image hospital-scheduler:latest \
     --ports 8000 \
     --cpu 2 --memory 4
   ```

### Google Cloud Platform

1. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy hospital-scheduler \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

## Troubleshooting

### Model Not Loading
- Ensure you've run `python models/train_model.py` first
- Check that `models/` directory contains the `.pkl` files

### API Connection Error
- Verify the API is running on port 8000
- Check firewall settings
- Update `API_BASE_URL` in `frontend/script.js` if needed

### CORS Issues
- The API has CORS enabled by default
- If issues persist, check browser console for specific errors

## Project Structure

```
Cloud Project/
├── api/                    # FastAPI application
│   └── main.py            # API endpoints
├── data/                   # Dataset and generation scripts
│   └── generate_data.py   # Dataset generator
├── models/                 # ML models
│   └── train_model.py     # Model training script
├── frontend/              # Web interface
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── docker/                # Docker configuration
│   └── nginx.conf
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Next Steps

1. ✅ Generate dataset
2. ✅ Train model
3. ✅ Start API
4. ✅ Test predictions
5. 🚀 Deploy to cloud

## Support

For issues or questions, please check:
- API documentation at `/docs`
- Model metrics in the web interface
- Console logs for error messages
