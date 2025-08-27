# PiXerse Backend

🎨 **Modern Backend API for PiXerse Landing Page CMS**

A comprehensive content management system API built with FastAPI, providing robust CRUD operations for projects, team members, blogs, and media assets with cloud storage integration.

## ✨ Features

- 🚀 **FastAPI** - High-performance async web framework
- 🗄️ **PostgreSQL** - Robust relational database with Alembic migrations
- ☁️ **Cloudinary Integration** - Cloud-based media storage and optimization
- 📚 **Auto-generated Documentation** - Interactive API docs with Swagger/OpenAPI
- 🔒 **Security Ready** - JWT authentication and environment-based configuration
- 🧪 **Comprehensive Testing** - Full test suite with pytest
- 🐳 **Docker Ready** - Container support for easy deployment

## 🏗️ Architecture

```
app/
├── api/endpoints/      # API route handlers
├── models/            # SQLAlchemy database models  
├── schemas/           # Pydantic request/response models
├── services/          # Business logic layer
└── database/          # Database configuration

tests/                 # Test suite
docs/                  # Documentation
development/           # Development tools and guides
scripts/               # Deployment and utility scripts
```

## 🗄️ Data Models

- **Projects** - Portfolio projects with descriptions
- **Members** - Team member profiles and roles
- **Blogs** - Content posts linked to projects
- **Assets** - Media files managed via Cloudinary
- **Associations** - Many-to-many relationships between entities

## 🚀 Quick Start

### Production Deployment

**Docker (Recommended)**
```bash
# Build and run
docker build -t pixerse-backend .
docker run -p 8000:8000 --env-file .env pixerse-backend

# Or with docker-compose
docker-compose -f docker-compose.prod.yml up -d
```

**Environment Setup**
```bash
# Copy configuration template
cp config_template.env .env

# Edit with your actual values
nano .env
```

### Development Setup

See [development/local_setup.md](development/local_setup.md) for detailed development instructions.

```bash
# Quick start for development
pip install -r requirements.txt
alembic upgrade head
python main.py
```

## 📚 API Documentation

- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc  
- **Detailed Guide**: [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)

## 🛠️ Core Endpoints

| Resource | Endpoints | Description |
|----------|-----------|-------------|
| **Projects** | `GET/POST /api/v1/projects/` | Manage project portfolios |
| **Members** | `GET/POST /api/v1/members/` | Team member profiles |
| **Blogs** | `GET/POST /api/v1/blogs/` | Content management |
| **Assets** | `POST /api/v1/assets/upload` | File upload to Cloudinary |

Each resource supports full CRUD operations with filtering, pagination, and asset associations.

## 🔒 Security Configuration

**⚠️ QUAN TRỌNG: Bảo mật**
- **KHÔNG BAO GIỜ** commit file `.env` vào Git
- **LUÔN LUÔN** sử dụng biến môi trường cho secrets
- **CHẠY** `python3 scripts/check_security.py` trước khi commit

**Required Environment Variables:**
```bash
# Database
DATABASE_URL=postgresql://username:password@host:port/database?sslmode=require

# Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key  
CLOUDINARY_API_SECRET=your-api-secret

# Security
SECRET_KEY=your-secret-key-at-least-32-characters
JWT_SECRET_KEY=your-jwt-secret-key
```

📋 **Setup Guide:**
1. Copy: `cp config_template.env .env`
2. Fill your actual values in `.env`
3. Verify: `python3 scripts/check_security.py`

📖 **Security Documentation:** [SECURITY.md](SECURITY.md)

## 🧪 Testing

```bash
# Run full test suite
pytest tests/ -v

# With coverage
pytest --cov=app tests/
```

## 🌍 Deployment Options

- **🤗 Hugging Face Spaces**: Run `scripts/deploy_hf.sh` for setup instructions
- **🐳 Docker**: Production-ready containers with multi-stage builds
- **☁️ Cloud Platforms**: Compatible with AWS, GCP, Azure, Railway, etc.

## 📖 Documentation

- [📋 API Documentation](docs/API_DOCUMENTATION.md) - Complete API reference
- [🛠️ Development Setup](development/local_setup.md) - Local development guide
- [🚀 Deployment Guide](scripts/) - Production deployment scripts

## 🏥 Health & Monitoring

- Health Check: `GET /health`
- Metrics: Built-in FastAPI metrics
- Logging: Structured JSON logging for production

---

Built with ❤️ using modern Python technologies for scalable web development.
