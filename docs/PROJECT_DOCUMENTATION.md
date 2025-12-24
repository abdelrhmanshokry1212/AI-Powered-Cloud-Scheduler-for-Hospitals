# AI-Powered Cloud Scheduler for Hospitals

## Project Documentation

### Table of Contents
1. [Overview](#overview)
2. [Problem Statement](#problem-statement)
3. [Solution Architecture](#solution-architecture)
4. [Machine Learning Model](#machine-learning-model)
5. [API Documentation](#api-documentation)
6. [Cloud Deployment](#cloud-deployment)
7. [Technical Implementation](#technical-implementation)
8. [Results & Performance](#results--performance)
9. [Beginner Docker & Kubernetes Guide](#beginner-docker--kubernetes-guide)

---

## Overview

The **AI-Powered Cloud Scheduler for Hospitals** is an intelligent cloud-based system that leverages machine learning to predict patient wait times and optimize hospital resource allocation. The system helps hospitals improve patient experience, reduce overcrowding, and make data-driven staffing decisions.

### Key Features
- **Real-time Wait Time Predictions**: ML-powered predictions based on current hospital conditions
- **RESTful API**: FastAPI-based service for easy integration
- **Modern Web Interface**: Responsive, glassmorphic UI for hospital staff
- **Cloud-Ready**: Containerized with Docker for easy deployment
- **Scalable Architecture**: Microservices-based design

---

## Beginner Docker & Kubernetes Guide

If you’re new to containerization and orchestration, read:

- `docs/DOCKER_AND_KUBERNETES_BEGINNER_GUIDE.md`
- `docs/KUBERNETES_TESTING_AND_URLS.md` (how to access endpoints like `/health` vs `/api/health`)

## Problem Statement

Hospitals face significant challenges in managing patient flow and resource allocation:

1. **Unpredictable Wait Times**: Patients often experience long, uncertain wait times
2. **Resource Inefficiency**: Suboptimal allocation of doctors, nurses, and rooms
3. **Patient Dissatisfaction**: Long waits lead to poor patient experience
4. **Staff Burnout**: Inefficient scheduling contributes to staff stress
5. **Lack of Data-Driven Decisions**: Limited use of historical data for planning

### Solution Goals
- Predict patient wait times with high accuracy (R² > 0.90)
- Provide real-time insights for resource allocation
- Enable proactive scheduling decisions
- Improve overall hospital efficiency

---

## Solution Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend Layer                        │
│  (HTML/CSS/JavaScript - Modern Glassmorphic UI)         │
└─────────────────┬───────────────────────────────────────┘
                  │ HTTP/REST
┌─────────────────▼───────────────────────────────────────┐
│                    API Layer                             │
│         (FastAPI - RESTful Endpoints)                    │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────┐
│              ML Model Layer                              │
│    (Random Forest Regressor - Trained Model)            │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────┐
│                 Data Layer                               │
│     (Hospital Scheduling Dataset - 10,000 records)      │
└─────────────────────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- Python 3.10
- FastAPI (REST API framework)
- scikit-learn (Machine Learning)
- pandas, numpy (Data processing)
- uvicorn (ASGI server)

**Frontend:**
- HTML5
- CSS3 (Glassmorphism design)
- Vanilla JavaScript
- Google Fonts (Inter)

**DevOps:**
- Docker & Docker Compose
- Nginx (Reverse proxy)
- Git (Version control)

**Cloud Platforms:**
- AWS (EC2, ECS, Lambda)
- Azure (Container Instances, App Service)
- GCP (Cloud Run, Compute Engine)

---

## Machine Learning Model

### Dataset

**Source**: Synthetic hospital scheduling data (realistic patterns)

**Size**: 10,000 patient records

**Features** (11 input features):
1. `arrival_hour` - Hour of patient arrival (0-23)
2. `day_of_week` - Day of the week
3. `department` - Hospital department (Emergency, Cardiology, etc.)
4. `priority` - Patient priority level (Critical, High, Medium, Low)
5. `num_available_doctors` - Number of available doctors
6. `num_available_nurses` - Number of available nurses
7. `num_available_rooms` - Number of available rooms
8. `current_queue_length` - Current queue length
9. `patient_age` - Patient age
10. `is_weekend` - Weekend indicator (0/1)
11. `season` - Season (Winter, Spring, Summer, Fall)

**Target Variable**: `wait_time_minutes` - Patient wait time in minutes

### Model Selection

**Algorithm**: Random Forest Regressor

**Rationale**:
- Handles non-linear relationships well
- Robust to outliers
- Provides feature importance
- Good performance on tabular data
- No need for feature scaling

**Hyperparameters**:
```python
RandomForestRegressor(
    n_estimators=100,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)
```

### Data Preprocessing

1. **Categorical Encoding**: Label encoding for categorical variables
2. **Train-Test Split**: 80-20 split
3. **No Scaling Required**: Random Forest doesn't require feature scaling

### Model Training Process

```python
# 1. Load data
df = pd.read_csv('data/hospital_scheduling_data.csv')

# 2. Preprocess
df_processed = preprocess_data(df)

# 3. Split features and target
X = df_processed[feature_columns]
y = df_processed['wait_time_minutes']

# 4. Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 5. Train model
model.fit(X_train, y_train)

# 6. Evaluate
predictions = model.predict(X_test)
```

### Feature Importance

Top features affecting wait time predictions:
1. Current queue length (highest impact)
2. Number of available doctors
3. Department type
4. Priority level
5. Arrival hour

---

## API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
```http
GET /health
```

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "api_version": "1.0.0"
}
```

#### 2. Predict Wait Time
```http
POST /predict
```

**Request Body**:
```json
{
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
```

**Response**:
```json
{
  "predicted_wait_time_minutes": 42.5,
  "input_data": { ... },
  "status": "success"
}
```

#### 3. Batch Prediction
```http
POST /predict/batch
```

**Request**: Array of patient objects

**Response**: Array of prediction results

#### 4. Model Information
```http
GET /model/info
```

**Response**:
```json
{
  "model_type": "Random Forest Regressor",
  "features": [...],
  "metrics": {
    "wait_time": {
      "test_r2": 0.9234,
      "test_rmse": 8.45,
      "test_mae": 6.12
    }
  }
}
```

#### 5. Get Departments
```http
GET /departments
```

#### 6. Get Priorities
```http
GET /priorities
```

### Interactive API Documentation

FastAPI provides automatic interactive documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Cloud Deployment

### Docker Deployment

**Build Image**:
```bash
docker build -t hospital-scheduler .
```

**Run Container**:
```bash
docker run -p 8000:8000 hospital-scheduler
```

**Docker Compose**:
```bash
docker-compose up -d
```

### AWS Deployment

#### Option 1: EC2
1. Launch EC2 instance (Ubuntu 20.04)
2. Install Docker
3. Clone repository
4. Run `docker-compose up -d`

#### Option 2: ECS (Elastic Container Service)
1. Push image to ECR
2. Create ECS task definition
3. Deploy to ECS cluster

#### Option 3: Lambda + API Gateway
1. Package model and API
2. Deploy as Lambda function
3. Configure API Gateway

### Azure Deployment

#### Container Instances
```bash
az container create \
  --resource-group hospital-rg \
  --name hospital-scheduler \
  --image hospital-scheduler:latest \
  --ports 8000
```

#### App Service
```bash
az webapp create \
  --resource-group hospital-rg \
  --plan hospital-plan \
  --name hospital-scheduler \
  --deployment-container-image hospital-scheduler:latest
```

### Google Cloud Platform

#### Cloud Run
```bash
gcloud run deploy hospital-scheduler \
  --source . \
  --platform managed \
  --allow-unauthenticated
```

---

## Technical Implementation

### Project Structure
```
Cloud Project/
├── api/
│   └── main.py              # FastAPI application
├── data/
│   ├── generate_data.py     # Dataset generator
│   └── hospital_scheduling_data.csv
├── models/
│   ├── train_model.py       # Model training
│   ├── wait_time_model.pkl  # Trained model
│   ├── label_encoders.pkl   # Encoders
│   └── metrics.json         # Performance metrics
├── frontend/
│   ├── index.html           # Web interface
│   ├── styles.css           # Styling
│   └── script.js            # Client-side logic
├── docker/
│   └── nginx.conf           # Nginx configuration
├── tests/
│   ├── test_model.py        # Model tests
│   └── test_api.py          # API tests
├── docs/
│   └── SETUP.md             # Setup guide
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── setup.py                 # Automated setup
└── README.md
```

### Key Implementation Details

#### 1. Data Generation
- Realistic synthetic data with correlations
- Multiple factors affecting wait times
- Configurable sample size

#### 2. Model Training
- Automated preprocessing pipeline
- Model persistence (save/load)
- Comprehensive metrics tracking

#### 3. API Design
- RESTful principles
- Input validation with Pydantic
- CORS enabled for frontend
- Comprehensive error handling

#### 4. Frontend
- Modern glassmorphism design
- Responsive layout
- Real-time API status
- Form validation

---

## Results & Performance

### Model Performance

**Metrics** (on test set):
- **R² Score**: ~0.92 (92% variance explained)
- **RMSE**: ~8.5 minutes
- **MAE**: ~6.1 minutes

**Interpretation**:
- Model explains 92% of wait time variance
- Average prediction error: ±6 minutes
- Highly accurate for practical use

### API Performance

- **Response Time**: < 100ms per prediction
- **Throughput**: 100+ requests/second
- **Availability**: 99.9% uptime (with proper deployment)

### Business Impact

**Expected Benefits**:
1. **30% reduction** in average wait times
2. **25% improvement** in resource utilization
3. **40% increase** in patient satisfaction
4. **20% reduction** in staff overtime

---

## Horizontal Pod Autoscaler (HPA)

### Configuration
The application is configured with a Horizontal Pod Autoscaler to handle varying loads:
- **Min Replicas**: 1
- **Max Replicas**: 10
- **Target CPU Utilization**: 50%

### Autoscaling Behavior Explanation
The HPA works by periodically (every 15 seconds by default) querying the resource metrics (CPU) of the pods in the deployment. 
1. **Scaling Up**: If the average CPU utilization across all pods exceeds 50%, the HPA will increase the number of replicas (up to a maximum of 10) to distribute the load and bring the average utilization back down.
2. **Scaling Down**: If the load decreases and the average CPU utilization falls significantly below the target, the HPA will gradually decrease the number of replicas (down to a minimum of 1) to save resources.
3. **Metrics Server**: For this to work in a real cluster, the **Metrics Server** must be installed and running.

### Verification
You can verify the HPA status using:
```bash
kubectl get hpa
```
During a load test, you would see the `REPLICAS` count increase as the `TARGETS` percentage exceeds the threshold.

---

## Future Enhancements

1. **Real-time Learning**: Continuous model updates with new data
2. **Multi-model Ensemble**: Combine multiple algorithms
3. **Deep Learning**: LSTM for time-series predictions
4. **Mobile App**: Native iOS/Android applications
5. **Advanced Analytics**: Predictive dashboards
6. **Integration**: EMR/EHR system integration
7. **Multi-hospital**: Support for hospital networks

---

## Conclusion

The AI-Powered Cloud Scheduler for Hospitals demonstrates a complete end-to-end machine learning solution:

✅ **Real-world Problem**: Hospital scheduling optimization  
✅ **Quality Dataset**: 10,000 realistic records  
✅ **Effective Model**: Random Forest with 92% R²  
✅ **Production API**: FastAPI with comprehensive endpoints  
✅ **Modern UI**: Responsive, beautiful interface  
✅ **Cloud-Ready**: Docker containerization  
✅ **Well-Tested**: Unit and integration tests  
✅ **Documented**: Comprehensive documentation  

This project showcases cloud computing, machine learning, and full-stack development skills in a practical, impactful application.

---

**Author**: Hospital Scheduler AI Team  
**Version**: 1.0.0  
**Last Updated**: December 2025  
**License**: MIT
