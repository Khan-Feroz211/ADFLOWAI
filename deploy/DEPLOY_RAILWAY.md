# 🚂 Deploy ADFLOWAI to Railway (Free - Easiest)

Railway is the easiest way to get ADFLOWAI live in 15 minutes.
Free tier includes $5/month credit - enough for this app.

---

## Step 1: Sign Up
Go to https://railway.app and sign up with your GitHub account.

---

## Step 2: Create Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Select your **ADFLOWAI** repository
4. Railway auto-detects it's a Python/Docker app

---

## Step 3: Add Database
In your Railway project:
1. Click **"+ New"** → **"Database"** → **"PostgreSQL"**
2. Click **"+ New"** → **"Database"** → **"Redis"**
3. Railway creates them automatically

---

## Step 4: Set Environment Variables
In your Railway service → **Variables** tab, add:

```
SECRET_KEY          = your-super-secret-production-key-here
JWT_SECRET_KEY      = your-jwt-production-secret-here
DATABASE_URL        = ${{Postgres.DATABASE_URL}}    ← Railway fills this auto
REDIS_URL           = ${{Redis.REDIS_URL}}          ← Railway fills this auto
ENVIRONMENT         = production
DEBUG               = False
CORS_ORIGINS        = https://your-frontend.railway.app
```

---

## Step 5: Deploy
Railway auto-deploys when you push to GitHub!

Your app will be live at:
`https://adflowai-production.up.railway.app`

---

## Step 6: Deploy Frontend
1. Create another Railway service
2. Point to your `frontend/` folder
3. Set build command: `npm install && npm run build`
4. Set start command: `npx serve -s build`
5. Set environment variable:
   ```
   REACT_APP_API_URL = https://your-api.railway.app
   ```

---

## Estimated Cost
- **Free tier:** $5/month credit (enough for development)
- **Production:** ~$15-25/month for small scale

---

# 🌊 Deploy to DigitalOcean (Best Value)

## $6/month Droplet

```bash
# 1. Create $6/month Ubuntu droplet at digitalocean.com
# 2. SSH in and run these commands:

# Install Docker
curl -fsSL https://get.docker.com | sh
usermod -aG docker $USER

# Clone your repo
git clone https://github.com/Khan-Feroz211/ADFLOWAI.git
cd ADFLOWAI

# Create .env for production
cat > .env << 'ENVEOF'
SECRET_KEY=your-super-secret-production-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=postgresql://adflowai:strongpassword@postgres:5432/adflowai
REDIS_URL=redis://redis:6379/0
ENVIRONMENT=production
DEBUG=False
ENVEOF

# Start everything
docker-compose up -d

# Set up SSL with Let's Encrypt (optional)
apt install certbot
certbot certonly --standalone -d yourdomain.com
```

---

# ☁️ Deploy to AWS (Enterprise)

## Using Elastic Beanstalk (Easy AWS)

```bash
# Install AWS CLI and EB CLI
pip install awscli awsebcli

# Configure AWS
aws configure

# Initialize EB app
eb init adflowai --region us-east-1 --platform docker

# Create environment
eb create adflowai-production

# Set environment variables
eb setenv SECRET_KEY=xxx JWT_SECRET_KEY=yyy DATABASE_URL=zzz

# Deploy
eb deploy

# Open in browser
eb open
```

## Required AWS Services:
- **Elastic Beanstalk** — App hosting
- **RDS PostgreSQL** — Database (~$15/mo for db.t3.micro)
- **ElastiCache Redis** — Cache (~$12/mo for cache.t3.micro)
- **S3** — File storage (optional)

**Estimated cost:** $50-80/month

---

# 🔧 Production Checklist

Before going live, make sure:

## Security
- [ ] Change SECRET_KEY to random 50+ char string
- [ ] Change JWT_SECRET_KEY to random 50+ char string
- [ ] Set CORS_ORIGINS to your frontend domain only
- [ ] Enable HTTPS only
- [ ] Remove DEBUG=True

## Generate strong secrets:
```python
import secrets
print(secrets.token_hex(32))  # Run this twice - use for both keys
```

## Database
- [ ] Run database migrations
- [ ] Set up automated backups
- [ ] Test restore process

## Monitoring
- [ ] Set up error alerts (free: Sentry.io)
- [ ] Monitor uptime (free: UptimeRobot.com)

---

# 📊 Recommended Stack by Budget

| Budget | Platform | What you get |
|--------|----------|--------------|
| Free   | Railway  | 500MB RAM, good for demos |
| $6/mo  | DigitalOcean | 1GB RAM, real production |
| $20/mo | DigitalOcean | 4GB RAM, scales well |
| $80/mo | AWS EB + RDS | Enterprise-grade |

**Recommendation for now:** Start with Railway (free) for demos,
move to DigitalOcean $6 when you get paying customers.
