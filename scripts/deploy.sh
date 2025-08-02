#!/bin/bash

# PravdaPlus Deployment Script

set -e

echo "🚀 Deploying PravdaPlus..."

# Build Docker images
echo "📦 Building Docker images..."
cd "$(dirname "$0")/.."

docker build -t pravda-api:latest ./services/api
docker build -t pravda-frontend:latest ./services/frontend  
docker build -t pravda-transformer:latest ./services/transformer

echo "☸️  Deploying to Kubernetes..."
kubectl apply -f k8s/deployment.yaml

echo "⏳ Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=api -n pravda-system --timeout=120s
kubectl wait --for=condition=ready pod -l app=frontend -n pravda-system --timeout=120s
kubectl wait --for=condition=ready pod -l app=transformer -n pravda-system --timeout=120s

echo "🔗 Setting up port forwarding..."
# Kill any existing port forwards
pkill -f "kubectl port-forward" 2>/dev/null || true
sleep 2

# Start new port forwards
kubectl port-forward svc/frontend-service 3001:3000 -n pravda-system >/dev/null 2>&1 &
kubectl port-forward svc/api-service 8000:8000 -n pravda-system >/dev/null 2>&1 &

echo "✅ Deployment complete!"
echo ""
echo "🌐 Frontend: http://localhost:3001"
echo "🔗 API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "🧪 Run health checks: ./scripts/final_validation.sh"