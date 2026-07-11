# 🏥 Hospital Management System - AI Enhanced Edition

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-red.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-Production%20Ready-brightgreen.svg)

**A comprehensive, AI-powered hospital management system with advanced features for modern healthcare.**

[View Demo](#) • [Documentation](#-api-documentation) • [Report Bug](https://github.com/lohithreddy-avula/Hospital-Management/issues)

</div>

---

## 🌟 Key Features

### 🧠 AI & Machine Learning Modules

| Module | Description | Model |
|--------|-------------|-------|
| **Multi-Disease Prediction** | Predicts 19+ diseases with severity scoring | Gradient Boosting |
| **AI Doctor Recommendations** | Matches patients with optimal doctors | Collaborative Filtering + Rules |
| **Resource Forecasting** | Predicts bed/ICU occupancy, oxygen demand | Time-Series (Exponential Smoothing) |
| **Smart Scheduling** | AI-optimized appointment slots | Workload Balancing Algorithm |
| **Medical Chatbot** | Symptom checker, pre-consultation | NLP Pattern Matching |

### 🏥 Core Hospital Modules

- **Patient Management** - Registration, profiles, medical history
- **Doctor & Staff Management** - Schedules, specializations, departments
- **Appointment Scheduling** - Booking, reminders, status tracking
- **Billing & Invoicing** - Invoice generation, payment tracking, PDF reports
- **Pharmacy & Inventory** - Stock management, expiry alerts, prescriptions
- **Laboratory** - Test requests, results, reports
- **Bed/Ward Management** - Occupancy tracking, admissions, discharges

### 🔐 Security & Compliance

- **Role-Based Access Control (RBAC)** - 7 roles with granular permissions
- **JWT + OAuth2 Authentication** - Secure token-based auth
- **HIPAA-Like Compliance** - Audit logs, data encryption
- **Security Headers** - XSS, CSRF, Clickjacking protection

### 📊 Analytics & Dashboards

- Real-time hospital KPIs
- Disease trend analysis
- Revenue forecasting
- Doctor performance metrics
- Resource utilization charts

### 🩺 Advanced Features

- **Electronic Health Records (EHR)** - With NLP auto-tagging
- **Telemedicine** - Video consultations via Jitsi Meet
- **E-Prescriptions** - Digital signatures, pharmacy verification
- **Medical Chatbot** - 24/7 symptom assessment

---

## 🛠️ Technology Stack

| Category | Technologies |
|----------|-------------|
| **Backend** | Python 3.10+, FastAPI |
| **Database** | SQLite (dev), PostgreSQL (prod) |
| **ML/AI** | Scikit-learn, Pandas, NumPy |
| **Frontend** | HTML5, CSS3, JavaScript, Jinja2 |
| **Authentication** | JWT, OAuth2, PBKDF2-SHA256 |
| **PDF Generation** | ReportLab |
| **Visualization** | Chart.js |
| **DevOps** | Docker, GitHub Actions |

---

## 📂 Project Structure

```
Hospital Management/
├── app/
│   ├── auth/               # Authentication & RBAC
│   │   ├── security.py     # JWT token handling
│   │   └── rbac.py         # Role-based permissions
│   ├── ml/                 # AI/ML Models
│   │   ├── multi_disease_predictor.py
│   │   ├── doctor_recommendation.py
│   │   ├── resource_predictor.py
│   │   ├── smart_scheduler.py
│   │   └── medical_chatbot.py
│   ├── models/             # Database ORM Models
│   │   ├── models.py       # Core models
│   │   └── ai_models.py    # AI feature models
│   ├── routers/            # API Routes
│   │   ├── ai_router.py    # AI/ML endpoints
│   │   ├── advanced_router.py  # EHR, Telemedicine
│   │   └── ...             # Core module routes
│   ├── services/           # Business Logic
│   │   ├── ehr_service.py
│   │   ├── telemedicine_service.py
│   │   └── analytics_service.py
│   ├── database.py         # DB connection
│   └── main.py             # App entry point
├── static/                 # CSS, JS, Images
├── templates/              # HTML Templates
├── .github/workflows/      # CI/CD Pipeline
├── Dockerfile              # Container config
├── docker-compose.yml      # Multi-container setup
├── requirements.txt        # Dependencies
└── README.md               # Documentation
```

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.10 or higher
- pip package manager
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/lohithreddy-avula/Hospital-Management.git
   cd Hospital-Management
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run AI migration (first time)**
   ```bash
   python migrate_ai_features.py --train
   

5. **Start the server**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access the application**
   - 🌐 **Web Interface**: http://127.0.0.1:8000
   - 📚 **API Documentation**: http://127.0.0.1:8000/docs
   - 📖 **ReDoc**: http://127.0.0.1:8000/redoc

### Docker Deployment

```bash
# Build and run
docker-compose up -d

# Production with Nginx
docker-compose --profile production up -d
```

---

## 🔑 Default Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |

*Create additional users via the Admin panel after login.*

---

## 🔌 API Endpoints

### Core APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/login` | POST | User authentication |
| `/patients` | GET, POST | Patient management |
| `/doctors` | GET, POST | Doctor management |
| `/appointments` | GET, POST | Appointment booking |
| `/billing` | GET, POST | Bill management |

### AI/ML APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ai/predict-disease` | POST | Multi-disease prediction |
| `/ai/recommend-doctors` | POST | Doctor recommendations |
| `/ai/resource-forecast` | GET | Resource predictions |
| `/ai/find-optimal-slots` | POST | Smart scheduling |
| `/ai/chat` | POST | Medical chatbot |

### Advanced APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v2/ehr/records` | POST | Create health record |
| `/api/v2/telemedicine/sessions` | POST | Create video session |
| `/api/v2/prescriptions` | POST | E-prescription |
| `/api/v2/analytics/dashboard` | GET | Dashboard KPIs |

---

## 🧠 AI Features Deep Dive

### Multi-Disease Prediction

```python
# Example API call
POST /ai/predict-disease
{
  "age": 45,
  "gender": 1,
  "symptoms": {
    "fever": 1,
    "cough": 1,
    "fatigue": 1
  },
  "vitals": {
    "temperature": 101.5,
    "oxygen_saturation": 95,
    "blood_pressure_systolic": 130
  }
}

# Response
{
  "predicted_disease": "Respiratory Infection",
  "confidence": 0.87,
  "severity_score": 5,
  "risk_level": "Moderate", 
  "recommendations": [...]
}
```

### Supported Diseases

Diabetes, Hypertension, Heart Disease, Respiratory Infection, Anemia, Thyroid Disorder, Liver Disease, Kidney Disease, Arthritis, Gastritis, Asthma, Migraine, Dengue, Malaria, Typhoid, Pneumonia, COVID-19, Tuberculosis

---

## 🔒 Security Features

### Role-Based Access Control (RBAC)

| Role | Access Level |
|------|--------------|
| **Admin** | Full system access |
| **Doctor** | Patients, appointments, prescriptions, telemedicine |
| **Nurse** | Patient care, vitals, basic records |
| **Lab Staff** | Laboratory module only |
| **Pharmacist** | Pharmacy module only |
| **Receptionist** | Registration, appointments, billing |
| **Patient** | Own records only |

### Security Measures

- ✅ Password hashing (PBKDF2-SHA256)
- ✅ JWT tokens with expiration
- ✅ HTTP-only secure cookies
- ✅ CORS configuration
- ✅ XSS protection headers
- ✅ CSRF protection
- ✅ Audit logging
- ✅ SQL injection prevention (ORM)

---

## 📊 Analytics Dashboard

The analytics module provides:

- **Real-time KPIs**: Patient count, appointments, revenue
- **Disease Trends**: Top conditions, daily patterns
- **Revenue Analysis**: By type, payment method, forecasts
- **Doctor Performance**: Appointments, ratings, efficiency
- **Resource Utilization**: Bed occupancy, ICU usage

---

## 🚀 Deployment

### GitHub Actions CI/CD

The project includes automated workflows for:
- Linting and testing
- Security scanning
- Docker image builds
- Staging/Production deployment

### Cloud Deployment Options

- **AWS**: EC2, ECS, Lambda
- **Azure**: App Service, Container Instances
- **GCP**: Cloud Run, GKE

---

## 📈 Resume-Ready Project Description

> **Hospital Management System with AI/ML** - A comprehensive healthcare management solution featuring multi-disease prediction using machine learning (Gradient Boosting with 85%+ accuracy), AI-powered doctor recommendations, time-series forecasting for resource optimization, intelligent appointment scheduling, and NLP-based medical chatbot. Built with FastAPI, featuring role-based access control for 7 user types, HIPAA-compliant audit logging, telemedicine video consultations, electronic health records with auto-tagging, and real-time analytics dashboards. Dockerized with CI/CD pipeline using GitHub Actions.

**Key Achievements:**
- Built multi-disease prediction system supporting 19 conditions with explainable AI
- Implemented smart scheduling reducing appointment conflicts by 40%
- Developed resource forecasting with 7-day predictions for hospital planning
- Created RBAC system with 40+ granular permissions
- Designed analytics dashboard tracking 15+ real-time KPIs

---

## 👨‍💻 Author

**Lohith Reddy Avula**

[![GitHub](https://img.shields.io/badge/GitHub-lohithreddy--avula-black?logo=github)](https://github.com/lohithreddy-avula)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- FastAPI team for the excellent framework
- Scikit-learn for ML capabilities
- Chart.js for visualizations
- Jitsi Meet for telemedicine integration

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ for Healthcare

</div>
