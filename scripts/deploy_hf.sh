#!/bin/bash

# Deploy PiXerse Backend to Hugging Face Spaces

set -e  # Exit on error

echo "🤗 Deploying PiXerse Backend to Hugging Face Spaces..."

# Check if required files exist
if [ ! -f "Dockerfile" ]; then
    echo "❌ Dockerfile not found!"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found!"
    exit 1
fi

# Create Hugging Face specific files
echo "📝 Creating Hugging Face configuration files..."

# Create app.py for Hugging Face Spaces
cat > app.py << 'EOF'
"""
Hugging Face Spaces entry point for PiXerse Backend
"""

import uvicorn
from main import app

if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=7860,  # Hugging Face Spaces default port
        log_level="info"
    )
EOF

# Create README for Hugging Face Spaces
cat > README_HF.md << 'EOF'
---
title: PiXerse Backend
emoji: 🎨
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# PiXerse Backend API

Backend API for PiXerse Landing Page CMS - A comprehensive content management system for projects, team members, blogs, and media assets.

## Features

- 🚀 **FastAPI** - Modern Python web framework
- 🗄️ **PostgreSQL** - Robust database with Alembic migrations  
- ☁️ **Cloudinary** - Cloud-based media management
- 🔒 **Security** - JWT authentication and validation
- 📚 **API Documentation** - Auto-generated with Swagger/OpenAPI
- 🧪 **Testing** - Comprehensive test suite with pytest

## API Endpoints

- **Projects**: Manage project information and portfolios
- **Members**: Team member profiles and roles
- **Blogs**: Content management for blog posts
- **Assets**: Media file upload and management via Cloudinary

## Usage

Visit the API documentation at `/docs` for interactive API exploration.

## Environment Variables

Configure the following environment variables:

- `DATABASE_URL`: PostgreSQL connection string
- `CLOUDINARY_*`: Cloudinary configuration for media storage
- `SECRET_KEY`: Application secret key
- `JWT_SECRET_KEY`: JWT signing key

Built with ❤️ for modern web development.
EOF

echo "✅ Hugging Face files created!"

echo "📋 Next steps for Hugging Face deployment:"
echo "1. Create a new Space on Hugging Face Hub"
echo "2. Choose 'Docker' as the SDK"
echo "3. Upload all files to your Space repository"
echo "4. Configure environment variables in Space settings:"
echo "   - DATABASE_URL"
echo "   - CLOUDINARY_CLOUD_NAME"
echo "   - CLOUDINARY_API_KEY" 
echo "   - CLOUDINARY_API_SECRET"
echo "5. Your API will be available at https://[USERNAME]-[SPACE_NAME].hf.space"

echo ""
echo "🔗 Useful links:"
echo "   - Hugging Face Spaces: https://huggingface.co/spaces"
echo "   - Docker SDK docs: https://huggingface.co/docs/hub/spaces-sdks-docker"
