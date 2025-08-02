# PravdaPlus - AI-Powered Satirical News Platform 🎭

A complete satirical news transformation platform that fetches real BBC news and transforms it into engaging satirical content using AI. **Currently deployed and fully operational on local Kubernetes!**

[![Security](https://img.shields.io/badge/security-gitleaks-green.svg)](https://github.com/gitleaks/gitleaks)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## ✅ **Live Demo**

**🌐 Frontend**: http://localhost:3001  
**🔗 API**: http://localhost:8000  
**📚 API Docs**: http://localhost:8000/docs

## 🚀 **Features**

- **🎭 AI-Powered Satirical Content**: GPT-4o transforms real news into engaging satirical articles
- **📰 Real-Time BBC News**: Live RSS feeds from multiple categories
- **🖥️ Modern Web Interface**: Clean, responsive Next.js frontend
- **⚡ Fast & Scalable**: Kubernetes-deployed microservices architecture
- **🔒 Security-First**: Gitleaks pre-commit hooks, no hardcoded secrets
- **🧪 Comprehensive Testing**: Health checks and validation scripts

## 🏗️ **Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Service   │    │  Transformer    │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (GPT-4o)      │
│   Port 3001     │    │   Port 8000     │    │   Port 8002     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                               │
                       ┌───────▼───────┐
                       │  PostgreSQL   │
                       │  + Redis      │
                       │  (Storage)    │
                       └───────────────┘
```

## 🔧 **Quick Start**

### Prerequisites
- Docker Desktop with Kubernetes enabled
- kubectl configured for local cluster

### 1. Deploy to Kubernetes
```bash
# Apply the complete deployment
kubectl apply -f deploy-simple-complete.yaml

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=api -n pravda-system --timeout=120s
kubectl wait --for=condition=ready pod -l app=frontend -n pravda-system --timeout=120s
kubectl wait --for=condition=ready pod -l app=transformer -n pravda-system --timeout=120s

# Set up port forwarding
kubectl port-forward svc/frontend-service 3001:3000 -n pravda-system &
kubectl port-forward svc/api-service 8000:8000 -n pravda-system &
```

### 2. Configure Environment (Optional)
```bash
# Copy environment template
cp .env.example .env

# Add your OpenAI API key for real AI transformations
# (Works with mock transformations without API key)
echo "OPENAI_API_KEY=your-openai-api-key-here" >> .env
```

### 3. Validate Deployment
```bash
# Run health checks
./final_validation.sh

# Expected output:
# ✅ API: Healthy
# ✅ Frontend: Accessible  
# ✅ News API: 5 articles retrieved
# ✅ Transformation: Working
# 🎉 All systems operational!
```

## 🎯 **How It Works**

1. **📥 News Ingestion**: Fetches real-time news from BBC RSS feeds
2. **🤖 AI Transformation**: GPT-4o rewrites articles into satirical masterpieces
3. **🌐 Web Display**: Modern interface presents satirical content as primary focus
4. **📎 Source Attribution**: Original articles linked for reference

## 📊 **API Endpoints**

### News Endpoints
```bash
# Get all categories
curl "http://localhost:8000/news"

# Get specific category
curl "http://localhost:8000/news/technology?limit=5"
```

### Transformation Endpoint
```bash
# Transform an article
curl -X POST "http://localhost:8000/transform" \
  -H "Content-Type: application/json" \
  -d '{
    "article": {
      "title": "Your news title",
      "description": "Your news description",
      "link": "https://example.com/news",
      "pub_date": "2025-08-02T06:00:00",
      "category": "world"
    },
    "style": "satirical"
  }'
```

## 🔒 **Security Features**

- **🛡️ Gitleaks Integration**: Pre-commit hooks prevent secret leaks
- **🔐 Environment Variables**: No hardcoded secrets in code
- **📋 Security Scanning**: Automated secret detection
- **🚫 .gitignore**: Comprehensive exclusion of sensitive files

### Security Setup
```bash
# Install gitleaks (if not already installed)
brew install gitleaks

# The pre-commit hook is automatically configured
# Test security scan
gitleaks detect --source . --verbose
```

## 🧪 **Testing**

### Automated Health Checks
```bash
# Comprehensive system validation
./health_check.sh

# Quick validation
./final_validation.sh
```

### Manual Testing
```bash
# Test news fetching
curl -s "http://localhost:8000/news/world?limit=1"

# Test transformation
curl -s -X POST "http://localhost:8000/transform" \
  -H "Content-Type: application/json" \
  -d '{"article":{"title":"Test","description":"Test","link":"http://test.com","pub_date":"2025-08-02T06:00:00","category":"world"},"style":"satirical"}'

# Test frontend
curl -s "http://localhost:3001" | grep "PravdaPlus"
```

## 📁 **Project Structure**

```
PravdaPlus/
├── api/                    # API service (FastAPI)
│   ├── simple_main.py      # Main application
│   ├── Dockerfile.simple   # Container definition
│   └── requirements-simple.txt
├── frontend-simple/        # Frontend service (Next.js)
│   ├── src/app/           # Application pages
│   ├── Dockerfile         # Container definition
│   └── package.json
├── transformer-simple/     # AI transformation service
│   ├── main.py            # GPT-4o integration
│   ├── Dockerfile         # Container definition
│   └── requirements.txt
├── deploy-simple-complete.yaml  # Kubernetes deployment
├── health_check.sh        # Health validation script
├── final_validation.sh    # Quick validation
├── .gitleaks.toml         # Security configuration
├── .gitignore             # Comprehensive exclusions
├── .env.example           # Environment template
└── README.md              # This file
```

## 🔧 **Management Commands**

### Check System Status
```bash
# View all pods
kubectl get pods -n pravda-system

# Check specific service
kubectl logs -f deployment/api -n pravda-system

# View services
kubectl get svc -n pravda-system
```

### Restart Services
```bash
# Restart API
kubectl rollout restart deployment/api -n pravda-system

# Restart Frontend  
kubectl rollout restart deployment/frontend -n pravda-system

# Restart Transformer
kubectl rollout restart deployment/transformer -n pravda-system
```

### Clean Up
```bash
# Remove entire deployment
kubectl delete -f deploy-simple-complete.yaml

# Or remove namespace
kubectl delete namespace pravda-system
```

## 🌟 **Key Features**

### ✅ **Confirmed Working**
- **Real BBC News Fetching**: Live RSS from 5+ categories
- **AI Content Transformation**: GPT-4o powered satirical rewriting
- **Full-Stack Web App**: Next.js frontend + FastAPI backend
- **Kubernetes Deployment**: Production-ready container orchestration
- **Security Hardened**: Gitleaks protection, no exposed secrets
- **Health Monitoring**: Comprehensive validation and testing

### 🎭 **Content Quality**
- **Category-Aware**: Different satirical styles per news category
- **Unique Content**: Each article gets personalized transformation
- **Professional Format**: Reads like real news, just funnier
- **Source Attribution**: Original articles properly referenced

## 🐛 **Troubleshooting**

### Common Issues

**Port Forward Conflicts**
```bash
# Kill existing forwards
pkill -f "kubectl port-forward"

# Restart forwards
kubectl port-forward svc/frontend-service 3001:3000 -n pravda-system &
kubectl port-forward svc/api-service 8000:8000 -n pravda-system &
```

**Pods Not Starting**
```bash
# Check pod status
kubectl describe pod -l app=api -n pravda-system

# View detailed logs
kubectl logs -f deployment/api -n pravda-system
```

**Gitleaks Pre-commit Issues**
```bash
# Run manual scan
gitleaks detect --source . --verbose

# Bypass (NOT RECOMMENDED)
git commit --no-verify
```

## 🚀 **Development**

### Adding New Features
1. Make code changes
2. Rebuild containers: `docker build -t service-name .`
3. Restart deployment: `kubectl rollout restart deployment/service-name -n pravda-system`
4. Test: `./final_validation.sh`

### Security Best Practices
- All secrets in environment variables
- Use `.env.example` as template
- Never commit `.env` files
- Run `gitleaks detect` before pushing

## 📄 **License**

MIT License - see LICENSE file for details.

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and test: `./final_validation.sh`
4. Commit with security check: `git commit -m "Add feature"`
5. Push and create pull request

---

**🎉 Ready for Production!** The application is secure, tested, and fully functional on Kubernetes.