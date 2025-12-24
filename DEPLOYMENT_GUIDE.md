# Complete Deployment Guide - AI-Powered Hospital Scheduler

## 🚀 Step-by-Step PowerShell Deployment Guide

This guide covers the complete deployment process including Docker, Kubernetes, and Minikube.

---

## Prerequisites

### Required Software
1. **Docker Desktop** - For containerization
2. **Minikube** - Local Kubernetes cluster
3. **kubectl** - Kubernetes CLI
4. **Python 3.10+** - For local development
5. **Git** - Version control

### Installation (No Chocolatey / “Normal” Windows Setup)

#### 1. Install Docker Desktop
- Download: `https://www.docker.com/products/docker-desktop/`
- After install: **restart Windows**
- Verify in PowerShell:

```powershell
docker --version
docker compose version
```

#### 2. Install kubectl (Kubernetes CLI)
- Official install guide (Windows): `https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/`
- Verify:

```powershell
kubectl version --client
```

#### 3. Install Minikube
- Download: `https://minikube.sigs.k8s.io/docs/start/`
- Verify:

```powershell
minikube version
```

#### 4. Verify Installations (All)
```powershell
# Check Docker
docker --version
docker compose version

# Check Minikube
minikube version

# Check kubectl
kubectl version --client
```

---

## 📋 Phase 1: Prepare the Application

### Step 1: Navigate to Project Directory
```powershell
cd "C:\Users\Abd El Rahman\Documents\GitHub\AI-Powered-Cloud-Scheduler-for-Hospitals"
```

### Step 2: Install Python Dependencies
```powershell
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Generate Hospital Dataset
```powershell
python data/generate_data.py
```
**Expected Output:** Creates `data/hospital_scheduling_data.csv` with 10,000 records

### Step 4: Train the ML Model
```powershell
python models/train_model.py
```
**Expected Output:** 
- Creates trained model files in `models/` directory
- Shows model performance metrics
- Files created: `wait_time_model.pkl`, `label_encoders.pkl`, `feature_columns.pkl`, `metrics.json`

---

## 🐳 Phase 2: Docker Deployment

### Step 5: Build Docker Image
```powershell
# Build the API Docker image
docker build -t hospital-scheduler-api:latest .
```

### Step 6: Test Docker Image Locally
```powershell
# Run the container
docker run -d -p 8000:8000 `
  -v ${PWD}/models:/app/models `
  -v ${PWD}/data:/app/data `
  --name hospital-api-test `
  hospital-scheduler-api:latest

# Check if container is running
docker ps

# View logs
docker logs hospital-api-test

# Test the API
curl http://localhost:8000/health
```

### Step 7: Deploy with Docker Compose
```powershell
# Stop the test container first
docker stop hospital-api-test
docker rm hospital-api-test

# Start all services with Docker Compose
docker-compose up -d

# View running containers
docker-compose ps

# View logs
docker-compose logs -f

# Test the deployment
# API: http://localhost:8000
# Frontend: http://localhost:80
# API Docs: http://localhost:8000/docs
```

### Step 8: Test Docker Deployment
```powershell
# Test API health
curl http://localhost:8000/health

# Test prediction endpoint
$body = @{
    arrival_hour = 14
    day_of_week = "Monday"
    department = "Emergency"
    priority = "High"
    num_available_doctors = 5
    num_available_nurses = 8
    num_available_rooms = 10
    current_queue_length = 15
    patient_age = 45
    is_weekend = 0
    season = "Winter"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/predict -Method Post -Body $body -ContentType "application/json"
```

---

## ☸️ Phase 3: Kubernetes Deployment with Minikube

### Step 9: Start Minikube
```powershell
# Start Minikube with Docker driver
minikube start --driver=docker --cpus=4 --memory=4096

# Enable metrics server (for HPA)
minikube addons enable metrics-server

# Verify Minikube is running
minikube status

# Check cluster info
kubectl cluster-info
```

### Step 10: Configure Docker to Use Minikube's Docker Daemon
```powershell
# Point your PowerShell to use Minikube's Docker daemon
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

# Verify you're using Minikube's Docker
docker ps
```

### Step 11: Build Docker Image in Minikube
```powershell
# Rebuild the image in Minikube's Docker environment
docker build -t hospital-scheduler-api:latest .

# Verify the image exists in Minikube
docker images | Select-String hospital-scheduler-api
```

### Step 12: Deploy to Kubernetes
```powershell
# Apply deployment
kubectl apply -f kubernetes/deployment.yaml

# Apply service
kubectl apply -f kubernetes/service.yaml

# Apply horizontal pod autoscaler
kubectl apply -f kubernetes/hpa.yaml

# Verify deployments
kubectl get deployments

# Verify pods
kubectl get pods

# Verify services
kubectl get services
```

### Step 13: Access the Application
```powershell
# Get the service URL
minikube service hospital-scheduler --url

# This will return a URL like: http://192.168.49.2:30000
# Open this URL in your browser

# Alternative: Use port forwarding
kubectl port-forward service/hospital-scheduler 8080:80

# Now access: http://localhost:8080
```

### Step 14: Monitor Kubernetes Deployment
```powershell
# Watch pods
kubectl get pods -w

# Check pod logs
kubectl logs -l app=hospital-scheduler

# Describe deployment
kubectl describe deployment hospital-scheduler

# Check HPA status
kubectl get hpa

# Open Kubernetes Dashboard
minikube dashboard
```

---

## 🧪 Phase 4: Testing & Verification

### Step 15: Test API Endpoints
```powershell
# Get the service URL (if not using port-forward)
$SERVICE_URL = minikube service hospital-scheduler --url

# Test health endpoint
curl "$SERVICE_URL/health"

# Test prediction (using port-forward example)
$body = @{
    arrival_hour = 14
    day_of_week = "Monday"
    department = "Emergency"
    priority = "High"
    num_available_doctors = 5
    num_available_nurses = 8
    num_available_rooms = 10
    current_queue_length = 15
    patient_age = 45
    is_weekend = 0
    season = "Winter"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8080/predict" -Method Post -Body $body -ContentType "application/json"
```

### Step 16: Load Testing (Optional)
```powershell
# Option A (no installs): simple request loop (Ctrl+C to stop)
while ($true) {
  try { Invoke-RestMethod -Method Get -Uri "http://localhost:8080/health" | Out-Null } catch {}
}

# Option B (recommended): k6 load test
# Install k6 via winget (if you have winget):
# winget install k6 --source winget
#
# Docs: https://grafana.com/docs/k6/latest/set-up/install-k6/
```

---

## 📊 Phase 5: Scaling & Management

### Step 17: Manual Scaling
```powershell
# Scale deployment to 3 replicas
kubectl scale deployment hospital-scheduler --replicas=3

# Watch pods being created
kubectl get pods -w

# Check running pods
kubectl get pods -l app=hospital-scheduler
```

### Step 18: Test Auto-Scaling (HPA)
```powershell
# Check HPA status
kubectl get hpa

# Generate load to trigger auto-scaling
# Open multiple PowerShell windows and run:
while ($true) { 
    Invoke-RestMethod -Uri "http://localhost:8080/health" 
    Start-Sleep -Milliseconds 100
}

# Watch HPA in action (in another window)
kubectl get hpa -w
```

### Step 19: Update Deployment (Rolling Update)
```powershell
# Make changes to your code, then rebuild
docker build -t hospital-scheduler-api:v2 .

# Update the deployment image
kubectl set image deployment/hospital-scheduler hospital-scheduler-api=hospital-scheduler-api:v2

# Watch rolling update
kubectl rollout status deployment/hospital-scheduler

# Check rollout history
kubectl rollout history deployment/hospital-scheduler

# Rollback if needed
kubectl rollout undo deployment/hospital-scheduler
```

---

## 🔍 Phase 6: Monitoring & Debugging

### Step 20: View Logs
```powershell
# Get logs from all pods
kubectl logs -l app=hospital-scheduler --all-containers=true

# Stream logs
kubectl logs -f deployment/hospital-scheduler

# Get logs from specific pod
kubectl logs <pod-name>
```

### Step 21: Debug Pod Issues
```powershell
# Describe pod to see events
kubectl describe pod <pod-name>

# Execute command in pod
kubectl exec -it <pod-name> -- /bin/bash

# Check inside the pod
kubectl exec -it <pod-name> -- ls /app/models
kubectl exec -it <pod-name> -- python -c "import joblib; print('OK')"
```

### Step 22: Resource Usage
```powershell
# Check resource usage
kubectl top nodes
kubectl top pods

# Get detailed resource info
kubectl describe nodes
```

---

## 🛑 Phase 7: Cleanup

### Step 23: Stop and Clean Up

#### Docker Compose Cleanup
```powershell
# Stop Docker Compose services
docker-compose down

# Remove volumes
docker-compose down -v

# Remove images
docker rmi hospital-scheduler-api:latest
```

#### Kubernetes Cleanup
```powershell
# Delete Kubernetes resources
kubectl delete -f kubernetes/hpa.yaml
kubectl delete -f kubernetes/service.yaml
kubectl delete -f kubernetes/deployment.yaml

# Or delete all at once
kubectl delete -f kubernetes/

# Verify deletion
kubectl get all
```

#### Minikube Cleanup
```powershell
# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete

# Clean up Minikube files (optional)
minikube delete --all --purge
```

---

## 🎯 Quick Reference Commands

### Docker Commands
```powershell
# Build
docker build -t hospital-scheduler-api:latest .

# Run
docker run -d -p 8000:8000 hospital-scheduler-api:latest

# Compose
docker-compose up -d
docker-compose down
docker-compose logs -f
```

### Kubernetes Commands
```powershell
# Apply
kubectl apply -f kubernetes/

# Get resources
kubectl get all
kubectl get pods
kubectl get services
kubectl get deployments

# Logs
kubectl logs -l app=hospital-scheduler -f

# Scale
kubectl scale deployment hospital-scheduler --replicas=5

# Delete
kubectl delete -f kubernetes/
```

### Minikube Commands
```powershell
# Start/Stop
minikube start
minikube stop
minikube delete

# Status
minikube status
minikube dashboard

# Service
minikube service hospital-scheduler
minikube service list
```

---

## 🔧 Troubleshooting Guide

### Issue: Model Not Loading
**Solution:**
```powershell
# Ensure models are trained
python models/train_model.py

# Check if model files exist
ls models/*.pkl
```

### Issue: Docker Build Fails
**Solution:**
```powershell
# Clear Docker cache
docker builder prune -a

# Rebuild with no cache
docker build --no-cache -t hospital-scheduler-api:latest .
```

### Issue: Minikube Won't Start
**Solution:**
```powershell
# Delete and restart
minikube delete
minikube start --driver=docker --force

# If still issues, try hyperv driver
minikube start --driver=hyperv
```

### Issue: Pods Not Running
**Solution:**
```powershell
# Check pod status
kubectl get pods
kubectl describe pod <pod-name>

# Check events
kubectl get events --sort-by=.metadata.creationTimestamp

# Check logs
kubectl logs <pod-name>
```

### Issue: Can't Access Service
**Solution:**
```powershell
# Use port forwarding
kubectl port-forward service/hospital-scheduler 8080:80

# Or use minikube tunnel (requires admin)
minikube tunnel
```

---

## 📈 Performance Tuning

### Optimize Resource Limits
Edit `kubernetes/deployment.yaml`:
```yaml
resources:
  requests:
    cpu: 200m
    memory: 256Mi
  limits:
    cpu: 1000m
    memory: 1Gi
```

### Optimize HPA Settings
Edit `kubernetes/hpa.yaml`:
```yaml
minReplicas: 2
maxReplicas: 20
targetCPUUtilizationPercentage: 70
```

---

## 🎉 Success Checklist

- [ ] Python dependencies installed
- [ ] Dataset generated (10,000 records)
- [ ] ML model trained successfully
- [ ] Docker image built
- [ ] Docker Compose services running
- [ ] Minikube cluster started
- [ ] Kubernetes deployment successful
- [ ] Service accessible via browser
- [ ] API endpoints responding
- [ ] HPA monitoring CPU usage
- [ ] Scaling working correctly

---

## 🌐 Access Points

After successful deployment:

| Service | Local (Docker Compose) | Kubernetes (Minikube) |
|---------|------------------------|------------------------|
| Frontend | http://localhost | `minikube service hospital-scheduler` |
| API | http://localhost:8000 | Use port-forward or minikube tunnel |
| API Docs | http://localhost:8000/docs | http://localhost:8080/docs |
| Health Check | http://localhost:8000/health | http://localhost:8080/health |
| Dashboard | - | `minikube dashboard` |

---

## 📚 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Docker Documentation**: https://docs.docker.com/
- **Kubernetes Documentation**: https://kubernetes.io/docs/
- **Minikube Documentation**: https://minikube.sigs.k8s.io/docs/

---

## 🤝 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review logs: `kubectl logs` or `docker-compose logs`
3. Verify all prerequisites are installed
4. Ensure ports are not in use by other applications

---

**Happy Deploying! 🚀**

