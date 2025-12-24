# AI-Powered Cloud Scheduler for Hospitals

## Project Overview
An intelligent cloud-based scheduling system for hospitals that uses machine learning to optimize resource allocation, predict patient wait times, and manage staff scheduling efficiently.

## Features
- **ML-Powered Predictions**: Predict patient wait times and resource requirements
- **REST API**: FastAPI-based service for model inference
- **Cloud-Ready**: Containerized and deployable to cloud platforms
- **Real-time Scheduling**: Optimize hospital resources in real-time
- **Data Analytics**: Comprehensive analytics dashboard

## Technology Stack
- **Backend**: Python, FastAPI
- **ML Framework**: scikit-learn, pandas, numpy
- **Database**: SQLite (development), PostgreSQL (production)
- **Containerization**: Docker
- **Cloud Platform**: AWS/Azure/GCP compatible
- **Frontend**: HTML, CSS, JavaScript

## Project Structure
```
Cloud Project/
├── data/                   # Dataset and data processing
├── models/                 # Trained ML models
├── api/                    # FastAPI application
├── frontend/              # Web interface
├── docker/                # Docker configuration
├── tests/                 # Unit and integration tests
├── notebooks/             # Jupyter notebooks for exploration
└── docs/                  # Documentation
```

## Machine Learning Component
- **Problem Type**: Regression (wait time prediction) + Classification (priority classification)
- **Dataset**: Hospital scheduling data with patient arrivals, resource usage, wait times
- **Model**: Ensemble model (Random Forest + Gradient Boosting)
- **API**: RESTful API using FastAPI for model serving

## Setup Instructions
### Prerequisites
- **Python**: 3.10+ recommended
- **pip**: installed with Python
- **(Optional) Docker**: for containerized runs
- **(Optional) kubectl + a cluster** (minikube/kind/EKS/AKS/GKE): for Kubernetes deployment

### Quick Start (Local)
1) **Create and activate a virtual environment**

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux (bash/zsh):**
```bash
python3 -m venv venv
source venv/bin/activate
```

2) **Install dependencies**
```bash
pip install -r requirements.txt
```

3) **Train the ML model**

This repository already includes a dataset at `data/hospital_scheduling_data.csv`.
```bash
python models/train_model.py
```

4) **Start the API**
```bash
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

5) **Run / open the frontend**
- **Option A (simple server)**:
```bash
python serve_frontend.py
```
Then open `http://localhost:3000/index.html`

- **Option B (open file directly)**: open `frontend/index.html` in your browser

### Useful URLs
- **Frontend**: `http://localhost:3000/index.html` (when using `serve_frontend.py`)
- **API root**: `http://localhost:8000/`
- **API docs (Swagger)**: `http://localhost:8000/docs`
- **Health**: `http://localhost:8000/health` (also `/healthz`)
- **Model info**: `http://localhost:8000/model/info`

### Test a Prediction (cURL)
```bash
curl -X POST "http://localhost:8000/predict" ^
  -H "Content-Type: application/json" ^
  -d "{\"arrival_hour\":14,\"day_of_week\":\"Monday\",\"department\":\"Emergency\",\"priority\":\"High\",\"num_available_doctors\":5,\"num_available_nurses\":8,\"num_available_rooms\":10,\"current_queue_length\":15,\"patient_age\":45,\"is_weekend\":0,\"season\":\"Winter\"}"
```

> Note: If you’re on macOS/Linux, replace `^` line continuations with `\`.

## Cloud Deployment
### Docker (recommended for quick deployment)
#### Docker Compose (API + Nginx-served frontend)
```bash
docker-compose up --build
```

Then open:
- **App (Nginx)**: `http://localhost/`
- **API (direct)**: `http://localhost:8000/`
- **API via Nginx proxy**: `http://localhost/api/` (proxies to the API container)
- **Health via Nginx**: `http://localhost/health`

#### Plain Docker (API only)
```bash
docker build -t hospital-scheduler .
docker run -p 8000:8000 -v "$(pwd)/models:/app/models" -v "$(pwd)/data:/app/data" hospital-scheduler
```

### Kubernetes
This repo includes manifests in `kubernetes/` for deploying the **API** (no frontend) plus an HPA.

1) **Build & publish an image**
- **Local cluster (minikube/kind)**: build/load the image into your cluster, or
- **Cloud cluster (EKS/AKS/GKE)**: push the image to a registry (ECR/ACR/GCR) and update `kubernetes/deployment.yaml` to point to it.

2) **Apply manifests**
```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/hpa.yaml
```

3) **Access the service**
- The service is `type: LoadBalancer`. In local clusters, you may need `minikube tunnel` or use port-forwarding:
```bash
kubectl port-forward service/hospital-scheduler 8000:80
```
Then open `http://localhost:8000/docs`

> HPA note: autoscaling requires the Kubernetes Metrics Server to be installed in the cluster.

### Cloud options (high-level)
- **AWS**: run `docker-compose` on an EC2 VM, or deploy the container to ECS/EKS.
- **Azure**: deploy the container to Azure Container Instances or AKS.
- **GCP**: deploy the container to Cloud Run (API-only) or GKE (Kubernetes).

For a more detailed guide, see `docs/SETUP.md` and `docs/PROJECT_DOCUMENTATION.md`.

## License
MIT License
