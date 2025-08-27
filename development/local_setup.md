# Local Development Setup

## Prerequisites

- Python 3.11+
- PostgreSQL (hoặc sử dụng Aiven cloud database)
- Git

## Quick Start

### 1. Clone và Setup Environment

```bash
# Clone repository
git clone <repository-url>
cd PiXerse

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Copy template và edit
cp config_template.env .env

# Edit .env với thông tin thực tế của bạn
nano .env
```

### 3. Database Setup

```bash
# Run migrations
alembic upgrade head

# (Tùy chọn) Seed database với dữ liệu mẫu
python scripts/seed_data.py
```

### 4. Start Development Server

```bash
# Với auto-reload
python main.py

# Hoặc với uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Development Tools

### Running Tests

```bash
# Chạy tất cả tests
pytest

# Với coverage
pytest --cov=app tests/

# Chỉ test một file
pytest tests/test_projects.py -v

# Với detailed output
pytest tests/ -v -s
```

### Database Migrations

```bash
# Tạo migration mới
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Check current revision
alembic current

# Migration history
alembic history
```

### Code Quality

```bash
# Format code với black (nếu cài đặt)
black app/ tests/

# Check linting với flake8 (nếu cài đặt)
flake8 app/ tests/

# Type checking với mypy (nếu cài đặt)
mypy app/
```

## Development Workflow

### 1. Feature Development

```bash
# Tạo branch mới
git checkout -b feature/new-feature

# Develop feature...

# Run tests
pytest

# Commit changes
git add .
git commit -m "Add new feature"

# Push branch
git push origin feature/new-feature
```

### 2. Database Schema Changes

```bash
# 1. Modify models trong app/models/
# 2. Generate migration
alembic revision --autogenerate -m "Add new column to users"

# 3. Review migration file
# 4. Test migration
alembic upgrade head

# 5. Test rollback
alembic downgrade -1
alembic upgrade head
```

### 3. API Endpoint Development

1. Create/update model trong `app/models/`
2. Create/update schema trong `app/schemas/`
3. Create/update service trong `app/services/`
4. Create/update endpoint trong `app/api/endpoints/`
5. Add tests trong `tests/`
6. Update documentation

## Debugging

### FastAPI Debug Mode

```python
# Trong main.py
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        debug=True    # Enable debug mode
    )
```

### Database Debugging

```python
# Enable SQL logging
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

### Using Interactive API Docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Common Issues

### 1. Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### 2. Database Connection Issues

```bash
# Check database URL trong .env
# Verify database is running
# Check firewall settings
```

### 3. Import Errors

```bash
# Verify PYTHONPATH
export PYTHONPATH=/path/to/project:$PYTHONPATH

# Hoặc install project in development mode
pip install -e .
```

### 4. Migration Conflicts

```bash
# Check migration history
alembic history

# Resolve conflicts manually
alembic merge <revision1> <revision2> -m "Merge migrations"
```

## Environment Variables for Development

```bash
# .env file cho development
DEBUG=True
DATABASE_URL=postgresql://username:password@localhost:5432/pixerse_dev
CLOUDINARY_CLOUD_NAME=dev-cloud-name
CLOUDINARY_API_KEY=dev-api-key
CLOUDINARY_API_SECRET=dev-api-secret
CORS_ORIGINS=["http://localhost:3000","http://localhost:8080"]
```

## VS Code Configuration

### .vscode/settings.json

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests"],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

### .vscode/launch.json

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "FastAPI",
            "type": "python",
            "request": "launch",
            "program": "main.py",
            "console": "integratedTerminal",
            "envFile": "${workspaceFolder}/.env"
        }
    ]
}
```

## Production Deployment Checklist

- [ ] Set `DEBUG=False`
- [ ] Use production database URL
- [ ] Configure CORS for production domains
- [ ] Set up HTTPS
- [ ] Configure reverse proxy (nginx)
- [ ] Set up monitoring
- [ ] Configure logging
- [ ] Set up backup strategy
- [ ] Performance testing
- [ ] Security testing
