#!/bin/bash

# Build and run PiXerse Backend with Docker

set -e  # Exit on error

echo "🐳 Building PiXerse Backend Docker image..."

# Build the Docker image
docker build -t pixerse-backend .

echo "✅ Docker image built successfully!"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Copying from config_template.env..."
    cp config_template.env .env
    echo "📝 Please edit .env file with your actual configuration"
fi

echo "🚀 To run the container, use:"
echo "docker run -p 8000:8000 --env-file .env pixerse-backend"
echo ""
echo "🐙 Or use docker-compose:"
echo "docker-compose up -d"
echo ""
echo "📊 Access the API at: http://localhost:8000"
echo "📚 API docs at: http://localhost:8000/docs"
