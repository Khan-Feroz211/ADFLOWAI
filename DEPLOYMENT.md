# 🚀 ADFLOWAI - Production Deployment Guide

This guide will help you deploy ADFLOWAI in a production environment.

---

## 📋 Prerequisites

### System Requirements
- **OS**: Ubuntu 20.04+ / CentOS 8+ / macOS 10.15+
- **RAM**: Minimum 4GB (8GB+ recommended)
- **CPU**: 2+ cores (4+ recommended)
- **Storage**: 20GB+ available
- **Network**: Public IP or domain name

### Required Software
- Docker 20.10+
- Docker Compose 2.0+
- Git
- SSL certificate (for HTTPS)

---

## 🔧 Quick Deployment (5 Minutes)

### Option 1: Using Quick Start Script

```bash
# Clone repository
git clone https://github.com/Khan-Feroz211/ADFLOWAI.git
cd ADFLOWAI

# Run quick start
chmod +x scripts/quick_start.sh
./scripts/quick_start.sh

# Choose option 2 (Production)
```

### Option 2: Manual Docker Compose

```bash
# Clone repository
git clone https://github.com/Khan-Feroz211/ADFLOWAI.git
cd ADFLOWAI

# Create and configure .env
cp .env.example .env
nano .env  # Add your API keys

# Start services
docker-compose up -d

# Initialize database
docker-compose exec api python scripts/init_db.py

# Check status
docker-compose ps
```

---

## 🔐 Security Configuration

### 1. Environment Variables

Edit `.env` file with secure values:

```bash
# Generate secure secrets
openssl rand -hex 32  # For SECRET_KEY
openssl rand -hex 32  # For JWT_SECRET_KEY
openssl rand -hex 16  # For DB_PASSWORD

# Update .env
SECRET_KEY=<generated-secret>
JWT_SECRET_KEY=<generated-jwt-secret>
DATABASE_URL=postgresql://adflowai:<db-password>@postgres:5432/adflowai
```

### 2. API Keys Setup

Add your platform API keys to `.env`:

```bash
# Google Ads
GOOGLE_ADS_DEVELOPER_TOKEN=your_token
GOOGLE_ADS_CLIENT_ID=your_client_id
GOOGLE_ADS_CLIENT_SECRET=your_secret

# Facebook/Instagram
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_secret

# LinkedIn
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_secret
```

### 3. SSL/TLS Configuration

For production, always use HTTPS:

```bash
# Using Let's Encrypt (recommended)
sudo apt-get install certbot
sudo certbot certonly --standalone -d yourdomain.com

# Update nginx config
cp nginx/nginx.conf.example nginx/nginx.conf
# Edit with your domain and SSL paths
```

---

## 🌐 Domain & DNS Setup

### 1. Point Domain to Server

Add these DNS records:

```
A Record:     yourdomain.com        -> YOUR_SERVER_IP
CNAME Record: www.yourdomain.com    -> yourdomain.com
CNAME Record: api.yourdomain.com    -> yourdomain.com
```

### 2. Update Configuration

```bash
# Update .env
CORS_ORIGINS=https://yourdomain.com,https://api.yourdomain.com

# Update docker-compose.yml for nginx
```

---

## 📦 Database Setup

### PostgreSQL Configuration

```bash
# Access database
docker-compose exec postgres psql -U adflowai -d adflowai

# Create backup
docker-compose exec postgres pg_dump -U adflowai adflowai > backup.sql

# Restore backup
docker-compose exec -T postgres psql -U adflowai -d adflowai < backup.sql
```

### Database Migration

```bash
# Install alembic
pip install alembic

# Initialize migrations
alembic init migrations

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

---

## 🔄 CI/CD Setup

### GitHub Actions (Already Configured)

The repository includes `.github/workflows/ci-cd.yml`.

Add these secrets to GitHub:
- `DOCKER_USERNAME`: Docker Hub username
- `DOCKER_PASSWORD`: Docker Hub password/token
- `SERVER_HOST`: Production server IP
- `SERVER_USER`: SSH username
- `SSH_PRIVATE_KEY`: SSH private key

### Automated Deployment

Every push to `main` branch:
1. Runs tests
2. Builds Docker image
3. Pushes to Docker Hub
4. (Optional) Deploys to production

---

## 📊 Monitoring Setup

### 1. Prometheus & Grafana

```bash
# Add monitoring services to docker-compose.yml
# Already included in the configuration

# Access Grafana
http://your-server:3000
# Default: admin/admin
```

### 2. Application Logs

```bash
# View logs
docker-compose logs -f api

# View specific service
docker-compose logs -f celery_worker

# Save logs to file
docker-compose logs --no-color > adflowai.log
```

### 3. Health Checks

```bash
# API health
curl http://localhost:5000/health

# Database health
docker-compose exec postgres pg_isready

# Redis health
docker-compose exec redis redis-cli ping
```

---

## 🚀 Performance Optimization

### 1. Database Optimization

```sql
-- Create indexes for better performance
CREATE INDEX idx_campaigns_user_id ON campaigns(user_id);
CREATE INDEX idx_campaigns_status ON campaigns(status);
CREATE INDEX idx_platform_campaigns_campaign_id ON platform_campaigns(campaign_id);
CREATE INDEX idx_metrics_history_campaign_id ON metrics_history(campaign_id);
CREATE INDEX idx_metrics_history_recorded_at ON metrics_history(recorded_at);
```

### 2. Redis Caching

```python
# Cache configuration already included
# Adjust TTL in .env if needed
REDIS_CACHE_TTL=3600  # 1 hour
```

### 3. Application Tuning

```bash
# Increase worker processes
# Edit docker-compose.yml
command: gunicorn --bind 0.0.0.0:5000 --workers 8 --threads 4 app:app
```

---

## 🔒 Backup Strategy

### Automated Backups

```bash
# Create backup script
cat > scripts/backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=/backups

# Database backup
docker-compose exec -T postgres pg_dump -U adflowai adflowai | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Files backup
tar -czf $BACKUP_DIR/files_$DATE.tar.gz uploads/ models/ reports/

# Keep only last 30 days
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete
EOF

chmod +x scripts/backup.sh

# Add to crontab for daily backup
crontab -e
# Add: 0 2 * * * /path/to/ADFLOWAI/scripts/backup.sh
```

---

## 🔄 Update & Maintenance

### Updating ADFLOWAI

```bash
# Pull latest changes
git pull origin main

# Rebuild containers
docker-compose build

# Restart services
docker-compose down
docker-compose up -d

# Run migrations if needed
docker-compose exec api alembic upgrade head
```

### Zero-Downtime Update

```bash
# Using blue-green deployment
docker-compose -f docker-compose.blue.yml up -d
# Switch traffic
docker-compose -f docker-compose.green.yml down
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue 1: Database Connection Failed**
```bash
# Check database status
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

**Issue 2: API Not Responding**
```bash
# Check API logs
docker-compose logs api

# Verify environment variables
docker-compose exec api env | grep DATABASE

# Restart API
docker-compose restart api
```

**Issue 3: High Memory Usage**
```bash
# Check resource usage
docker stats

# Reduce worker count
# Edit docker-compose.yml
```

---

## 📞 Support & Resources

### Getting Help
- 📧 Email: support@adflowai.com
- 💬 GitHub Issues: https://github.com/Khan-Feroz211/ADFLOWAI/issues
- 📚 Documentation: /docs

### Health Check Endpoints
- API: `GET /health`
- Database: `GET /api/v1/health`

### Monitoring URLs
- Grafana: http://localhost:3000
- Flower: http://localhost:5555
- Prometheus: http://localhost:9090

---

## ✅ Production Checklist

Before going live:

- [ ] All environment variables configured
- [ ] API keys added and tested
- [ ] SSL certificate installed
- [ ] Domain DNS configured
- [ ] Database backups scheduled
- [ ] Monitoring setup complete
- [ ] Logs rotation configured
- [ ] Firewall rules applied
- [ ] Load testing completed
- [ ] Security audit done
- [ ] Documentation updated

---

## 🎯 Performance Benchmarks

Expected performance (4GB RAM, 2 CPU):

- **API Response**: < 100ms (95th percentile)
- **Campaigns**: Up to 10,000 concurrent
- **Requests**: 1000 req/sec
- **Optimization**: < 5 seconds per campaign
- **Database Queries**: < 50ms average

---

**Deployment complete! 🎉**

For questions: khan.feroz@adflowai.com
