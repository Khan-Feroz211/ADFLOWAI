#!/bin/bash

# ADFLOWAI Quick Start Script
# Sets up the entire application for development or production

set -e  # Exit on error

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         ADFLOWAI - Quick Start Installation              ║"
echo "║    AI-Powered Campaign Optimization Platform             ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi
print_status "Docker found"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi
print_status "Docker Compose found"

# Ask deployment type
echo ""
echo "Select deployment type:"
echo "  1) Development (with hot-reload, debug mode)"
echo "  2) Production (optimized, secure)"
read -p "Enter choice [1-2]: " deployment_choice

case $deployment_choice in
    1)
        DEPLOYMENT="development"
        print_status "Development mode selected"
        ;;
    2)
        DEPLOYMENT="production"
        print_status "Production mode selected"
        ;;
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    print_warning ".env file not found. Creating from template..."
    cp .env.example .env
    
    # Generate random secrets
    SECRET_KEY=$(openssl rand -hex 32)
    JWT_SECRET=$(openssl rand -hex 32)
    DB_PASSWORD=$(openssl rand -hex 16)
    
    # Update .env file
    sed -i "s/your-super-secret-key-change-this/$SECRET_KEY/" .env
    sed -i "s/your-jwt-secret-key-change-this/$JWT_SECRET/" .env
    sed -i "s/change-this-password/$DB_PASSWORD/" .env
    
    if [ "$DEPLOYMENT" == "production" ]; then
        sed -i "s/DEBUG=False/DEBUG=False/" .env
        sed -i "s/ENVIRONMENT=production/ENVIRONMENT=production/" .env
    else
        sed -i "s/ENVIRONMENT=production/ENVIRONMENT=development/" .env
    fi
    
    print_status ".env file created with secure random values"
    print_warning "Please review .env file and add your API keys!"
fi

# Create necessary directories
echo ""
print_status "Creating application directories..."
mkdir -p models uploads reports logs data

# Build and start services
echo ""
print_status "Building Docker containers..."
docker-compose build

echo ""
print_status "Starting services..."
docker-compose up -d

# Wait for database to be ready
echo ""
print_status "Waiting for database to be ready..."
sleep 10

# Initialize database
echo ""
print_status "Initializing database..."
docker-compose exec -T api python -c "
from src.core.database import db
from config.settings import Config
from app import app

with app.app_context():
    db.create_tables()
    print('Database tables created successfully!')
"

# Check if services are running
echo ""
print_status "Checking service health..."
sleep 5

# Test API health
if curl -s http://localhost:5000/health > /dev/null; then
    print_status "API is healthy!"
else
    print_error "API health check failed"
fi

# Print access information
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║              ADFLOWAI Successfully Started!              ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "Access points:"
echo "  📡 API:          http://localhost:5000"
echo "  📊 API Docs:     http://localhost:5000/api/docs"
echo "  🌸 Flower:       http://localhost:5555 (Celery monitoring)"
echo "  🗄️  PostgreSQL:  localhost:5432"
echo "  🔴 Redis:        localhost:6379"
echo ""
echo "Useful commands:"
echo "  View logs:       docker-compose logs -f"
echo "  Stop services:   docker-compose stop"
echo "  Restart:         docker-compose restart"
echo "  Shutdown:        docker-compose down"
echo "  Clean all:       docker-compose down -v"
echo ""
print_warning "Don't forget to add your platform API keys to the .env file!"
print_status "Setup complete! Happy optimizing! 🚀"
echo ""
